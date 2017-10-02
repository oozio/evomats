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

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'),
                               'favicon.ico', mimetype='image/png')

@app.route("/", methods = ['GET', 'POST'])
@app.route('/index.html', methods = ["GET","POST"])
def index_page():
    form = idForm(request.form) 
    return render_template("/index.html", form = form)  

@app.route("/faq.html",methods=["GET"])
def faq_page():
     return render_template("/faq.html")


@app.route("/evomats.html", methods = ['GET','POST'])
def evomats_page():
    id = request.form.get('mons_id', None)
#   prev = prevEvos(id, [id])
#    print "prevvv" + str(prev)
#   mats = findmats(id, [id], [], 0)
#    mats = collect_mats(id, [], [id],[],[], 0,[],[])
    mats,pictures = collectmats(id,[id,'break'],[id],[id,'break'])
    iconURL = []
    names = []
    print 'getting pics'

    for n in pictures:
        info = getInfo(n)
        if n in mats:
          names.append(info[1])
        iconURL.append(info[0])
    names[:] = [x[2:-2] for x in names]

    occur = [[str(x),names.count(x)] for x in set(names) if x != 'e']
     
    occur.sort(key=lambda tup: tup[0])
  #  print 'sorted'+str(occur)
    occur = [item for sublist in occur for item in sublist]
  #  print 'ocur' + str(occur)
 #   occur.sort(key=lambda tup: tup[1])
    return render_template("/evomats.html", iconURLs = iconURL[:-1], names = occur, name = getInfo(id)[1][2:-2])
if __name__ == "__main__":
    sys.stderr.write("Ready.\n");
    app.debug = True
    app.run()

