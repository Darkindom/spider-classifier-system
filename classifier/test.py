# coding=utf-8
import json
import os, sys
reload(sys)
sys.setdefaultencoding('utf-8')

path_file = os.path.abspath(sys.argv[0])

path_parent = os.path.abspath(os.path.join(path_file, os.pardir))
path_file = os.path.dirname(path_file) + '/'
path_spider = os.path.dirname(path_parent) + '/spider_json/'

print path_file
print path_spider
