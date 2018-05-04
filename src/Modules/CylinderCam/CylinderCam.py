import libjevois as jevois
import cv2
import numpy as np
from process import process_image
import struct


def checksum(data):
  """ Implementation of Fletcher-16 checksum 
    @return (lobyte,hibyte) tuple 
  """
  hisum = 0
  losum = 0
  for c in data:
    losum = (losum + c)%256
    hisum = (losum + hisum)%256
  return losum + (hisum<<8)

class CylinderCam:

    def __init__(self):
        pass

    def processNoUSB(self, inframe):
        self.process(inframe,None)
    
    def process(self, inframe, outframe):

        im = inframe.getCvBGR()

        dbg,re,rc = process_image(im)
      
        # entry
        entry_area,entry_color,entry_h = re

        # cylinder
        cylinder_area,cylinder_color = rc

        entry_area = 0 if entry_area is None else entry_area
        cylinder_area = 0 if cylinder_area is None else cylinder_area

        word = struct.pack("cccHII",
          bytes([0x55]),
          bytes([ord(entry_color[0])]),
          bytes([ord(cylinder_color[0])]),
          int(entry_h),
          int(entry_area),
          int(cylinder_area))
        word += struct.pack("H",checksum(word))       
        jevois.sendSerial(word) 

        if outframe is not None:
            outframe.sendCvBGR(dbg)

