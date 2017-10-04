#! /usr/bin/env python
import base64, random, sys
from flask import *
from lxml import html
import requests 
import urllib, cStringIO
from PIL import Image
import os 
#from functions import *
from forms import *
import pickle

f = open('trees.txt', 'a+')
#f1 = open('monsterbook.txt','a+')

#for i in range(3188,3977):
 #    stufff = "n="+str(i)
  #   stuff = tree.xpath('//div[@class ="indexframe"]//a[contains(@href,"%s")]/@href' % stufff)
   #  if stuff: 
    #      stuff = stuff[0]
    # print stuff
     #     stuff = stuff.split("=")[1]
    # print stuff
     
      #    info = getInfo(stuff)
       #   search = "{ value: "+str(info[1])[1:-1] + ", data: "+stuff + "},"
        #  print search   
         # print info
          #print >>f, search
          #print >>f1, info
def findmats(id,tree):
     ## print "finding mats"
   #  # print "got tree in findmats"
     stuff = "/"+str(id)+"."
     o = len(tree.xpath('//div[@class = "evolveframe"]/img[contains(@src,stuff)]/ancestor::td[@class = "evolve"]/preceding-sibling::td[@class = "evolve"]'))
  #   # print 'oo' + str(o)
     evomats = tree.xpath('//div[@class = "evolveframe"]/img[contains(@src, stuff)]/ancestor::td[@class = "evolve"]/preceding-sibling::*[position()=1]//a/@href')
   #  # print 'first' + str(evomats)
     if not evomats:
          evomats = tree.xpath('//div[@class = "evolveframe"]/img[contains(@src, stuff)]/ancestor::td[@class = "awokenevolve"]/following-sibling::td[position()=1]//a/@href')

   #       # print 'here' + str(evomats)

     if (o > 0) and not evomats:
          evomats = tree.xpath('//div[@class = "evolveframe"]/img[contains(@src, stuff)]/ancestor::td[@class = "evolve"]/../following-sibling::*[position()=1]/td[@colspan = 2 and position() = "%d"]//a/@href' % o)
    #      # print 'whatthe heck' + str(evomats)


     if (o > 0) and not evomats:
          evomats = tree.xpath('//div[@class = "evolveframe"]/img[contains(@src, stuff)]/ancestor::td[@class = "evolve"]/../following-sibling::*[position()=1]/td[@colspan = 2]//a/@href')
     #     # print 'hereee' + str(evomats)

#     # print "evomats begin" + str(evomats) 
   
     for j in range(0, len(evomats)):
          evomats[j] = [(s) for s in evomats[j].split("=") if s.isdigit()]
     evomats = flatten(evomats)  

#     # print "evomats " + str(evomats)
#     for evomat in evomats:
#          if evomat not in seen and evomat not in enhances and evomat not in weekdays:
#               seen.append(evomat)
#               mats.append(evomat)
#          else:
#               mats.append(evomat)
 
#     # print "seen" + str(seen)

#     # print "Mats" + str(mats)

#    if i == len(seen)-1: 
#          return mats
#     return findmats(seen[i+1], seen, mats, i+1)
     return evomats
global trees
trees = {'hello':'bye'}
#@profile(print_stats=10, sort_stats='time')
def getTree(id):
     tree = trees.get(str(id))
     if not tree:
          url0 = "http://www.puzzledragonx.com/en/monster.asp?n="
          url = url0 + str(id)
          
          page = requests.get(url)
          tree = html.fromstring(page.content) 
          trees[str(id)] = tree  
     return tree 


for i in range(1,3):
     tree=getTree(i)
     print i    
     
print trees
     
#a = {'hello': 'world'}

#with open('trees.txt', 'wb') as handle:
 #   pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)

#with open('trees.txt', 'rb') as handle:
 #   b = pickle.load(handle)

#print a == b
     
with open("trees.txt", "wb") as fp:   #Pickling
   pickle.dump(trees, fp)
#3977
for i in range(1,3):
     tree=getTree(i)
     print type (tree)
     print tree
     print >>f, tree
     print i
         
with open('trees.txt', 'rb') as handle:
    b = pickle.load(handle)

print type(trees)

print type(b)
t = b.get('1')
print findmat(1,t)
          
f.close()
#f1.close()
print ' done'
          
