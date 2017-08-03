import fs
import s3
import json

class not_db(object):
    def __init__(self, name, path='.', driver="fs", counter_dump=100):
        self.name = name
        self.path = path
        self.write_counter = 0
        self.counter_dump = counter_dump
        self.driver = {
              "fs": fs,
              "s3": s3
              }[driver]
        self.error = self.driver.init(self.path, self.name)
        self.cache = self.get('.cache') or {}

    def set(self, key, value):
        self.driver.write(key, value, self.path, self.name)
        self.cache[key] = json.dumps(value)
        self.write_counter += 1
        if not self.write_counter % self.counter_dump:
           self.driver.write('.cache', self.cache, self.path, self.name)
    
    def get(self, key, cached=True):
        def get_from_disk():
            try:
                self.cache[key] = self.driver.read(key, self.path, self.name)
                return self.cache[key]
            except:
                return None
        if not cached:
           return get_from_disk()
        try:
            return json.loads(self.cache[key])
        except:
            return get_from_disk()

    def remove(self, key):
        self.driver.remove(key, self.path, self.name)
        try:
            self.cache.pop(key)
        except:
            pass

    def drop(self):
        self.driver.drop(self.path, self.name)
