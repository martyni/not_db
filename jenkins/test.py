import requests
import sys
import json
import random
import string
print "url: " + sys.argv[1]
base_url = sys.argv[1]

def random_string(n):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(n))

def get(path, payload=None):
    req = requests.get(base_url + path, allow_redirects=True)
    print req.text
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
    req = requests.put(base_url + path, headers={'content-type': 'application/json'}, data=json.dumps(payload))
    print req.text
    if req:
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

def get_json(path):
    try:
        return requests.get(base_url + path).json()
    except:
        return 0

def check_this_errors(path):
    if not requests.get(base_url + path):
        print "errors: {}".format(base_url + path)
        return 0
    else:
        print "no errors: {}".format(base_url + path)
        return 1
paths = [random_string(12)]
lists = ["dave"]
complete_paths = ["/{}/thing/{}".format(path, list_) for path in paths for list_ in lists ]

# Put item in list
for path in complete_paths:
    if not put(path, "hi"):
        sys.exit(1)

# Check its there
for path in complete_paths:
    if not get(path, "hi"):
        sys.exit(1)


# Put random data in list and check its there
for path in complete_paths:
    my_string = random_string(4)
    put(path, my_string)
    my_string_2 = random_string(5)
    put(path, my_string_2)
    serializable(path)
    payload = get_json(path)
    if payload:
        if my_string in payload and my_string_2 in payload:
            print "payload contains: {} {}".format(my_string, my_string_2), payload
        else:
            sys.exit(1)
    else:
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
