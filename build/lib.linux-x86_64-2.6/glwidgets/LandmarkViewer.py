# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="olmozavala"
__date__ ="$Apr 19, 2010 9:12:43 PM$"

#!/usr/bin/python

#Qt GUI libraries
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtOpenGL import *

#OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *

from utilities.RandomColors import *
from utilities.PtsManager import *

class LandmarkViewer(QGLWidget):
    """ 3D Landmark viewer"""

    def __init__(self, imw, imh,parent = None):
        """Constructor, recives QMainWindow, and two PIL Images"""        
        # Size of the widget
        self.winWidth = imw
        self.winHeight = imh
         
        self.imw = self.winWidth
        self.imh = self.winHeight

        self.presButton = None

        self.hnear = .1 #Closest depth that the camera see
        self.hfar = 60

        self.colors = RandomColors()
        self.red, self.green, self.blue = self.colors.getColors()

        self.resetView()

        QGLWidget.__init__(self, parent)
        # It is important, PtsManager is a Singleton so if some points are
        # already loaded by another class then, those points will be imported
        self.ptsManager = PtsManager()        
        self.calcMaxValues()

    def calcMaxValues(self):
        """Computes the maximum abs values from the landmarks"""
        self.maxx, self.maxy, self.maxz = self.ptsManager.maxValues()

    def resetView(self):
        # There are 3 display modes 1 -> shows the 2 images side by side
        # 2 Shows only the left image, 3 shows only the right image
        self.displayMode = 2
        self.psize = 5 #Size of the landmarks
        self.zoom = 1
        
        #This values are used to rotate the points.
        # They should be expressed in angles
        self.rotx = 0
        self.roty = 0
        self.rotz = 0

        self.transx = 0
        self.transy = 0
        self.transz = 0
    
        self.ptsOffsetX = 0
        self.ptsOffsetY = 0    

#        self.zpos = -self.hnear; #Z position of the square exactly where hnear is
        self.zpos = -self.hfar/2; #Z position of the square exactly where hnear is
 
    def drawPoints(self, pts):
        """Draws the landmarks in a 3D space"""
        colorIndex = 1
        glBegin(GL_POINTS)
        
        for pt in pts:            
            #Changing the color for each point
            r = self.red[colorIndex % self.colors.difColors]
            g = self.green[colorIndex % self.colors.difColors]
            b = self.blue[colorIndex % self.colors.difColors]
            glColor3f(r,g,b)

            #Normalize all the values between -self.hfar/6 and self.hfar/6
#            print "-----------PLOTING-----------------"
#            print pt.x, pt.y, pt.z
            norx, nory, norz = self.normCord(pt.x, pt.y, pt.z, self.hfar/5)
            
            glVertex3f(norx, nory, norz )
            colorIndex = colorIndex + 1
        glColor3f(1,1,1)
        glEnd()

    def initializeGL(self):
        """Initialize all the OpenGL paramaters """
        glClearColor(0.0, 0.0, 0.0, 1.0)#Black background
        glEnable(GL_TEXTURE_2D);#Enable texturing
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        self.setMinimumSize(50,50)          


    def mouseMoveEvent(self,mouseEvent):
        """Receives events from the mouse, moves the rightImg position"""
        x, y = [mouseEvent.x(), mouseEvent.y()]

        if(self.presButton == Qt.LeftButton):            
            self.roty = self.roty - float(self.mousex - x)/10 #Rotate over y
            self.rotx = self.rotx - float(self.mousey - y)/10 #Rotate over x
        else:            
            self.transy = self.transy + float(self.mousey - y)/30 #Translate over y
            self.transx = self.transx - float(self.mousex - x)/30 #Translate over x
#            self.transz = self.transz - float(self.mousey - y)/10 #Translate over x

        self.mousex, self.mousey = x , y        
        self.updateGL()

    def normCord(self,x,y,z,normValue):
        """Normalize the coordinates  all the values between -10 and 10"""        
        #The values are only positive numbers, so I need to center them
        x = x - self.maxx/2
        y = y - self.maxy/2
        z = z - self.maxz/2
        # And then normalize them      
        normx = (x/(self.maxx/2))*normValue
        normy = (y/(self.maxy/2))*normValue
        normz = (z/(self.maxz/2))*normValue

        return normx,normy,normz


    def mousePressEvent(self,mouseEvent):
        """Receives events from the mouse"""
        self.mousex, self.mousey = [mouseEvent.x(), mouseEvent.y()]
        
        if(mouseEvent.button() == Qt.RightButton):
            self.presButton = Qt.RightButton

        if(mouseEvent.button() == Qt.LeftButton):
            self.presButton = Qt.LeftButton
            
        self.updateGL()

    def modifyZoom(self, amount):
        """Used to increase and decrease the zoom"""
        self.zoom = self.zoom + amount        
        self.updateGL()

    def wheelEvent(self, wheelEvent):
        """Use wheel in mouse to change zoom"""        
        delta = self.hfar/40
        if( wheelEvent.delta() >0):
            self.modifyZoom(-delta)
        else:
            self.modifyZoom(delta)

    def updateGL(self):
        """Updates the display. Its a public slot"""               
        self.paintGL()
        self.swapBuffers()

    def paintGL(self):
         """Glut display function."""
         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
         glColorMask( True, True, True, True )
         self.updateCamera()         
         self.render()#We are only displaying the left rightImg
         

    def resizeGL(self, w, h):
        """ Resize the width and height of the square """
        #The main window has a top toolbar of size 50
        glViewport(0,0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        self.winHeight = h
        self.winWidth = w
        self.updateGL()

    def keyPressEvent(self,key):
        """Manage the keys pressed by the user"""
        if( (key.text() == '1')or (key.text() == '2')or (key.text() == '3')):
            self.displayMode = int(key.text())

        if( (key.text() == 'r')or (key.text() == 'R')):
            self.resetView()
            
        self.updateGL()

    def updateCamera(self):
        """Updates the position of the cameras"""
        winw, winh = [self.winWidth, self.winHeight]#Set rightImg size as local variables

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # This formula is straight forward from http://www.lighthouse3d.com/opengl/viewfrustum/index.php?defvf
        #In this case the choosen camera (left or right) needs to see
        #exactly one of the rightImgs
        ratio = float(winw)/float(winh)               
        gluPerspective(45, ratio , 1,self.hfar)

        gluLookAt( 0,0,0,0,0,-1,0,1,0 )

    def render(self):
        """Render the scene."""
        #Size of the rectangle. Reduce the size of the border
        glPushMatrix()
        #Translate more less to the center in z
        glTranslate(self.transx,self.transy,self.zoom-(self.hfar/2))
        glRotatef(self.rotx,1,0,0)
        glRotatef(self.roty,0,1,0)
        glRotatef(self.rotz,0,0,1)

        # More less 20 lines along the z axis
        self.drawXYZplanes(30,(self.hfar/2))
        self.ptsManager = PtsManager()
        glPointSize(self.psize)        
        if(self.displayMode == 1):
            self.drawPoints(self.ptsManager.leftpts)
            self.drawPoints(self.ptsManager.rightpts)

        if(self.displayMode == 2):
            self.drawPoints(self.ptsManager.leftpts)

        if(self.displayMode == 3):
            self.drawPoints(self.ptsManager.rightpts)
        
        glPopMatrix()

    def drawXYZplanes(self,lines,size):
        glColor(.5,0,0)
        glPointSize(self.psize*2)
        glBegin(GL_POINTS)
        glVertex3f(0,0,0)    # Bottom Left Of The Texture and Quad
        glEnd()

        glBegin(GL_LINES)

        for i in range(lines):
            # Horizontal lines  along the z axis
            glVertex3f( -size, 0, i*(size/lines))
            glVertex3f( size, 0, i*(size/lines))
            glVertex3f( -size, 0, -i*(size/lines))
            glVertex3f( size, 0, -i*(size/lines))

            #Vertical lines along the z axis
            glVertex3f( i*(size/lines), 0, -size)
            glVertex3f( i*(size/lines), 0, size)
            glVertex3f( -i*(size/lines), 0, -size)
            glVertex3f( -i*(size/lines), 0, size)

            # Horizontal lines  along the y axis
            glVertex3f( 0, i*(size/lines), size)
            glVertex3f( 0, i*(size/lines), -size)
            glVertex3f( 0, -i*(size/lines), size)
            glVertex3f( 0, -i*(size/lines), -size)

            # Verticallines  along the y axis
            glVertex3f( 0, size, i*(size/lines))
            glVertex3f( 0, -size, i*(size/lines))
            glVertex3f( 0, size, -i*(size/lines))
            glVertex3f( 0, -size, -i*(size/lines))

        glEnd()