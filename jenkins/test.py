import requests
import sys
import json
print "url: " + sys.argv[1]
base_url = sys.argv[1]

def get(path, payload=None):
    req = requests.get(base_url + path)
    if req and not payload:
        print "success: {}".format(base_url + path) 
        return 1
    elif req and payload:
        if payload not in req.text:
            print "fail: {}".format(base_url + path)
            print "{} not in {}".format(payload, req.text)
            return 0
        else:    
            print "success: {}".format(base_url + path) 
            return 1
    else:
        print "fail: {}".format(base_url + path)
        return 0

def put(path, payload):
    if requests.put(base_url + path, data="data=" + json.dumps(payload)):
        print "success: {}".format(base_url + path)
        return 1
    else:
        print "fail: {}".format(base_url + path)
        return 0

def delete(path):
    if requests.delete(base_url + path):
        print "success: {}".format(base_url + path)
        return 1
    else:
        print "fail: {}".format(base_url + path)

def serializable(path):
    try:
        requests.get(base_url + path).json()
        print "serializable: {}".format(base_url + path)
        return 1
    except:
        print "not serializable: {}".format(base_url + path)
        return 0

def check_this_errors(path):
    if not requests.get(base_url + path):
        print "errors: {}".format(base_url + path)
        return 0
    else:
        print "no errors: {}".format(base_url + path)
        return 1
paths = ["aklsdjhfalkjsdfhlakjhdsfl"]
lists = ["dave"]
complete_paths = ["/{}/list/{}".format(path, list_) for path in paths for list_ in lists ]

for path in complete_paths:
    if not put(path, "hi"):
        sys.exit(1)

for path in complete_paths:
    if not get(path, "hi"):
        sys.exit(1)

for path in paths:
    if not delete("/" + path):
        sys.exit(1)

'''
for path in [""]:
    if not serializable(path):
        sys.exit(1)

for path in [""]:
    if serializable(path):
        sys.exit(1)

for path in ["", "", ""]:
    if check_this_errors(path):
        sys.exit(1)

for path in [""]:
    if test_path(path):
        sys.exit(1)
'''        
