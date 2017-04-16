# =======================================================================
# title           :trafficlightdetection_pi.py
# description     :This program holds the function for TrafficLightDetection on Raspberry Pi
# author          :Marco Moro
# date            :03.02.2017
# version         :0.2
# usage           :python trafficlightdetection_pi.py
# notes           :
# python_version  :3.5.2
# opencv_version  :3.1.0
# =======================================================================

# Import the modules needed to run the script.
import time
import logging
import common.config.confighandler as cfg

from trafficlight.trafficlightdetectionhandler import TrafficLightDetection
from logging.config import fileConfig
from common.processing.camerahandler import CameraHandler
from threading import Thread


class TrafficLightDetectionPi(object):
    # Initialize the class
    def __init__(self):
        fileConfig(cfg.get_logging_config_fullpath())
        self.__log = logging.getLogger()
        self.__log.setLevel(cfg.get_settings_loglevel())
        self.stopped = True
        self.frame = None
        self.trafficstatus = "red"
        self.pistream = CameraHandler().start()
        self.start()

    def start(self):
        if self.stopped:
            t = Thread(target=self.update, args=())
            t.daemon = True
            self.stopped = False
            t.start()
            time.sleep(0.5)

    def getstatus(self):
        return self.trafficstatus

    def updatestatus(self, status):
        self.trafficstatus = status

    def update(self):
        while not self.stopped:
            img = self.pistream.read()
            tld = TrafficLightDetection()
            self.frame = tld.detect_trafficlight(img)
            self.updatestatus(tld.get_color_state())

    def stop(self):
        self.stopped = True
        CameraHandler().stop()

if __name__ == '__main__':
    TrafficLightDetectionPi()
    time.sleep(999)