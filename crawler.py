from urllib.parse import urlparse
from urllib.error import HTTPError
from urllib.request import urlopen
from bs4 import BeautifulSoup
import random
import re

def getInternalLinks(bsObj, internalUrl):
    internalLinks = []
    for link in bsObj.findAll('a', href=re.compile('^\/|.*(http:\/\/'+internalUrl+')).*')):
        #still confused about how this regular expression work
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks

def getExternalLinks(bsObj, url):
    externalLinks = []
    externalUrl = getDomain(url)
    for link in bsObj.findAll('a', href=re.compile('^(http)((?!'+externalUrl+').)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks

def getDomain(address):
    #what does netloc do? cant figure out via googling it
    return urlparse(address).netloc

def followExternalOnly(bsObj, url):
    externalLinks = getExternalLinks(bsObj, url)
    #if no external links on the current page, go to a random internal link
    if len(externalLinks) == 0:
        print("sorry, no external link on this page, try again")
        internalLinks = getInternalLinks(bsObj, getDomain(url))
        randInternal = 'http://' + getDomain(url)
        randInternal += internalLinks[random.randint(0, len(internalLinks)-1)]#get url
        bsObj = BeautifulSoup(urlopen(randInternal), 'html.parser')
        followExternalOnly(bsObj, randInternal)
    #external links found in current page
    else:
        randExternalLink = externalLinks[random.randint(0, len(externalLinks)-1)]
        try:
            print("the random external link is: " + randExternalLink)
            #next round
            nextBsObject = BeautifulSoup(urlopen(randExternalLink), 'html.parser')
            followExternalOnly(nextBsObject, randExternalLink)
        #http error
        except HTTPError as e:
            print("error occurs at" + randExternalLink + "will try again")
            followExternalOnly(bsObj, url)#does not need to get a new external here cuz we will do it at the beginning of the function

#collect all the external links on a website
allExternalLinks = set()
allInternalLinks = set()
def getAllExternalLinks(siteUrl):
    html = urlopen(siteUrl)
    bsObj = BeautifulSoup(html, 'html.parser')
    internalLinks = getInternalLinks(bsObj, splitAddress(siteUrl[0]))
    externalLinks = getExternalLinks(bsObj, splitAddress(siteUrl[0]))
    for link in externalLinks:
        if link not in allExternalLinks:
            allExternalLinks.add(link)
            print(link)
    for link in internalLinks:
        if link not in allInternalLinks:
            allInternalLinks.add(link)
            print(link)
            getAllExternalLinks('http://' + getDomain(siteUrl) + link)#restart the app
url = "http://oreilly.com"
bsObj = BeautifulSoup(urlopen(url), 'html.parser')
followExternalOnly(bsObj, url)
getAllExternalLinks(url)
