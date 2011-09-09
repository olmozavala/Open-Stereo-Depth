#!/usr/bin/python
import sys
import math
import ImageQt

#Qt GUI libraries
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtOpenGL import *

#OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *

from utilities.RandomColors import *
from utilities.PtsManager import PtsManager

class DigitizerWidget(QGLWidget):
    """ 3D Digitizer widget"""

    def __init__(self, parent,leftImg, rightImg):
        """Constructor, recives QMainWindow, and two PIL Images"""
        QGLWidget.__init__(self, parent)
        self.hnear = .1; #Closest depth that the camera sees
        self.hfar = 50; #Farest depth that the camera sees

        self.zpos = -self.hnear; #Z position of the square exactly where hnear is

        # Size of the widget
        self.winWidth = 100
        self.winHeight = 100

        # There are 3 display modes 1 -> shows the 2 images side by side
        # 2 Shows only the left image, 3 shows only the right image 
        self.displayMode = 1
        self.psize = 4 #Size of the landmarks
        self.hideImg = False
        self.textureIds = [-1, -1] # Ids of the textures

        self.ptsManager = PtsManager()

        self.resetVariables()

        self.rightImg = rightImg
        self.leftImg = leftImg
        self.imw, self.imh = self.rightImg.size
        self.updateSqrSize()                

    def resetVariables(self):
        """Initialize all the internal variables of the widget"""
        self.sqrzoom = 1;

        self.sqrOffsetX = 0
        self.sqrOffsetY = 0

        # This variables are used to move the rightImg using the mouse
        self.mousex = -1
        self.mousey = -1        

        self.colors = RandomColors()
        self.red, self.green, self.blue = self.colors.getColors()

    def drawPoints(self):
        glPushMatrix()
        glPointSize(self.psize)

        colorIndex = 1
        glBegin(GL_POINTS)
        pts = []
        if(self.displayMode == 2):
            pts = self.ptsManager.leftpts

        if(self.displayMode == 3):
            pts = self.ptsManager.rightpts
            
        for pt in pts:
            #Changing the color for each point
            r = self.red[colorIndex % self.colors.difColors]
            g = self.green[colorIndex % self.colors.difColors]
            b = self.blue[colorIndex % self.colors.difColors]
            glColor3f(r,g,b)

            glx, gly = self.imgCoorToGlCoor(pt.x, pt.y)
            #Displaying vertex
            glVertex3f( glx,gly,  self.zpos)    # Bottom Left Of The Texture and Quad
            colorIndex = colorIndex + 1

        glColor3f(1,1,1)
        glEnd()
        glPopMatrix()

    def initializeGL(self):
        """Initialize all the OpenGL paramaters """
        glClearColor(0.0, 0.0, 0.0, 1.0)#Black background
        glEnable(GL_TEXTURE_2D);#Enable texturing
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        self.setMinimumSize(50,50)
        self.updateSqrSize()
        self.resetVariables()
        self.loadTextures(self.leftImg,self.rightImg)
        self.updateGL()

    def updateSqrSize(self):
        """ Updates the square size. Is the biggest square proportional the
        the original leftImage that can be fited inside the window"""
        if( (self.displayMode == 2) or (self.displayMode == 3) ):
            if( (self.imw > self.winWidth) or (self.imh > self.winHeight) ):
                if(self.imw > self.winWidth):
                    self.sqw = self.winWidth
                    self.sqh = int(self.sqw*(float(self.imh)/float(self.imw)))
                    if(self.sqh > self.winHeight):
                        self.sqh = self.winHeight
                        self.sqw = int(self.winHeight*(float(self.imw)/float(self.imh)))
                else:
                    self.sqh = self.winHeight
                    self.sqw = int(self.winHeight*(float(self.imw)/float(self.imh)))
            else:
            # The rightImg is smaller than the window in both directions. Then we maintain
            # the original size of the rightImg
                self.sqw = self.imw
                self.sqh = self.imh
        else:
            if(self.displayMode == 1):         
                if( (2*self.imw > self.winWidth) or (self.imh > self.winHeight) ):
                    if(2*self.imw > self.winWidth):                        
                        self.sqw = self.winWidth/2
                        self.sqh = int(self.sqw*(float(self.imh)/float(self.imw)))
                        if(self.sqh > self.winHeight):                            
                            self.sqh = self.winHeight
                            self.sqw = int(self.winHeight*(float(self.imw)/float(self.imh)))
                    else:                        
                        self.sqh = self.winHeight
                        self.sqw = int(self.winHeight*(float(self.imw)/float(self.imh)))
                else:
                # The rightImg is smaller than the window in both directions. Then we maintain
                # the original size of the rightImg                    
                    self.sqw = self.imw
                    self.sqh = self.imh        

    def loadTextures(self,newleftImg,newrightImg):
        """Loads a texture """
        self.rightImg = newrightImg
        self.leftImg = newleftImg
        
        self.imw, self.imh = self.rightImg.size
        self.textureIds[0] = self.bindTexture(ImageQt.ImageQt(self.leftImg),GL_TEXTURE_2D)
        self.textureIds[1] = self.bindTexture(ImageQt.ImageQt(self.rightImg),GL_TEXTURE_2D)


    def mouseMoveEvent(self,mouseEvent):
        """Receives events from the mouse, moves the rightImg position"""
        x, y = [mouseEvent.x(), mouseEvent.y()]
        self.sqrOffsetX = self.sqrOffsetX + (self.mousex - x)
        self.sqrOffsetY = self.sqrOffsetY + (self.mousey - y)
        self.mousex, self.mousey = x , y
        self.updateGL()

    def windowToGlCoor(self,x,y):
        glx = x - self.winWidth/2
        gly = self.winHeight/2 - y
        return glx, gly

    def glCoorToImage(self,x,y):
        """ Transform a glCoordinate into Image coordinate inside [imw,imh]"""
        # Actual size of the image        
        sizew, sizeh = float(self.sqw*self.sqrzoom), float(self.sqh*self.sqrzoom)        

        # Origin of the image in the GL coordinates
        ox, oy = (-sizew/2 - self.sqrOffsetX), (-sizeh/2 + self.sqrOffsetY)        

        # Ratio of the original image and the displayed one
        ratiox, ratioy = (self.imw/sizew), (self.imh/sizeh)        

        imx = (x - ox)*ratiox
        imy = (y - oy)*ratioy        

        return imx, imy

    def imgCoorToGlCoor(self,x,y):
        """Transform an image coordinate into GL coordinate"""
        # Actual size of the image
        sizew, sizeh = float(self.sqw*self.sqrzoom), float(self.sqh*self.sqrzoom)

        # Origin of the image in the GL coordinates
        ox, oy = (-sizew/2 - self.sqrOffsetX), (-sizeh/2 + self.sqrOffsetY)

        # Ratio of the original image and the displayed one
        ratiox, ratioy = (self.imw/sizew), (self.imh/sizeh)

        glx = x/ratiox + ox
        gly = y/ratioy + oy

        return glx, gly


    def mousePressEvent(self,mouseEvent):
        """Receives events from the mouse"""
        self.mousex, self.mousey = [mouseEvent.x(), mouseEvent.y()]        

        if(mouseEvent.button() == Qt.RightButton):
            # Change the windows coordinates to OpenGL coordinates
            glx, gly = self.windowToGlCoor(self.mousex, self.mousey)            

            # Change the OpengGL coordiantes to Image coordinates
            imx, imy = self.glCoorToImage(glx, gly)           

            if( ((imx>=0) and (imy>=0)) and ((imx<=self.imw) and (imy<=self.imh)) ):
                if(self.displayMode == 2):
                    self.ptsManager.addLeftPoint(imx,imy)

                if(self.displayMode == 3):
                    self.ptsManager.addRightPoint(imx,imy)

#                self.ptsManager.printPoints()
            else:
                print "The selected point is outside of the image"

        self.updateGL()

    def modifyZoom(self, amount):
        """Used to increase and decrease the zoom"""
        self.sqrzoom = max(self.sqrzoom + amount,.1)
        self.updateGL()

    def wheelEvent(self,wheelEvent):
        """Use wheel in mouse to change zoom"""
        if( wheelEvent.delta() > 0):
            self.modifyZoom(-.1)
        else:
            self.modifyZoom(.1)


    def updateGL(self):
        """Updates the display. Its a public slot"""
        self.updateCamera()
        self.updateSqrSize()
        self.paintGL()
        self.swapBuffers()
        
    def paintGL(self):
         """Glut display function."""         
         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
         glColorMask( True, True, True, True )        
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
        if( (key.text() == 'q')or (key.text() == 'Q')):
            sys.exit(0)

        if( (key.text() == '1')or (key.text() == '2')or (key.text() == '3')):
            self.displayMode = int(key.text())

        if( (key.text() == 'z') or (key.text() == 'Z')):
            self.ptsManager.removeLastPoint()

        if( (key.text() == 'h') or (key.text() == 'H')):
            self.hideImg = not(self.hideImg)

#        if( (key.text() == 'r') or (key.text() == 'R')):
#            self.resetVariables()

        self.render()
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
        param1 = float(winh)/float(2*(self.hnear))
        fov = 2*math.degrees(math.atan(param1))
        ratio = float(winw)/float(winh)
        gluPerspective(fov, ratio , self.hnear,self.hfar)        

        gluLookAt( 0,0,0,0,0,-1,0,1,0 )

    def render(self):
        """Render the scene."""    
        #Size of the rectangle. Reduce the size of the border
        sizew = float(self.sqw*self.sqrzoom)
        sizeh = float(self.sqh*self.sqrzoom)
        
        if( not (self.hideImg)):
            if( (self.displayMode == 2) or (self.displayMode == 3)):#Displays only the left image
                #Origin of the square containing the texture
                ox = -sizew/2 - self.sqrOffsetX
                oy = -sizeh/2 + self.sqrOffsetY
                if(self.displayMode == 2):
                    self.drawSquare(self.textureIds[0], ox, oy, sizew, sizeh)
                else:
                    self.drawSquare(self.textureIds[1], ox, oy, sizew, sizeh)
            else:
                if(self.displayMode == 1):
                     # Draw left image
                    ox = -sizew - self.sqrOffsetX
                    oy = -sizeh/2 + self.sqrOffsetY
                    self.drawSquare(self.textureIds[0], ox, oy, sizew, sizeh)

                # Draw right image
                ox = - self.sqrOffsetX
                oy = -sizeh/2 + self.sqrOffsetY            
                self.drawSquare(self.textureIds[1], ox, oy, sizew, sizeh)

        self.drawPoints()


    def drawSquare(self, textId, ox, oy, sizew, sizeh):
        """Renders a square with a texture with the size and origin defined"""
        glPushMatrix()
        glColor3f(1,1,1)
        glBindTexture(GL_TEXTURE_2D, textId)
        zdistance = self.zpos        
    
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex3f(ox        ,oy,  zdistance)    # Bottom Left Of The Texture and Quad
        glTexCoord2f(1.0, 0.0); glVertex3f(ox + sizew,oy,  zdistance)    # Bottom Right Of The Texture and Quad
        glTexCoord2f(1.0, 1.0); glVertex3f(ox + sizew,oy + sizeh,  zdistance)    # Top Right Of The Texture and Quad
        glTexCoord2f(0.0, 1.0); glVertex3f(ox        ,oy + sizeh,  zdistance)    # Top Left Of The Texture and Quad
        glEnd()
        glPopMatrix()