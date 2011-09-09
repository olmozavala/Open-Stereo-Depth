# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="olmozavala"
__date__ ="$Feb 26, 2010 11:26:48 AM$"

class StereoCam(object):
    def __init__(self, dist ,focalLength,ccdWidth, ccdHeigth):
        """Initialize the properties of the camera. The width and Height of the
        ccd should be given in centimeters"""
        self.dist = dist #Distance between two lenses
        self.foclen = focalLength
        self.ccdw = ccdWidth
        self.ccdh = ccdHeigth
        
