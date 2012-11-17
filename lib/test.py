#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv
import time

single_output_size = (320, 240)
merged_output_size = (640, 240)

scale_factor = 0.5
grayscale = True

cv.NamedWindow("Capture", cv.CV_WINDOW_AUTOSIZE)
camera_index = 0
capture = cv.CaptureFromCAM(camera_index)
cascade = cv.Load('./haarcascade/haarcascade_frontalface_alt.xml')


def detect(image):
    faces = cv.HaarDetectObjects(image, cascade, cv.CreateMemStorage(),\
                1.1, 2, 0, (20, 20))
    return faces


def flip(src):
    cv.Flip(src, None, 1)


def threshold(src, th_type=cv.CV_THRESH_BINARY):
    dst = cv.CreateImage((src.width, src.height), src.depth, src.channels)
    cv.Threshold(src, dst, 100.0, 255.0, th_type)
    return dst


def resize(src, scale):
    dst = cv.CreateImage((int(src.width * scale), int(src.height * scale)),
                            src.depth,
                            src.channels)
    cv.Resize(src, dst)
    return dst


def to_grayscale(src):
    dst = cv.CreateImage((src.width, src.height), src.depth, 1)
    cv.CvtColor(src, dst, cv.CV_RGB2GRAY)
    return dst


def mark_objects(src, objects, scale_factor):
    for obj in objects:
        (x, y, w, h), n = obj
        print "Resizing! ", (x, y, w, h), n
        cv.Rectangle(src,
                     (int(x) * scale_factor, int(y) * scale_factor),
                     (int(x + w) * scale_factor,
                     int(y + h) * scale_factor),
                     cv.RGB(0, 255, 0),
                     1, 8, 0)


def repeat():
    global capture
    global camera_index

    frame = cv.QueryFrame(capture)
    flip(frame)

    print (frame.width, frame.height), frame.depth, frame.channels

    working_frame = resize(frame, scale_factor)
    faces = detect(working_frame)
    mark_objects(working_frame, faces, 1)
    cv.ShowImage("Capture", working_frame)

    # FIXME: replace
    c = cv.WaitKey(10)
    if(c == "n"):
        camera_index += 1
        capture = cv.CaptureFromCAM(camera_index)
        if not capture:
            camera_index = 0
            capture = cv.CaptureFromCAM(camera_index)


if __name__ == "__main__":
    while True:
        s = time.time()
        repeat()
        e = time.time()
        print "Execution time: %s" % str(e - s)
