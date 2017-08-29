# coding=utf-8
import re
import json
import requests
from bs4 import BeautifulSoup
import os, sys
reload(sys)
sys.setdefaultencoding('utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
page = 20

path_file = os.path.abspath(sys.argv[0])

path_parent = os.path.abspath(os.path.join(path_file, os.pardir))
path_file = os.path.dirname(path_file) + '/'
path_parent = os.path.dirname(path_parent) + '/'

print path_file
print path_parent
