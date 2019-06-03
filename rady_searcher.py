# -*- coding: utf-8 -*-

import cv2
import numpy as np
import rady_functions as rfs
from rady_messages import Messages

msgs = Messages()

class Searcher:
    def __init__(self):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.running = False
        self.mode = "normal"

        self.__point = ()
        self.roi_question_coords = ()
        self.roi_answers_coords = ()
        self.roi_question_mask = None
        self.roi_answers_mask = None

        self.question_text = None
        self.answers_text = []

        self.frame_shape = ()
        self.mask_initialized = False

    def initialize_masks(self, frame_shape):
        self.frame_shape = frame_shape
        self.roi_answers_mask = self.empty_mask()
        self.roi_question_mask = self.empty_mask()
        self.mask_initialized = True


    def empty_mask(self):
        if self.frame_shape:
            return np.zeros(self.frame_shape, dtype=np.uint8)
        else:
            return None

    def save_aux_point(self, x, y, next_mode):
        self.__point = (x, y)
        self.mode = next_mode

    def save_roi_question(self, x, y):
        if self.__point[0] < x:
            x1 = self.__point[0]
            x2 = x
        else:
            x1 = x
            x2 = self.__point[0]

        if self.__point[1] < y:
            y1 = self.__point[1]
            y2 = y
        else:
            y1 = y
            y2 = self.__point[1]

        self.__point = ()
        self.roi_question_mask = self.empty_mask()
        self.roi_question_coords = (x1, y1, x2, y2)
        cv2.rectangle(self.roi_question_mask, (x1,y1), (x2,y2), color=rfs.color("yellow"), thickness=-1)
        msgs.clear_info()
        self.mode = "normal"

    def save_roi_answers(self, x, y):
        if self.__point[0] < x:
            x1 = self.__point[0]
            x2 = x
        else:
            x1 = x
            x2 = self.__point[0]

        if self.__point[1] < y:
            y1 = self.__point[1]
            y2 = y
        else:
            y1 = y
            y2 = self.__point[1]

        self.__point = ()
        self.roi_answers_mask = self.empty_mask()
        self.roi_answers_coords = (x1, y1, x2, y2)
        cv2.rectangle(self.roi_answers_mask, (x1, y1), (x2, y2), color=rfs.color("blue"), thickness=-1)
        msgs.clear_info()
        self.mode = "normal"

    def print_rois_on_image(self, frame):
        # print(frame.shape, frame.dtype)
        if self.roi_question_mask is not None:
            frame = cv2.addWeighted(frame, 1, self.roi_question_mask, 0.3, 1, 0)
        if self.roi_answers_mask is not None:
            frame = cv2.addWeighted(frame, 1, self.roi_answers_mask, 0.3, 0.1, 0)
        return frame