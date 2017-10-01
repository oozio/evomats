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
#    mats = collect_mats(id, [], [id],[],[], 0,[],[])
    mats,pictures = collectmats(id,[id],[],[id])
    iconURL = []
    names = []
    print 'getting pics'

    for n in pictures:
        info = getInfo(n)
        if n in mats:
          names.append(info[1])
        iconURL.append(info[0])
    names[:] = [x[2:-2] for x in names]
   
   # print 'wtf'+str(names)
    occur = [[str(x),names.count(x)] for x in set(names) if x != 'e']
    occur = [item for sublist in occur for item in sublist]     
   # print 'ocur' + str(occur)
    return render_template("/evomats.html", iconURLs = iconURL, names = occur)
if __name__ == "__main__":
    sys.stderr.write("Ready.\n");
    app.debug = True
    app.run()

