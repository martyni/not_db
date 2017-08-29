import requests
import sys
import json
print "url: " + sys.argv[1]
base_url = sys.argv[1]

def test_path(path):
    if requests.get(base_url + path):
        print "success: {}".format(base_url + path) 
        return 1
    else:
        print "fail: {}".format(base_url + path)
        return 0

def put(path, payload)
    if requests.put(base_url + path, data=json.dumps(payload)):
        print "success: {}".format(base_url + path)
        return 1
    else:
        print "fail: {}".format(base_url + path)
        return 0

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

for path in ["/aklsdjhfalkjsdfhlakjhdsfl/list/dave"]:
    if not put(path, "hi"):
        sys.exit(1)

for path in ["/aklsdjhfalkjsdfhlakjhdsfl/list/dave"]:
    if not get(path):
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
