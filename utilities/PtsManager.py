# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="olmozavala"
__date__ ="$Feb 25, 2010 7:51:05 PM$"
from utilities.StereoCam import *
from point import *

class _PtsManager(object):
    """This class should be used as a Singleton. Create an object using PtsManager()"""

    def __init__(self):
        """This class controls all the 3D points of the digitizer"""        
        self.instance = "Instance at %d" % self.__hash__()
        self.initVars()

    def initVars(self):
        self.depth = [] #Contains the depth for all the pair of points
        self.leftpts = [] #All the selected points in the left image
        self.rightpts = [] #All the selected points in the right image
        self.lastAdd = '' #From what image was the last point added 'l' or 'r'
        self.total = 0 #Total number of landmarks (With depth)

        
    def addLeftPoint(self,x,y):
        if(len(self.leftpts)>len(self.rightpts)):
            print "The next point has to be selected from the right image"
        else:
            self.lastAdd = 'l'
            self.leftpts.append(point(x,y,0))

    def addRightPoint(self,x,y):
        if(len(self.leftpts)<len(self.rightpts)):
            print "The next point has to be selected from the left image"
        else:
            self.lastAdd = 'r'
            self.rightpts.append(point(x,y,0))

    def removeLastPoint(self):
        if((self.lastAdd == 'l') and (len(self.leftpts)>0)):
            self.leftpts.pop()

        if((self.lastAdd == 'r') and (len(self.rightpts)>0)):
            self.rightpts.pop()

    def calcDepth(self,stereoCam,imw,imh):        
        self.depth = []
        size = min(len(self.leftpts),len(self.rightpts))
        self.total = size
        self.depth = []
        print " "
        print " "
        print " "

        for i in range(size):
#            The points should be relative to the center of the image            

            xleft = self.leftpts[i].x - imw/2
            xright = self.rightpts[i].x - imw/2

#            xleft = -2013
#            xright = -1966.6

            # Changing the pixel values to meters
            d2 = xleft * stereoCam.ccdw / imw
            d1 = xright * stereoCam.ccdw / imw        

            z = abs((float(stereoCam.foclen*stereoCam.dist)/(d2 - d1)))

            print "Left pos  =",self.leftpts[i].x
            print "Right pos =",self.rightpts[i].x,"\n"

            print "Dleft in pixel =",xleft
            print "Dright in pixel=",xright,"\n"

            print stereoCam.ccdw
            print imw,"\n"

            print "Z in mts:",z,"\n"

            self.depth.append(z)
            
        self.maxValues()
        self.printPointsWithDepth()

    def printPointsWithDepth(self):
        print "--------------- Actual points -----------"
        rg = range(min(len(self.leftpts),len(self.rightpts)))
        for i in rg:
            if(len(self.depth) > i):
                z = self.depth[i]
            else:
                z = -1
            print "L :",self.leftpts[i].x,' ',self.leftpts[i].y, ' -- z = ',z
            print "R :",self.rightpts[i].x,' ',self.rightpts[i].y, ' -- z = ',z

    def printPoints(self):
        print "--------------- Actual points -----------"
        rg = range(min(len(self.leftpts),len(self.rightpts)))
        for i in rg:
            print "L : ",self.leftpts[i].x,'x',self.leftpts[i].y
            print "R : ",self.rightpts[i].x,'x',self.rightpts[i].y

    def savePoints(self,fileName,imw,imh):
        f = open(fileName,'w')
        rg = range(min(len(self.leftpts),len(self.rightpts)))
        f.write("3D landmarks\n")#Just a header
        f.write(str(imw)+','+str(imh)+'\n')#Original size of the image
        for i in rg:
            z = self.depth[i]
            f.write('L,'+str(self.leftpts[i].x)+','+str(self.leftpts[i].y)+','+str(z)+'\n')
            f.write('R,'+str(self.rightpts[i].x)+','+str(self.rightpts[i].y)+','+str(z)+'\n')

    def loadPoints(self,fileName):
        f = open(fileName,'r')
        f.readline() #Reading headder
        
        size = f.readline()# Reading size of the image width and heigth
        size = size.split(',')
        imw = int(size[0])
        imh = int(size[1])
        
        # Reading all the points
        for line in f:
            vars = line.split(',')
            x = float(vars[1])
            y = float(vars[2])
            z = float(vars[3])
            if(vars[0] == 'L'):
                self.leftpts.append(point(x,y,z))
                self.lastAdd = 'l' #From what image was the last point added 'l' or 'r'
            else:
                self.lastAdd = 'r' #From what image was the last point added 'l' or 'r'
                self.rightpts.append(point(x,y,z))

        # Assigning the depth of the points. This part assumes that the
        # depth of the left and right image should be the same for the corresponding
        # points
        for i in range(min(len(self.leftpts),len(self.rightpts))):
            self.total += 1 #Total number of landmarks (With depth)
            self.depth.append(self.rightpts[i].z)
        
        return imw, imh

    def maxValues(self):
        """Obtains the maximimum value of all the points (x,y,z)"""
        maxx = 1.0
        maxy = 1.0
        maxz = 1.0        
        
        for i in range(min(len(self.leftpts),len(self.rightpts))):
            if(abs(self.leftpts[i].x) > maxx):
                maxx = abs(self.leftpts[i].x)
            if(abs(self.rightpts[i].x) > maxx):
                maxx = abs(self.rightpts[i].x)

            if(abs(self.leftpts[i].y) > maxy):
                maxy = abs(self.leftpts[i].y)
            if(abs(self.rightpts[i].y) > maxy):
                maxy = abs(self.rightpts[i].y)

            if(abs(self.leftpts[i].z) > maxz):
                maxz = abs(self.leftpts[i].z)
            if(abs(self.rightpts[i].z) > maxz):
                maxz = abs(self.rightpts[i].z)        

        return maxx, maxy, maxz

_singleton = _PtsManager()

def PtsManager(): return _singleton