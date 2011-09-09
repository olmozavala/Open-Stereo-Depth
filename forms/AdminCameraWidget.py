# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="olmozavala"
__date__ ="$Apr 19, 2010 12:52:43 PM$"

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from forms.CameraWidget import *
from utilities.StereoCam import *

class AdminCameraWidget(QWidget, Ui_CameraWidget):
    
    def __init__(self, camera, parent = None):
        """Initialize all the settings of the camera widget"""
        self.camera = camera
        QWidget.__init__(self, parent)
        
        self.setupUi(self)
        self.updateValues()
        self.connect(self.bt_save, SIGNAL("clicked()"),self.updateParams)

    def updateValues(self):
        self.txtFieldCCDw.setText( str(self.camera.ccdw))
        self.txtFieldCCDh.setText( str(self.camera.ccdh))
        self.txtFieldFoclen.setText( str(self.camera.foclen))
        self.txtFieldDistance.setText( str(self.camera.dist))

    def updateParams(self):
        self.camera.ccdw = float(self.txtFieldCCDw.text())
        self.camera.ccdh = float(self.txtFieldCCDh.text())
        self.camera.foclen = float(self.txtFieldFoclen.text())
        self.camera.dist = float(self.txtFieldDistance.text())
        self.updateValues()
        QtGui.QMessageBox.about(self, "Message",
                        "Success!")