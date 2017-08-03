import json
import os
from threading import Thread
from time import sleep


def pather(*args):
    return "/".join([arg for arg in args])

def init(path, name):
    try:
            os.stat(pather(path, name))
    except:
            os.mkdir(pather(path,name)) 

def write(key, value, path, name):
    with open(pather(path, name, key), 'w+') as page:
        page.write(json.dumps(value))
        print "written"

def _write(*args):
    t = Thread(target=thread_write, args=args)
    t.start()

def read(key, path, name):
    with open(pather(path, name, key), 'r') as page:
        return json.loads(page.read())

def remove(key, path, name):
    try:
       os.remove(pather(path, name, key))
    except:
       pass

