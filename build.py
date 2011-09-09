#!/usr/bin/env python

import os

commands = ("pyuic4 -o forms/QtMainWin.py forms/QtMainWin.ui",
            "pyuic4 -o forms/CameraWidget.py forms/CameraWidget.ui")
#            "pyuic4 -o forms/CameraWidget.py forms/CameraDockWidget.ui")

for command in commands:
    print command
    os.system(command)

