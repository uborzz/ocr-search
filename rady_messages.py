# -*- coding: utf-8 -*-

import cv2
import rady_functions as rfs

class Messages(object):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance.__init__()
        return cls.__instance

    def __init__(self):
        self.head = ""
        self.information = ""
        self.question = ""
        self.answers = ""

    def set_header(self, name):
        self.head = name

    def clear_info(self):
        self.information = ""

    def set_info(self, text):
        self.information = text

    def print_info_on_image(self, frame):
        # CURRENT INFO
        cv2.putText(frame, f"{self.head}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, rfs.color("white"), 1)
        cv2.putText(frame, f"{self.information}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.55, rfs.color("red"), 1)
        cv2.putText(frame, f"{self.question}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.55, rfs.color("yellow"), 1)
        cv2.putText(frame, f"{self.answers}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.55, rfs.color("blue"), 1)

