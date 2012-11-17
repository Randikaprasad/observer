# -*- coding: utf-8 -*-

import cv
from lib.mixins import DefaultLogger


class Detector(DefaultLogger):
    SINGLE_OUTPUT_SIZE = (320, 240)
    MERGED_OUTPUT_SIZE = (640, 240)
    SCALE_FACTOR = 0.5

    def __init__(self, cascade):
        super(Detector, self).__init__()
        self.set_logger()
        self.camera_index = 0

        for index in xrange(10):
            self.capt = cv.CaptureFromCAM(index)
            if self.capt:
                self.camera_index = index
                break

        self.log.debug("Camera index: %d" % self.camera_index)
        self.cascade = cv.Load(cascade)
        self.reset()

    def capture(self):
        self.reset()
        self.frame = cv.QueryFrame(self.capt)
        self.working_frame = self.resize()

    def reset(self):
        self.frame = None
        self.working_frame = None

    def resize(self):
        dst = cv.CreateImage(
                (int(self.frame.width * Detector.SCALE_FACTOR),
                    int(self.frame.height * Detector.SCALE_FACTOR)),
                self.frame.depth,
                self.frame.channels)
        cv.Resize(self.frame, dst)
        return dst

    def grayscale(self):
        dst = cv.CreateImage((self.working_frame.width,
                                self.working_frame.height),
                                self.working_frame.depth, 1)
        cv.CvtColor(self.working_frame, dst, cv.CV_RGB2GRAY)
        return dst

    def detect(self):
        objects = cv.HaarDetectObjects(self.working_frame,
                    self.cascade,
                    cv.CreateMemStorage(),
                    1.1, 2, 0, (20, 20))
        self.log.debug("Objects: %s" % objects)
        return objects

    def mark(self, objects):
        for obj in objects:
            (x, y, w, h), n = obj
            self.log.debug("Marking (%d, %d, %d, %d)" %
                         (int(x) / Detector.SCALE_FACTOR,
                          int(y) / Detector.SCALE_FACTOR,
                          int(x + w) / Detector.SCALE_FACTOR,
                          int(y + h) / Detector.SCALE_FACTOR))
            cv.Rectangle(self.frame,
                        (int(int(x) / Detector.SCALE_FACTOR),
                         int(int(y) / Detector.SCALE_FACTOR)),
                        (int(int(x + w) / Detector.SCALE_FACTOR),
                         int(int(y + h) / Detector.SCALE_FACTOR)),
                        cv.RGB(0, 255, 0),
                        1, 8, 0)

    def retrieve(self):
        return self.frame

    def save_frame(self, path):
        self.log.info("Saving frame as %s" % path)
        cv.SaveImage(path, self.frame)
