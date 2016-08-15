from urllib.request import urlopen
from bs4 import BeautifulSoup
import random
import re
import datetime

random.seed(datetime.datetime.now())
def getLinks(articleURL):
    html = urlopen('http://en.wikipedia.org' + articleURL)
    bsObj = BeautifulSoup(html,'html.parser')
    return bsObj.find('div', {'id':'bodyContent'}).findAll('a', href=re.compile('^(/wiki/)((?!:).)*$'))

pages = set()
def getLinks_f(pageUrl):
    global pages
    html = urlopen('http://en.wikipedia.org'+pageUrl)
    ###shit is a beautifulsoup object
    bsObj = BeautifulSoup(html,'html.parser')
    ###parsing
    for link in bsObj.findAll('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:###when we counter a fucking new page
                new_page = link.attrs['href']
                print(new_page)
                pages.add(new_page)
                getLinks_f(new_page)
getLinks_f("") #open with the Wikipedia home page as the first page

''' this will get all the article links in the page
links = getLinks("/wiki/Kevin_Bacon")
while len(links)<0:
    newArticle = links[random.randint(0,len(links)-1)].attrs['href']
    print(newArticle)
    links = getLinks(newArticle)
'''
