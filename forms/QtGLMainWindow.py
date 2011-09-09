# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="olmozavala"
__date__ ="$Mar 18, 2010 1:00:44 PM$"


import Image
import ImageQt
from glwidgets.LandmarkViewer import LandmarkViewer
import sys

from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import *

from glwidgets.DitizerWidget import DigitizerWidget
from forms.QtMainWin import *
from forms.AdminCameraWidget import *

from utilities.split_mpo import *
from utilities.FileUtils import *
from utilities.PtsManager import PtsManager
from utilities.StereoCam import StereoCam



class QtGLMainWindow(QMainWindow, Ui_QtMainWin):
#       Properties of the Camera
#       Param1 Distance between cameras
#       Param2 Focall length
#   Lens focal length 	f=6.3 - 18.9mm, equivalent to 35.0 - 105.0mm on a 35mm camera
#   Number of pixels 32048 x 1536 (img size)
#   CCD Sensor 1/2.3 Diagonal 7.7 mm    Width 6.16 mm Height 4.62 mm
#   Everything is in centimeters
    def __init__(self, dist ,focalLength,ccdWidth, ccdHeigth, parent = None):
        """Initialize all the settings of the main window"""
        self.rightImg = ''
        self.leftImg = ''
        self.selectedWidget = 1
        self.imw = -1
        self.imh = -1

        QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.camera = StereoCam(dist ,focalLength,ccdWidth, ccdHeigth)
        self.initWidgets()
        self.ptsManager = PtsManager()
                        
        #--------------------- Setting SIGNAL --> SLOT-----------
        self.connect(self.actionOpen, SIGNAL("activated()"),self.openFile)
        self.connect(self.actionSaveLandmarks, SIGNAL("activated()"),self.saveLandmarks)        
        self.connect(self.actionLoad_Land, SIGNAL("activated()"),self.loadLandmarks)            
        self.connect(self.actionClearMarks, SIGNAL("activated()"), self.clearLandmarks)
        self.connect(self.actionResetMarks, SIGNAL("activated()"), self.resetViewers)
        self.connect(self.tabWidget, SIGNAL("currentChanged(int)"), self.tabChanged)

    def tabChanged(self,index):
        self.updateWidgets()
        
    def adminTab(self, action):
        """Manage the widgets inside the tab"""
        if(action == "init"):
            self.tabWidget = QtGui.QTabWidget(self.centralwidget)
            size = self.size()
            self.tabWidget.setGeometry(QtCore.QRect(0, 0, size.width(), size.height()))
            self.tabWidget.setObjectName("tabWidget")
            self.tabCamera = self.cameraWidget
            self.tabCamera.setObjectName("Camera")
            self.tabWidget.addTab(self.tabCamera, "Camera")

        if(action == "addImgViewer"):
            # When adding or updating this viewer we need to update the
            # size of the image
            self.imw = self.leftImg.size[0]
            self.imh = self.leftImg.size[1]

            if( self.glDigitizerWidet == None):#First time
                self.glDigitizerWidet = DigitizerWidget(self,self.leftImg,self.rightImg)
                self.tabImgViewer = self.glDigitizerWidet
                self.tabImgViewer.setObjectName("Image")
                self.tabWidget.addTab(self.tabImgViewer, "Image")                
            else:#Only updating the  image
                self.glDigitizerWidet.loadTextures(self.leftImg,self.rightImg)                
            
            self.tabWidget.setCurrentWidget(self.tabImgViewer)
            self.glDigitizerWidet.render()
            self.glDigitizerWidet.updateGL()

        if(action == "updateMarksViewer"):
            if(self.marksViewerWidget == None):
               #Initializing the marks viewer widget               
               self.marksViewerWidget = LandmarkViewer(self.imw,self.imh)
               self.tabMarkViewer = self.marksViewerWidget
               self.tabMarkViewer.setObjectName("3D Marks")
               self.tabWidget.addTab(self.tabMarkViewer, "3D Marks")
            
            self.tabWidget.setCurrentWidget(self.tabMarkViewer)
            self.marksViewerWidget.paintGL()
            self.marksViewerWidget.calcMaxValues()

    def resizeEvent(self, event):
        """When the main window is resized, all the tabs change size"""
        size = event.size()
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, size.width(), size.height()))                

    def resetViewers(self):
        """Reset the landmark viewer to its initial state (no rotation nor zoom)"""        
        if( self.marksViewerWidget != None):            
            self.marksViewerWidget.resetView()
            self.marksViewerWidget.render()
            self.marksViewerWidget.updateGL()

        if( self.glDigitizerWidet != None):            
            self.glDigitizerWidet.resetVariables()            
            self.glDigitizerWidet.render()
            self.glDigitizerWidet.updateGL()

    def updateWidgets(self):
        """Updates the landmarks in each widget"""        

        if( self.glDigitizerWidet != None):            
            self.glDigitizerWidet.updateGL()

        if( self.marksViewerWidget != None):            
            self.marksViewerWidget.calcMaxValues()
            self.marksViewerWidget.updateGL()            

    def clearLandmarks(self):
        """Delets all the landmarks"""
        self.ptsManager.initVars()
        self.updateWidgets()

    def loadLandmarks(self):
        """Loads the 3D landmarks from a file. If the Digitizer widget is initializer
        those landmarks are copied to the widget"""
        fileName = QFileDialog.getOpenFileName(self,"Choose txt file with landmarks", "~/", \
                    "Text files(*.txt *.TXT)")

        if( fileName != ''):
            # Load the points            
            self.imw, self.imh = self.ptsManager.loadPoints(fileName)
            
            if(self.glDigitizerWidet != None):                
                self.glDigitizerWidet.updateGL()

            self.adminTab("updateMarksViewer")
            self.enableMenus(True)
            self.ptsManager.printPointsWithDepth()            

        
    def saveLandmarks(self):
        fileName = QFileDialog.getSaveFileName(self,"Save File", \
                    "~/land.txt","Text file (*.txt)")

        if( fileName != ''):
            self.ptsManager.savePoints(fileName,self.imw,self.imh)

    def keyPressEvent(self,key):
        """ Manages the keyboard inputs and passes them to the central widget"""
        if( (key.text() == 'q')or (key.text() == 'Q')):
            sys.exit(0)

        # Prints the landmarks
        if( (key.text() == 'p')or (key.text() == 'P')):
            self.ptsManager.printPointsWithDepth()

        # Computes the depth of the landmarks and update local variable ptsManager
        if( (key.text() == 'd')or (key.text() == 'D')):
            self.ptsManager.calcDepth(self.camera,self.imw, self.imh)            
            self.updateWidgets()

            if(self.ptsManager.total > 0):
                self.enableMenus(True)
                QtGui.QMessageBox.about(self, "Message",
                    "Depth computed successfully!")
                self.adminTab("updateMarksViewer")
            else:
                QtGui.QMessageBox.about(self, "Warning",
                    "There are no landmarks")
                    
        if( (key.text() == 'r') or (key.text() == 'R')):
            self.resetViewers()

        if(self.glDigitizerWidet != None):        
                self.glDigitizerWidet.keyPressEvent(key)

        if(self.marksViewerWidget != None):
                self.marksViewerWidget.keyPressEvent(key)

    def enableMenus(self,enable):
        """Enables or disables the landmarks menus"""
        self.actionSaveLandmarks.setEnabled(enable)        
        self.actionClearMarks.setEnabled(enable)
        self.actionResetMarks.setEnabled(enable)

    def initWidgets(self):
        """Initialize all the widgets that can be used for this window as none"""
        self.glDigitizerWidet = None
        self.marksViewerWidget = None
        self.cameraWidget = AdminCameraWidget(self.camera)
        self.adminTab("init") #Initialize the tab object    

    def openFile(self):        
        fileName = QFileDialog.getOpenFileName(self,"Choose left image or MPO file", "~/", \
                    "File types (*.png *.jpg *.bmp *.mpo *.PNG *.JPG *.BMP *.MPO)")
        
        if( fileName != ''):
            #We should check if we are opening an mpo file, or any other file type
            # which contains the two images togethe            
            if( (fileName.contains(".MPO")) or (fileName.contains(".mpo"))):
                f = open(fileName)
                self.leftImg, self.rightImg, size =  split_mpo(f)                
                self.adminTab("addImgViewer")
                f.close()
            else:
                self.leftImg = Image.open(str(fileName))                
                fileName = QFileDialog.getOpenFileName(self,"Choose right image", "~/testImages", format("File types (*"+getExtFromFile(fileName)+")"))

                if( fileName != ''):
                    self.rightImg= Image.open(str(fileName))                    
                    self.adminTab("addImgViewer")
                
    def closeFile(self):
        self.centralwidget = self
        print "Closing file:"+fileName
        