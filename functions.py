from lxml import html
import requests 
import urllib, cStringIO
from PIL import Image
import os 
import collections
from profilestats import profile

#@profile(print_stats=10, sort_stats='time')
def weekday():
     page = requests.get('http://www.puzzledragonx.com/en/monsterbook.asp?t1=7&ue=0&s1=1&s2=1&o1=1&o2=1&o3=1&t=1')
     tree = html.fromstring(page.content)
     weekdays = tree.xpath('//div[@class ="indexframe"]//a/@href')
     for i in range(0, len(weekdays)):
               weekdays[i] = [(s) for s in weekdays[i].split("=") if s.isdigit()]
               
     weekdays = [y for x in weekdays for y in x]
     return weekdays

global weekdays 
weekdays = weekday()

global infos
infos = {'break':['break', 'break']}
def getInfo(id):
     key = id
     picture = ''
     name = ''
     if id.isdigit():
          key = '/'+str(id)+'.png'
     if key == 'break':
          return['break','break']
     else:
#     info = infos.get(str(id))
 #    if not info:
  #        tree = getTree(id)
   #       iconURL = "http://www.puzzledragonx.com/en/"+ str(tree.xpath('//div[@class = "avatar"]/img/@src')[0])
    #      name = str(tree.xpath('//div[@class="name"]/h1/text()'))
     #     info = [iconURL,name]
      #    infos[str(id)] = info
          with open("monsterbook.txt") as f:
               for line in f:
                    if key in line and ', "[' in line:
                         name = line.split(', "[')[1][1:-5]
                         picture = line.split(', "[')[0][2:-1]
                    elif key in line and ", '[" in line:
                         name = line.split(", '[")[1][1:-5]
                         picture = line.split(", '[")[0][2:-1]
     return [picture,name]


#@profile(print_stats=10, sort_stats='time')
def enhancemats():
     page = requests.get('http://puzzledragonx.com/en/monsterbook.asp?t1=8&ue=0&s1=1&s2=1&o1=1&o2=1&o3=1')
     tree = html.fromstring(page.content)
     enhancemats = tree.xpath('//div[@class ="indexframe"]//a/@href')
     for i in range(0, len(enhancemats)):
               enhancemats[i] = [(s) for s in enhancemats[i].split("=") if s.isdigit()]
               
     enhancemats = [y for x in enhancemats for y in x]     
     return enhancemats
     
global enhances
enhances = enhancemats()

global trees
trees = {}

#@profile(print_stats=10, sort_stats='time')
def getTree(id):
     if id.isdigit():
          id = str(id)
     
     tree = trees.get(id)
     if not tree:
          url0 = "http://www.puzzledragonx.com/en/monster.asp?n="
          url = url0 + id
          
          page = requests.get(url)
          tree = html.fromstring(page.content) 
          trees[id] = tree  
     return tree 

#@profile(print_stats=10, sort_stats='time')
def flatten(aList):
    t = []
    for i in aList:
        if not isinstance(i, list):
             t.append(i)
        else:
             t.extend(flatten(i))
    return t

#@profile(print_stats=10, sort_stats='time')
def prevEvos(id, prev,tree):
     
     arrow_left = []
     arrow_left_awokens = []
     arrow_right = []
     arrow_away = []
     arrow_new_awoken = []
     
#     # print "begin prev" + str(prev) + "id" + str(id)
     possible_left = "img/evolvearrow2.png" # a straigt line???
     possible_left_awoken = "img/evolvearrow8.png" #yellow pointing to the right from the left
     possible_left_awoken_1 = "img/evolvearrow9.png" #same 
     possible_new_awoken = 'img/evolvearrow10.png'
     possible_right = "img/evolvearrow7.png" #kinked L arrow to the left from the right
     possible_right_1 = "img/evolvearrow6.png" #arrow in the middle of a line              

     o = len(tree.xpath('//div[@class = "evolveframe"]/img[contains(@src,stuff)]/ancestor::td[@class = "evolve"]/preceding-sibling::td[@class = "evolve"]'))
   #  print ' prev oo' + str(o)

     arrow_left = tree.xpath('//div[@class = "evolveframe"]/img[contains(@src, id)]/ancestor::td[@class = "evolve"]/preceding-sibling::td[position()=1]/descendant::img/@data-original')
   #  print "arrow left"+str(arrow_left)
     
     arrow_left_awokens =  tree.xpath('//div[@class = "evolveframe"]/img[contains(@src, id)]/ancestor::td[@colspan = 2]/preceding-sibling::td[position()=1]/descendant::img/@data-original')
    # print "arrow left a"+str(arrow_left_awokens)


     arrow_right = tree.xpath('//div[@class = "evolveframe"]/img[contains(@src, id)]/ancestor::td[@class = "evolve"]/following::td[position()=1]/div[@class = "arrowspace2"]/*/@data-original')
     #print "arrow right"+str(arrow_right)

     arrow_new_awoken = tree.xpath('//div[@class = "evolveframe"]/img[contains(@src, id)]/ancestor::td[@colspan = 2]/descendant::td[position()=1]/descendant::img/@data-original')
     #print 'arrow new awoken' + str(arrow_new_awoken)
     
     
     
     
     arrow_away = tree.xpath('//div[@class = "evolveframe"]/descendant::img[contains(@src, id)]/ancestor::td[@class ="evolve"]/following-sibling::td[position()=1]/descendant::div[contains(@class, "arrow")]/child::*/@data-original')
     #print "arrow away"+str(arrow_away)
     
     if possible_new_awoken in arrow_new_awoken:
        #  print 'YES'    
          name_new_awoken = tree.xpath('//div[@class = "evolveframe"]/img[contains(@src, id)]/ancestor::td[@colspan = 2]/parent::tr/preceding-sibling::tr[position()=1]/descendant::img/@data-original')
          id_new_awoken = str(''.join(list(filter(str.isdigit, name_new_awoken[0]))))
          prev.append(id_new_awoken)
     
     elif possible_left in arrow_left:
          name_left = tree.xpath('//div[@class = "evolveframe"]/descendant::img[contains(@src, id)]/ancestor::td[@class = "evolve"]/preceding-sibling::td[position()=2]/descendant::img/@data-original')
          id_left = str(''.join(list(filter(str.isdigit, name_left[o-1])))) 
      #    print "name left"+id_left
          prev.append(id_left)
          #return prevEvos(id_left, prev)
     elif possible_left_awoken in arrow_left_awokens: 
          name_awoken = tree.xpath('//div[contains(@class, "arrow")]/img[contains(@data-original, "arrow8")]/ancestor::div[@class = "arrowspace2"]/../preceding-sibling::td[position()=1]/div[@class = "evolveframe"]/descendant::*/@data-original')
          id_awoken = str(''.join(list(filter(str.isdigit, name_awoken[0]))))
        #  print "name awoken"+id_awoken
          prev.append(id_awoken)
       #   return prevEvos(id_awoken, prev)
     elif possible_left_awoken_1 in arrow_left_awokens:
          name_awoken = tree.xpath('//div[contains(@class, "arrow")]/img[contains(@data-original, "arrow9")]/ancestor::div[@class = "arrowspace2"]/../preceding-sibling::td[position()=1]/div[@class = "evolveframe"]/descendant::*/@data-original')
          id_awoken = str(''.join(list(filter(str.isdigit, name_awoken[0]))))
      #    print "name awoken"+id_awoken
          prev.append(id_awoken)
       #   return prevEvos(id_awoken, prev)

     elif possible_right in arrow_right or possible_right_1 in arrow_right:
          name_right = tree.xpath('//div[contains(@class, "arrow")]/img[contains(@data-original, "arrow4")]/ancestor::div[@class = "arrowspace2"]/../preceding-sibling::td[position()=1]/div[@class = "evolveframe"]/descendant::*/@data-original')
          id_right = str(''.join(list(filter(str.isdigit, name_right[0]))))
       #   print "name right"+id_right    
          prev.append(id_right)
      #    return prevEvos(id_right, prev)
     
     
     
     #else:
        #  # print "end prev" + str(prev) 
       #   # print ""
     return prev

#@profile(print_stats=10, sort_stats='time')
def findmats(id,tree):
     ## print "finding mats"
   #  # print "got tree in findmats"
     if id.isdigit():
          id = str(id)
     stuff = "/"+id+"."
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

#@profile(print_stats=10, sort_stats='time')
def collectmats(id,final,hasmore,pictures,bases):
     tree = getTree(id)
     
     
     temp = findmats(id,tree)
     prev = prevEvos(id, [],tree)
 #    print 'prev' + str(prev)
     temp.append(prev)
     
     if len(temp) > 1:
          pictures.append(id)
     
     temp = flatten(temp)
     final.append(temp)
     final = flatten(final)
     pictures.append(temp)
     pictures = flatten(pictures)
     
     if not temp:
          pictures.append('break')
          bases.append(id)

     for each in temp:
          if each not in enhances and each not in weekdays:
               hasmore.append(id)
               hasmore = flatten(hasmore)
               pictures.append('break')
               final,pictures,bases =  collectmats(each,final,hasmore,pictures,bases)
          
  
     final = [x for x in final if x not in hasmore]
     final = flatten(final)
     pictures = flatten(pictures)
     bases = flatten(bases)
 
     return [final,pictures,bases]

     
