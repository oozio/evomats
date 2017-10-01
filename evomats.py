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

from rq import Queue
from redis import Redis

# Tell RQ what Redis connection to use
redis_conn = Redis()
q = Queue(connection=redis_conn)  # no args implies the default queue

# Delay execution of count_words_at_url('http://nvie.com')
q.enqueue_call(func=collectmats,args=('http://www.puzzledragonx.com',),timeout=300)



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
    mats = collectmats(id,[])
    iconURL = []
    names = []
    print 'getting pics'
    for n in mats:
        if n:
          #print 'n'+ str(n)
          names.append(getInfo(n)[1])
          iconURL.append(getInfo(n)[0])
  #  print iconURL
    names[:] = [x[2:-2] for x in names]
   
   # print 'wtf'+str(names)
    occur = [[str(x),names.count(x)] for x in set(names)]
    occur = [item for sublist in occur for item in sublist]     
   # print 'ocur' + str(occur)
    return render_template("/evomats.html", iconURLs = iconURL, names = occur)
if __name__ == "__main__":
    sys.stderr.write("Ready.\n");
    app.debug = True
    app.run()

