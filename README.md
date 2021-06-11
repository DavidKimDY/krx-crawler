# krx-crawler
hi

## Setup on EC2 ubuntu 20.02
```
$ git clone https://github.com/DavidKimDY/krx-crawler.git
$ git clone https://github.com/DavidKimDY/CoreDotFinance.git
$ cd CoreDotFinance
$ sudo python3 setup.py install
$ cd ../krx_data
$ pip3 install -r requirements.txt
$ vi .env
$ python3 krx_crawler.py
```
