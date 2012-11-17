import os
from time import sleep, strftime
from lib.detector import Detector
from lib.mixins import DefaultLogger


class Monitor(DefaultLogger):
    LOOP_SLEEP_SECONDS = 1
    ONE_MINUTE_NOF = 60.0 / LOOP_SLEEP_SECONDS
    CASCADE_FILE = "./haarcascade/haarcascade_frontalface.xml"

    def __init__(self):
        self.set_logger()
        self.framecount = 0
        self.detector = Detector(Monitor.CASCADE_FILE)
        # FIXME: change default to camera name after adding support of
        # multiple cameras
        self.output_path_template = "./img/default/%Y/%m/%d/"
        self.output_file_template = "%H%M%S_%%s.jpg"

    def run(self):
        self.log.info("Starting Monitor.run")
        while True:
            self.framecount += 1
            if self.framecount % Monitor.ONE_MINUTE_NOF == 0:
                self.log.info("Monitor.run: Framecount: %d" % self.framecount)

            self.log.debug("Capturing frame!")
            self.detector.capture()
            objects = self.detector.detect()
            if objects:
                self.log.debug("%d object(s) detected!" % len(objects))
                path = strftime(self.output_path_template)

                try:
                    os.makedirs(path)
                except OSError, e:
                    # Raised when path exists
                    if e.errno == 17:
                        self.log.info("os.mkdirs: Path exists - ignoring!")
                    else:
                        raise e

                filename = strftime(self.output_file_template)
                filename = filename % str(self.framecount)
                self.detector.mark(objects)
                self.detector.save_frame(path + filename)

            sleep(Monitor.LOOP_SLEEP_SECONDS)
