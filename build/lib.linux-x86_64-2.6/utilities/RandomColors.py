# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="olmozavala"
__date__ ="$Apr 21, 2010 12:12:59 PM$"

from random import random

class _RandomColors(object):

    def __init__(self):
        # just for the sake of information
        self.instance = "Instance at %d" % self.__hash__()
        #By default it stores 300 different colors        
        self.randColors(300)

    def randColors(self,difColors):
        self.difColors = difColors
        """Obtain n different number of colors"""
        self.red, self.green, self.blue = [[],[],[]]
        # Stores N different colors that are used to display landmarks
        for i in range(difColors):
            self.red.append(random())
            self.green.append(random())
            self.blue.append(random())



    def getColors(self):
        return self.red, self.green, self.blue


_singleton = _RandomColors()

def RandomColors(): return _singleton