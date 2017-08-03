from Not_Db import not_db
import unittest
import timeit
import random
import string
import time

def random_string():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(1000))

class TestStringMethods(unittest.TestCase):
    my_db = not_db('martynprattdatabase1', driver='s3')

    def test_get(self):
        self.my_db.set('foo','bar')
        self.assertEqual(self.my_db.get('foo'), 'bar')

    def test_get(self):
        self.my_db.set('foobar',{i:i**2 for i in range(5)})
        self.assertEqual(self.my_db.get('foobar'), {str(i):i**2 for i in range(5)})

    def test_get_from_disk(self):
        value = random_string()
        self.my_db.set('test_get_from_disk', value)
        self.assertEqual(self.my_db.get('test_get_from_disk', cached=False), value)

    def test_remove(self):
        self.my_db.set('foobarfoo', "deleted")
        self.my_db.remove('foobarfoo')
        self.assertEqual(self.my_db.get('foobarfoo'),None)
    
    def test_timing(self):
        iterations = 25
        random_str =''
        i = 0
        key_values = {}
        for func in "write", "read", "disk_read":
           total = 0.0
           for i in range(iterations):
              index = str(i)
              random_str = random_string()
              if func == "write": 
                 random_str = random_string()
                 start = time.clock()
                 self.my_db.set(index, random_str)
                 end = time.clock()
                 key_values[index] = random_str
              elif func == "read":
                 start = time.clock()
                 value = self.my_db.get(index)
                 end = time.clock()
                 self.assertEqual(value, key_values[index])
              elif func == "disk_read":
                 start = time.clock()
                 value = self.my_db.get(index, cached=False)
                 end = time.clock()
                 self.assertEqual(value, key_values[index])
              total += end - start
           print int(1 / (total/iterations)), func, "per second"
           self.assertLess(total/iterations, 0.1) 
    

    

if __name__ == '__main__':
    unittest.main()
