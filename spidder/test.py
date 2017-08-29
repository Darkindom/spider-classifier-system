# coding=utf-8
import re
import json
import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

f = open('/Users/darkindom/Desktop/spidder/spider_json/aa.json', "r")
item = json.load(f)
print item

for i in item['data']:
    print i['title']
    print i['authors']
    print i['abstract']
    print i['fields']

f.close()
