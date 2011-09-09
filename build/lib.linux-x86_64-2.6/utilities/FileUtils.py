# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="olmozavala"
__date__ ="$Apr 17, 2010 6:45:33 PM$"

from PyQt4.QtCore import *

def getExtFromFile(fileName):
    """Receives a Qstring obj and returns the ext of the obj like '.jpg' """
    i = fileName.lastIndexOf(".")    
    fileName.remove(0,i)
    return fileName

if __name__ == "__main__":
    print getExtFromFile(QString("/medi/sopas.jpg"))
