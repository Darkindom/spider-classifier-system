# coding=utf-8
import json
import requests
from bs4 import BeautifulSoup
import os, sys
reload(sys)
sys.setdefaultencoding('utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
page = 2

path_file = os.path.abspath(sys.argv[0])
path_parent = os.path.abspath(os.path.join(path_file, os.pardir))
path_file = os.path.dirname(path_file) + '/'
path_parent = os.path.dirname(path_parent) + '/'

file_url_path = path_parent + 'spider_json/url_'
file_data_path = path_parent + 'spider_json/data_'
file_keywords_path = path_file + 'keywords.txt'

def getKeywords():
    with open(file_keywords_path, "r") as f_keywords:
        keywords = f_keywords.readlines()
        f_keywords.close()
    return keywords

def getUrls(keyword, index):
    f_url = open(file_url_path + keyword + '_' + str(index) + '.txt', "r")
    urls = f_url.readlines()
    f_url.close()
    return urls

def searchUrls(keyword, index):
    f_url = open(file_url_path + keyword + '_' + str(index) + '.txt', "w")
    for i in range(page):
        sourceUrl = 'http://cn.bing.com/academic/search?q=' + keyword + '&first=' + str(i) + '1&FORM=PENR'
        r_url = requests.get(sourceUrl, headers = headers)
        content = r_url.text
        soup = BeautifulSoup(content, 'lxml')
        items = soup.find_all(class_ = 'aca_algo')

        for item in items:
            itemUrl = item.h2.a.attrs['href']
            if re.match('/academic', itemUrl, re.M|re.I):
                url = 'http://cn.bing.com' + itemUrl
                print url
                f_url.write(url + '\n')
    f_url.close()

def searchItem(keyword, urls, index):
    f_data = open(file_data_path + str(index) + '.json', "w")
    item = {
        'num': 0,
        'data': []
    }

    for url in urls:
        url = url.strip('\n')
        r_data = requests.get(url, headers = headers)
        content = r_data.text
        soup = BeautifulSoup(content, 'lxml')

        title = soup.find(class_ = 'aca_title')
        results = soup.find_all(class_ = 'aca_content')

        try:
            if results[1].div.span.span != None:
                print '\n---- title ----\n', title.get_text(),'\n'
                data = {
                    'title': '',
                    'url': '',
                    'authors': [],
                    'abstract': '',
                    'types': [],
                    'fields': ''
                }
                data['title'] = title.get_text()
                data['url'] = url

                for i,result in enumerate(results):
                    if i == 0:
                        authors = result.div.span.find_all('a')
                        print '---- authors ----'
                        for author in authors:
                            print author.get_text()
                            data['authors'].append(author.get_text())
                    if i == 1:
                        abstract = result.div.span.span['title']
                        print '\n---- abstract ----\n',abstract,'\n'
                        data['abstract'] = str(abstract)
                    if i == 2:
                        fields = result.find_all(class_ = 'aca_badge')
                        # print '---- fields ----'
                        for field in fields:
                            # print field.a.get_text()
                            data['types'].append(field.a.get_text())
                        print '---- fields ----'
                        print keyword
                        data['fields'] = str(keyword);
                        print '\n------------------------------------------------------------------------------------------\n'
                item['data'].append(data)
                item['num'] += 1
            else:
                continue
        except:
            continue
    json.dump(item, f_data, sort_keys = True, indent = 4)
    print keyword + ' have ' + str(item['num']) + ' papers\n'
    f_data.close()

print "start"
keywords = getKeywords()
index = 1
for keyword in keywords:
    keyword = keyword.strip('\n')
    print 'search for ' + keyword + '\n'
    searchUrls(keyword, index)
    urls = getUrls(keyword, index)
    searchItem(keyword, urls, index)
    index += 1
print "end"
