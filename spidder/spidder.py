import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
r = requests.get('http://www.bing.com/academic/profile?id=e8c3f26473f3e260b3ca25322b7abf86&encoded=0&v=paper_preview&mkt=zh-cn&setmkt=zh-CN', headers = headers)

content = r.text
# print content
soup = BeautifulSoup(content, 'lxml')
title = soup.find(class_ = 'aca_title')
results = soup.find_all(class_ = 'aca_content')
# authors = soup.find_all(class_ = 'caption_author')
# venues = soup.find_all(class_ = 'caption_venue')
# field = soup.find_all(class_ = 'caption_field')

# for result in results:
#     # abstract = result.find(class_ = 'caption_abstract').p.get_text()
#     authors = result.span.a.get_text()
#     abstract =result.span.span

print 'title',title.get_text(),'\n'
for i,result in enumerate(results):
    # print i,result
    if i == 0:
        authors = result.div.span.find_all('a')
        print 'authors'
        for author in authors:
            print author.get_text()
        print '\n'
    if i == 1:
        abstract = result.div.span
        print 'abstract',abstract,'\n'
    if i == 2:
        fields = result.find_all(class_ = 'aca_badge')
        print 'fields'
        for field in fields:
            print field.a.get_text()
        print '\n'
