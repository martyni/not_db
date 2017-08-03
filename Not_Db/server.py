from flask_restful import Resource, Api
from flask import Flask, request
from not_db import not_db
import json
app = Flask(__name__)
@app.route('/')
def healthcheck():
    return 'ok'
api = Api(app)



class Base(Resource):
    Book = None 
    def not_found(self, thing):
        return None, 404 

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

    def create_book(self, db, *args, **kwargs):    
        self.Book = not_db(db, driver="s3")
        if self.Book.error:
            return self.Book.error


class List(Book):
     
    def get_list(self, list_name, db):
        if not self.Book:
            self.create_book(db)
        l = self.Book.get(list_name)
        return l if l else self.not_found(l)

    def get(self, list_name, db):
        return self.get_list(list_name, db)

    def put(self, list_name, db):
        l = self.get_list(list_name, db)
        if not l[0]:
            self.Book.set(list_name, [request.form['data']])
        else:
            self.Book.set(list_name, l + [request.form['data']])
        return self.Book.get(list_name)

    def post(self, *args, **kwargs):
        return self.put(*args, **kwargs)

    def delete(self, list_name, db):
        l = self.get_list(list_name, db)
        resp = 404 if l[-1] == 404 else 200
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
        return self.Book.get(list_name, db)[index]


    def put(self, index, list_name, db):
        list_, index_exist = self.index_fail(index, list_name, db)
        if not index_exist:
            return self.not_found(list_) 
        list_.insert(index, request.form['data'])
        self.Book.set(list_name, list_)
        return self.Book.get(list_name)

    def post(self, index, list_name, db):
        list_, index_exist = self.index_fail(index, list_name, db)
        if not index_exist:
            return self.not_found(list_) 
        list_[index] = request.form['data']
        self.Book.set(list_name, list_)
        return self.Book.get(list_name)

    def delete(self, index, list_name, db):
        list_, index_exist = self.index_fail(index, list_name, db)
        if not index_exist:
            return self.not_found(list_) 
        list_.pop(index)
        self.Book.set(list_name, list_)
        return self.Book.get(list_name)


api.add_resource(Item, '/<string:db>/list/<string:list_name>/<int:index>')
api.add_resource(List, '/<string:db>/list/<string:list_name>')
api.add_resource(Book, '/<string:db>')

def main():
   app.run(host="0.0.0.0")

if __name__ == '__main__':
   app.run(host="0.0.0.0", debug=True)
