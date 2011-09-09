# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="olmozavala"
__date__ ="$Apr 15, 2010 8:11:38 PM$"

from forms.QtGLMainWindow import QtGLMainWindow
import sys

from PyQt4 import QtGui
from forms.QtGLMainWindow import *

if __name__ == "__main__":
#    test = PtsManager()
#    test.loadPoints("landmarks/land.txt")
#
#    test2 =PtsManager()
#
#    test.printPointsWithDepth()
#    test2.printPointsWithDepth()
#
#    camera = StereoCam( 7.62, 0.63, 0.616, 0.462)
#    test.calcDepth(camera,800,600)
#    test.printPointsWithDepth()
#    test2.printPointsWithDepth()

    app = QtGui.QApplication(sys.argv)
    mpoe = QtGLMainWindow(0.07, 0.0063, 0.0077, 0.0062)
    mpoe.show()

    sys.exit(app.exec_())