from flask_restful import Resource, Api
from flask import Flask, request, render_template, redirect
from not_db import not_db
from botocore.exceptions import ParamValidationError
import json
import re
import urlparse
from pprint import pprint
app = Flask(__name__)
#cors = CORS(app, resources={r"/*": {"origins": "*martyni.co.uk"}})
api = Api(app)

@app.route('/')
def healthcheck():
    referrer = request.args.get('refer')
    if referrer:
        return render_template("base.html", referrer=referrer)
    else:
        return render_template("base.html", referrer=request.referrer)

class Base(Resource):

    Book = None 
    url = None
    def not_found(self, thing):
        return None, 404 

    def process_url(self):
        url = urlparse.urlparse(self.url)
        self.protocol = url.scheme + "://"
        self.domain = url.hostname
        self.port = ":" + str(url.port) or ''

    def extract_json(self, blob):
        try:
            return json.loads(blob)
        except:
            try:
               blob = blob.replace("'",'"')
               return json.loads(blob)
            except:
               return blob 

    def parse_request(self, request):
        def json_fail():
           data_string = request.form.get('data')
           pprint(request.__dict__)
           if not data_string and str(data_string) is not '':
               data_string = request.get_data().split('data=')[-1]
           return self.extract_json(data_string)
        try:
           ob = request.json
           return ob if ob else json_fail()
        except:
           return json_fail()

class Book(Base):
    def get(self, db):
        self.create_book(db)

    def post(self, db):
        self.create_book(db)

    def put(self, db):
        self.create_book(db)

    def delete(self, db):
        self.create_book(db)
        self.Book.drop()
        return None, 204

    def create_book(self, db, *args, **kwargs):    
        if not self.Book:
           self.Book = not_db(db, driver="s3")
           self.url = request.url
           self.process_url()
        if self.Book.error:
            return self.Book.error


class List(Book):
    def get_list(self, list_name, db):
        if not self.Book:
            self.create_book(db)
        l = self.Book.get_contents(list_name)
        return l if l else self.not_found(l)

    def get(self, list_name, db):
        return self.get_list(list_name, db)

    def put(self, list_name, db):
        l = self.get_list(list_name, db)
        thing = Thing()
        data = self.parse_request(request)
        print data
        if not l[0]:
            thing_name = list_name + ".0"
            thing_path = "/" + db + "/thing/" + thing_name
            thing.put(thing_name, db, data=data)
            self.Book.set(list_name, [thing_path])
        else:
            list_size = len(l)
            thing_name = list_name + ".{}".format(list_size)
            thing_path = "/" + db + "/thing/" + thing_name
            thing.put(thing_name, db, data=data)
            self.Book.set(list_name, l + [thing_path])
        return self.Book.get_contents(list_name)

    def post(self, *args, **kwargs):
        return self.put(*args, **kwargs)

    def delete(self, list_name, db):
        l = self.get_list(list_name, db)
        resp = 404 if l[-1] == 404 else 204
        self.Book.remove(list_name)
        return None, resp 


class Item(List):

    def index_fail(self, index, list_name, db):
        list_ = self.get_list(list_name, db)
        try:
            list_[index]
            return (list_, True)
        except:
            return (list_, False)

    def get(self, index, list_name, db):
        list_, index_exist = self.index_fail(index, list_name, db) 
        if not index_exist:
            return self.not_found(list_) 
        return redirect(list_[index], 301)


    def put(self, index, list_name, db):
        list_, index_exist = self.index_fail(index, list_name, db)
        thing = Thing()
        if not index_exist:
            return self.not_found(list_) 
        thing.put(list_name + ".{}".format(index), db, data=self.parse_request(request))
        return self.Book.get_contents(list_name)

    def post(self, *args, **kwargs):
        return self.put(*args, **kwargs)

    def delete(self, index, list_name, db):
        list_, index_exist = self.index_fail(index, list_name, db)
        if not index_exist:
            return self.not_found(list_) 
        list_.pop(index)
        self.Book.set(list_name, list_)
        return self.Book.get_contents(list_name), 204

class File(Book):
    def get(self, file_name,  db):
        if not self.Book:
            self.create_book(db)
        return self.Book.get_contents(file_name, raw=True)

    def put(self, db, file_name=None):
        if not self.Book:
            self.create_book(db)
        try:
           for file_ in request.files:
               if file_name is None:
                  file_name = request.files[file_].filename
                  self.Book.raw_set(file_name, request.files[file_].read())
               else:    
                  self.Book.raw_set(file_name, request.files[file_].read())
        except ParamValidationError:
            return None, 400
        return "{}/{}".format(request.url, file_name)

    def post(self, db, file_name=None):
        if not self.Book:
            self.create_book(db)
        if self.Book.error and "BucketAlreadyOwnedByYou" not in str(self.Book.error):
            return str(self.Book.error), 401
        try:
           for file_ in request.files:
               if file_name is None:
                  file_name = request.files[file_].filename
                  self.Book.raw_set(file_name, request.files[file_].read())
               else:    
                  self.Book.raw_set(file_name, request.files[file_].read())
        except ParamValidationError:
            return None, 400
        referrer = request.referrer.split("?")[0].replace(self.protocol + self.domain + self.port, "")
        match = re.match(r"^(/prod|/stge|/dev)(/.*/file/.*$)", request.path)
        if match:
            path = match.group(2)
        else:
            path = request.path
        return  redirect("{}?refer={}".format(referrer, path), code=302)

    def delete(self, file_name, db):
        l = self.get_list(list_name, db)
        resp = 404 if l[-1] == 404 else 204
        self.Book.remove(list_name)
        return None, resp

class Linked_List(List):

    def put(self, list_name, db):
        l = self.get_list(list_name, db)
        data = self.parse_request(request)
        print "this is the data  ", data
        print type(data)
        if type(data) == str or type(data) == unicode:
            thing_path = data
        elif data.get('link'):
            thing_path = data['link']
        if not l[0]:
            self.Book.set(list_name, [thing_path])
        else:
            self.Book.set(list_name, l + [thing_path])
        return self.Book.get_contents(list_name)

class Thing(Book):
    def get_thing(self, thing_name, db):
        if not self.Book:
            self.create_book(db)
        l = self.Book.get_contents(thing_name)
        return l if l else self.not_found(l)

    def get(self, thing_name, db):
        return self.get_thing(thing_name, db)

    def put(self, thing_name, db, data=None):
        d = self.get_thing(thing_name, db)
        if not data:
            data=self.parse_request(request)
        print "I'm going to create thing {thing} in db {db} with contents {contents}".format(
                thing=thing_name,
                db=db,
                contents=data
                )
        self.Book.set(thing_name, data)
        return self.Book.get_contents(thing_name)

    def post(self, *args, **kwargs):
        return self.put(*args, **kwargs)

    def delete(self, thing_name, db):
        l = self.get_thing(thing_name, db)
        resp = 404 if l[-1] == 404 else 204
        self.Book.remove(thing_name)
        return None, resp

class File_Auto_Name(File):
    pass

api.add_resource(Item, '/<string:db>/list/<string:list_name>/<int:index>')
api.add_resource(List, '/<string:db>/list/<string:list_name>')
api.add_resource(Linked_List, '/<string:db>/link/<string:list_name>')
api.add_resource(Thing, '/<string:db>/thing/<string:thing_name>')
api.add_resource(File, '/<string:db>/file/<string:file_name>')
api.add_resource(File_Auto_Name, '/<string:db>/file/')
api.add_resource(Book, '/<string:db>')

@app.after_request
def after_request(response):
    search = None
    if request.__dict__['environ'].get('HTTP_REFERER'):
       search = re.search(r'(http(s)?://)(.*\.martyni.co.uk)(:5000)?(.*)', request.__dict__['environ']['HTTP_REFERER'])
    if search:
       if search.group(4):
           cors = search.group(1) + search.group(3) + search.group(4)
       else:
           cors = search.group(1) + search.group(3)
       response.headers.add('Access-Control-Allow-Origin', cors)
       response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
       response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

def main():
   app.run(host="0.0.0.0", debug=False)

if __name__ == '__main__':
   app.run(host="0.0.0.0", debug=True)
