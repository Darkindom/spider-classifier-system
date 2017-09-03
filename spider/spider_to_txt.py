# coding=utf-8
import re
import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
page = 1
file_url_path = '/Users/darkindom/Desktop/spidder/spider_txt/url_'
file_data_path = '/Users/darkindom/Desktop/spidder/spider_txt/data_'
file_keywords_path = '/Users/darkindom/Desktop/spidder/spider/keywords.txt'

# with open(file_data_path, "w") as f_data
def getKeywords():
    with open(file_keywords_path, "r") as f_keywords:
        keywords = f_keywords.readlines()
        f_keywords.close()
    return keywords

def getUrls(keyword):
    f_url = open(file_url_path + keyword + '.txt', "r")
    urls = f_url.readlines()
    f_url.close()
    return urls

def searchUrls(keyword):
    f_url = open(file_url_path + keyword + '.txt', "w")
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

def searchItem(keyword, urls):
    f_data = open(file_data_path + keyword + '.txt', "w")
    for url in urls:
        r_data = requests.get(url, headers = headers)
        content = r_data.text
        soup = BeautifulSoup(content, 'lxml')

        title = soup.find(class_ = 'aca_title')
        results = soup.find_all(class_ = 'aca_content')

        try:
            if results[1].div.span.span != None:
                print '\n\n---- title ----\n', title.get_text(),'\n'
                f_data.write('title\n' + title.get_text() + '\n')
                f_data.write('url\n' + url)

                for i,result in enumerate(results):
                    # print i,result
                    if i == 0:
                        authors = result.div.span.find_all('a')
                        print '---- authors ----'
                        f_data.write('authors\n')
                        for author in authors:
                            print author.get_text()
                            f_data.write(author.get_text())
                        f_data.write('\n')
                    if i == 1:
                        abstract = result.div.span.span
                        print '---- abstract ----\n',abstract,'\n'
                        f_data.write('abstract\n')
                        f_data.write(str(abstract) + '\n')
                    if i == 2:
                        fields = result.find_all(class_ = 'aca_badge')
                        print '---- fields ----'
                        f_data.write('fields\n')
                        for field in fields:
                            print field.a.get_text()
                            f_data.write(field.a.get_text() + '\n')
                        print '------------------------------------------------------------------------------------------\n'
                        f_data.write('\n')
            else:
                continue
        except:
            continue
    f_data.close()

print "start"
keywords = getKeywords()
for keyword in keywords:
    print 'search for ' + keyword
    searchUrls(keyword)
    urls = getUrls(keyword)
    searchItem(keyword, urls)
