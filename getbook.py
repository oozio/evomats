#! /usr/bin/env python
import base64, random, sys
from flask import *
from lxml import html
import requests 
import urllib, cStringIO
from PIL import Image
import os 
from functions import *
from forms import *

info = []
page = requests.get('http://puzzledragonx.com/en/monsterbook.asp')
tree = html.fromstring(page.content)
f = open('searchbar.txt', 'a+')
f1 = open('monsterbook.txt','a+')

for i in range(3188,3977):
     stufff = "n="+str(i)
     stuff = tree.xpath('//div[@class ="indexframe"]//a[contains(@href,"%s")]/@href' % stufff)
     if stuff: 
          stuff = stuff[0]
    # print stuff
          stuff = stuff.split("=")[1]
    # print stuff
     
          info = getInfo(stuff)
          search = "{ value: "+str(info[1])[1:-1] + ", data: "+stuff + "},"
          print search   
          print info
          print >>f, search
          print >>f1, info
     
f.close()
f1.close()
print ' done'
          
