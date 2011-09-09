# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="olmozavala"
__date__ ="$Feb 26, 2010 11:25:11 AM$"
class point(object):
    def __init__(self,x,y,z):
        """Represent a point in 2D or 3D"""
        self.x = x
        self.y = y
        self.z = z

    def addPoint(self,x,y):
        """Adds a 2D point"""
        self.x = x
        self.y = y

    def addPoint(self,x,y,z):
        """Adds a 3D point"""
        self.x = x
        self.y = y
        self.z = z