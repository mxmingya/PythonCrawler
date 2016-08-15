from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")
bsObj = BeautifulSoup(html, "html.parser")

"""nameList = bsObj.findAll("span", {"class":"green"})###(word, attribute)
for name in nameList:
    print(name)
print(len(nameList))
"""

"""
alltext = bsObj.findAll(id='title', class_='text')
for t in alltext:
    print(t)
"""

"""
print(bsObj.find('img',{'src':'../img/gifts/img1.jpg'
                           }).parent.previous_sibling.get_text())
"""

###images
'''
images = bsObj.findAll('img', {'src':re.compile('\.\.\/img\/gifts/img.*\.jpg')})
for image in images:
    print(image['src'])
'''
###links
for link in bsObj.find('div', {'id':'bodyContent'}).findAll('a', href=re.compile('^(/wiki/)((?!:).)*$')):
    if 'href' in link.attrs:
        print(link.attrs['href'])
