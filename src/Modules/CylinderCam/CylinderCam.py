import libjevois as jevois
import cv2
import numpy as np
from process import process_image
import rome


def color_to_rome_color(color):
    return {'O': 'orange', 'G': 'green'}.get(color[0], 'none')


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

        params = dict(
            entry_color = color_to_rome_color(entry_color),
            cylinder_color = color_to_rome_color(cylinder_color),
            entry_height = int(entry_h),
            entry_area = int(entry_area),
            cylinder_area = int(cylinder_area),
        )

        frame = rome.Frame('jevois_tm_cylinder_cam', **params)
        data = frame.data()
        jevois.sendSerial(data)

        if outframe is not None:
            outframe.sendCvBGR(dbg)

