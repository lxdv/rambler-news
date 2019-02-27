import datetime
import json
import os.path as osp
import re
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import urllib3
from lxml import html

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class RamblerParser:
    def __init__(self, num_pools=50, num_workers=50, days=7, output="output.json", re_pattern=None, pages=50):
        base = datetime.datetime.today()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'
        }
        if re_pattern:
            self.re = re.compile(re_pattern)
        else:
            self.re = re.compile('[\s&nbsp]+')
        self.pool_manager = urllib3.PoolManager(num_pools=num_pools, headers=self.headers)
        self.num_workers = num_workers
        self.date_list = [base - datetime.timedelta(days=x) for x in range(days)]
        self.output = output
        self.root = 'https://news.rambler.ru'
        self.links_xpath = '/html/body/div[7]/div/div/div[3]/div[2]/div/div[1]/div[2]/div/div/a[1]'
        self.title_xpath = '/html/body/div[7]/div/div/div[3]/div[2]/div/div[1]/div[3]/h1'
        self.descr_xpaths = ['/html/body/div[7]/div/div/div[3]/div[2]/div/div[1]/div[6]',
                             '/html/body/div[7]/div/div/div[3]/div[2]/div/div[1]/div[5]']
        self.pages = pages

    def get_links_by_date(self, date, page=None):
        link = osp.join(self.root, '{}/{:02}/{:02}'.format(date.year, date.month, date.day))
        if page:
            link += "?page=" + str(page)
        r = self.pool_manager.request('GET', link, preload_content=True, headers=self.headers)
        return [osp.join(self.root, i.get('href')[1:]) for i in html.fromstring(r.data).xpath(self.links_xpath)]

    def get_by_link(self, link):
        r = self.pool_manager.request('GET', link, preload_content=True, headers=self.headers)
        title = html.fromstring(r.data).xpath(self.title_xpath)[0].text_content()

        for xpath in self.descr_xpaths:
            descr = html.fromstring(r.data).xpath(xpath)[0].text_content()
            if re.search('[А-Яа-яЁё]', descr):
                title = self.re.sub(' ', title)
                descr = self.re.sub(' ', descr)
                return {
                    'title': title,
                    'descr': descr,
                    'link': link
                }
        return None

    def f(self, date):
        print("Starting parsing from {:02}/{:02}/{}".format(date.day, date.month, date.year))
        links = [self.get_links_by_date(date, page=i) for i in range(1, self.pages + 1)]
        links = np.unique(np.hstack(links))
        for link in links:
            parsed_data = self.get_by_link(link)
            if parsed_data:
                parsed_data['date'] = date.timestamp()
                parsed_data = json.dumps(parsed_data, ensure_ascii=False)
                with open(self.output, 'a') as file:
                    file.write(parsed_data + '\n')
        print(" * Success {:02}/{:02}/{}".format(date.day, date.month, date.year))

    def parse(self):
        if self.num_workers > 1:
            exec = ThreadPoolExecutor(max_workers=self.num_workers)
            exec.map(self.f, self.date_list)
        else:
            for date in self.date_list:
                self.f(date)
