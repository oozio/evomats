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
app = Flask(__name__)

@app.route("/", methods = ['GET', 'POST'])
@app.route('/index.html', methods = ["GET","POST"])
def index_page():
    form = idForm(request.form) 
    return render_template("/index.html", form = form)  

@app.route("/evomats.html", methods = ['GET','POST'])
def evomats_page():
    id = request.form.get('mons_id', None)
#   prev = prevEvos(id, [id])
#    print "prevvv" + str(prev)
#   mats = findmats(id, [id], [], 0)
    mats = collect_mats(id, [], [id],[],[], 0)
    iconURL = []
    names = []
    for n in mats:
        if n:
             print 'getting images'+n
             tree = getTree(n)
             print "getting tree"
             #print "avatar url?" + str(tree.xpath('//div[@class = "avatar"]/img/@src'))
             iconURL.append("http://www.puzzledragonx.com/en/"+ str(tree.xpath('//div[@class = "avatar"]/img/@src')[0]))
             names.append(str(tree.xpath('//div[@class="name"]/h1/text()')))
    print iconURL
    print names
    names = flatten(names)
    return render_template("/evomats.html", iconURLs = iconURL, names = names)
if __name__ == "__main__":
    sys.stderr.write("Ready.\n");
    app.debug = True
    app.run()

