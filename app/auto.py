from time import sleep
from threading import *

class hello(Thread):
    def test(self):
        for i in range(5):
            print("hi")
            sleep(1)

class hi(Thread):
    def test(self):
        for i in range(5):
            print("hii")
            sleep(1)



