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
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'),'favicon.ico', mimetype='image/png')
    
@app.route('/style.css')
def style():
    return send_from_directory(os.path.join(app.root_path, 'templates'),'style.css')
    
@app.route('/jquery-1.9.1.min.js')
def jsmin():
    return send_from_directory(os.path.join(app.root_path, 'templates','js'),'jquery-1.9.1.min.js')
    
@app.route('/jquery.autocomplete.min.js')
def jsauto():
    return send_from_directory(os.path.join(app.root_path, 'templates','js'),'jquery.autocomplete.min.js')
    
@app.route('/monster-autocomplete.js')
def monsters():
    return send_from_directory(os.path.join(app.root_path, 'templates','js'),'monster-autocomplete.js')
    
@app.route('/error.html')
def error():
      return render_template("/error.html")                  
      
@app.route("/", methods = ['GET', 'POST'])
@app.route('/index.html', methods = ["GET","POST"])
def index_page():
     form = idForm(request.form) 
     return render_template("/index.html", form = form)  
 #    return render_template("/index.html")
     
@app.route("/faq.html",methods=["GET"])
def faq_page():
     return render_template("/faq.html")


@app.route("/evomats.html", methods = ['GET','POST'])
def evomats_page():
    id = request.form.get('monster')
    #print str(id)+"dd"
#   prev = prevEvos(id, [id])
#    print "prevvv" + str(prev)
#   mats = findmats(id, [id], [], 0)
#    mats = collect_mats(id, [], [id],[],[], 0,[],[])
    mats,pictures,bases = collectmats(id,[id,'break'],[id],[id,'break'],[])
    iconURL = []
    names = []
    basenames = []
  #  print 'getting pics'
   # print 'start'+str(os.times())
    for n in pictures:
        info = getInfo(n)
        if n in mats:
          names.append(info[1])
        iconURL.append(info[0])
    for n in bases:
        info = getInfo(n)
        basenames.append(info[0])
    basenames = flatten(basenames)
      #  print info[0]
      #  print info[1]
    occur = [[str(x),names.count(x)] for x in set(names) if x != 'break']
     
    occur.sort(key=lambda tup: tup[0])
  #  print 'sorted'+str(occur)
    occur = [item for sublist in occur for item in sublist]
   # print 'end'+str(os.times())
 #   print basenames
  #  print 'ocur' + str(occur)
 #   occur.sort(key=lambda tup: tup[1])
    return render_template("/evomats.html", iconURLs = iconURL[:-1], names = occur, name = getInfo(id)[1],bases = bases)
if __name__ == "__main__":
 #   sys.stderr.write("Ready.\n");
    app.debug = False
    app.run()

