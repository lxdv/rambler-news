## Rambler News parser

Simple news parser from https://news.rambler.ru implemented as part of the 
Natural Language Processing course.

Collected data is available [here](https://drive.google.com/file/d/1ByVbdR6UZb_z6l_nSLBx4u4zI2Npd0-2/view?usp=sharing)

*National Research University - Higher School of Economics.* &copy;2019

## Dependencies

* Python 3.6.7
   * urllib3==1.23  
   * lxml==4.3.1
   * numpy==1.14.2

It can be easily installed via ```pip3 install -r requirements.txt```  


## Usage

#### TL;DR

Run `main.py` and get news for last week

#### Detailed

```
parser = RamblerParser(num_pools=50, num_workers=50, days=7, 
            output="output.json", re_pattern='[\s&nbsp]+', pages=50)
parser.parse()
```
where

* **num_pools** - Number of pools for *urllib3.PoolManager(num_pools=num_pools)*
* **num_workers** - Number of workers
* **days** - Collect data from N days ago up to now
* **pages** - Number of pages for each date
* **re_pattern** - Pattern for regexp.
* **output** - File to save data

## Output format

Output example is represented in `output-example.json`. It's JSON per line with `title`, `descr`, `link`, `date`.
```json
{"title": " ВБ выделит Египту $8 млрд ", "descr": " В период с 2015 по 2019 год Всемирный банк выделит Египту кредит на 8 млрд долларов для проведения экономических реформ, сообщило египетское информагентство MENA. В пятницу Египет получил первый транш от Всемирного банка на 1 миллиард долларов. Выделение денег направлено на стабилизацию финансовых рынков, повышение конкурентоспособности за счет создания рабочих мест и на привлечение инвестиций в частный сектор. Сотрудничество с Всемирным банком поможет Египту в таких отраслях, как энергетика, транспорт, сельское хозяйство и здравоохранение, заявил чиновник ВБ. ", "link": "https://news.rambler.ru/africa/34682008-vb-vydelit-egiptu-8-mlrd/", "date": 1473544816.8916}
{"title": " На побережье Ливии обнаружили тела 16 мигрантов ", "descr": " В Ливии на берегу города Зувара были обнаружены тела 16 мигрантов, передает Reuter со ссылкой на представителя Красного Полумесяца. Представитель организации Аль-Хамис аль-Босайфи уточнил, что все погибшие были беженцами из африканских стран. Он также добавил, что определить, когда утонули мигранты, невозможно из-за состояния тел. Ранее сообщалось, что в Средиземном море у побережья Ливии пропали без вести более 90 мигрантов. ", "link": "https://news.rambler.ru/africa/35136161-na-poberezhe-livii-obnaruzhili-tela-16-migrantov/", "date": 1477778416.8916}
```