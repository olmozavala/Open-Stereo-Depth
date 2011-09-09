# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms/QtMainWin.ui'
#
# Created: Sun Jun  6 18:06:47 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_QtMainWin(object):
    def setupUi(self, QtMainWin):
        QtMainWin.setObjectName("QtMainWin")
        QtMainWin.setEnabled(True)
        QtMainWin.resize(613, 478)
        self.centralwidget = QtGui.QWidget(QtMainWin)
        self.centralwidget.setObjectName("centralwidget")
        QtMainWin.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(QtMainWin)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 613, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuLandmarks = QtGui.QMenu(self.menubar)
        self.menuLandmarks.setObjectName("menuLandmarks")
        QtMainWin.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(QtMainWin)
        self.statusbar.setObjectName("statusbar")
        QtMainWin.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(QtMainWin)
        self.actionOpen.setObjectName("actionOpen")
        self.actionQuit = QtGui.QAction(QtMainWin)
        self.actionQuit.setObjectName("actionQuit")
        self.actionClose = QtGui.QAction(QtMainWin)
        self.actionClose.setObjectName("actionClose")
        self.actionOpen_Dir = QtGui.QAction(QtMainWin)
        self.actionOpen_Dir.setObjectName("actionOpen_Dir")
        self.actionSaveLandmarks = QtGui.QAction(QtMainWin)
        self.actionSaveLandmarks.setEnabled(False)
        self.actionSaveLandmarks.setObjectName("actionSaveLandmarks")
        self.actionView_in_3D_Land = QtGui.QAction(QtMainWin)
        self.actionView_in_3D_Land.setEnabled(False)
        self.actionView_in_3D_Land.setObjectName("actionView_in_3D_Land")
        self.actionLoad_Land = QtGui.QAction(QtMainWin)
        self.actionLoad_Land.setObjectName("actionLoad_Land")
        self.actionConfigCamera = QtGui.QAction(QtMainWin)
        self.actionConfigCamera.setObjectName("actionConfigCamera")
        self.actionClearMarks = QtGui.QAction(QtMainWin)
        self.actionClearMarks.setEnabled(False)
        self.actionClearMarks.setObjectName("actionClearMarks")
        self.actionResetMarks = QtGui.QAction(QtMainWin)
        self.actionResetMarks.setEnabled(False)
        self.actionResetMarks.setObjectName("actionResetMarks")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuLandmarks.addAction(self.actionLoad_Land)
        self.menuLandmarks.addAction(self.actionSaveLandmarks)
        self.menuLandmarks.addAction(self.actionClearMarks)
        self.menuLandmarks.addAction(self.actionResetMarks)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuLandmarks.menuAction())

        self.retranslateUi(QtMainWin)
        QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL("activated()"), QtMainWin.close)
        QtCore.QMetaObject.connectSlotsByName(QtMainWin)

    def retranslateUi(self, QtMainWin):
        QtMainWin.setWindowTitle(QtGui.QApplication.translate("QtMainWin", "OpenStDepth", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("QtMainWin", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuLandmarks.setTitle(QtGui.QApplication.translate("QtMainWin", "Landmarks", None, QtGui.QApplication.UnicodeUTF8))
        self.statusbar.setToolTip(QtGui.QApplication.translate("QtMainWin", "Status bar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("QtMainWin", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("QtMainWin", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose.setText(QtGui.QApplication.translate("QtMainWin", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Dir.setText(QtGui.QApplication.translate("QtMainWin", "Open Directory", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveLandmarks.setText(QtGui.QApplication.translate("QtMainWin", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionView_in_3D_Land.setText(QtGui.QApplication.translate("QtMainWin", "View in 3D", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_Land.setText(QtGui.QApplication.translate("QtMainWin", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConfigCamera.setText(QtGui.QApplication.translate("QtMainWin", "Parameters", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClearMarks.setText(QtGui.QApplication.translate("QtMainWin", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.actionResetMarks.setText(QtGui.QApplication.translate("QtMainWin", "Reset Viewer", None, QtGui.QApplication.UnicodeUTF8))

