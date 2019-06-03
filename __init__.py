# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import cv2

import config as cfg
import modes
import rady_functions as rfs
from rady_messages import Messages
from rady_searcher import Searcher
from rady_stream import Stream


t_start = datetime.now()
print("Comenzando LisaSimpson! Hora actual: {:%Y_%m_%d_%H_%M}".format(t_start))

# Camera
width, height = 640, 480
fps_camera = 30  # a mano, fps de captura de la camara (va en otro hilo).
rotate, undistort = False, False

# Workning params
fps_main = 25

cam = Stream(src=cfg.camera_src, resolution=(width, height), framerate=fps_camera).start()

schr = Searcher()
msgs = Messages()
msgs.set_header(f"{cfg.name} v{cfg.version}")


def clicks_callback(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONUP:
        print(f"Clicked on {x}, {y}!")
        if schr.mode == modes.QUESTION_SET_FIRST_POINT:
            schr.save_aux_point(x, y, next_mode=modes.QUESTION_SET_SECOND_POINT)
        elif schr.mode == modes.QUESTION_SET_SECOND_POINT:
            schr.save_roi_question(x, y)
        elif schr.mode == modes.ANSWERS_SET_FIRST_POINT:
            schr.save_aux_point(x, y, next_mode=modes.ANSWERS_SET_SECOND_POINT)
        elif schr.mode == modes.ANSWERS_SET_SECOND_POINT:
            schr.save_roi_answers(x, y)


def main():

    # handle clicks
    cv2.namedWindow('General')
    # cv2.moveWindow('General', 200, 100)
    cv2.setMouseCallback('General', clicks_callback)

    timer_fps = datetime.now()  # guarda tiempo de ultimo procesamiento.
    micros_para_procesar = timedelta(microseconds=int(1000000 / fps_main))

    while True:

        toca_procesar = datetime.now() - timer_fps >= micros_para_procesar
        if not toca_procesar:
            continue
        timer_fps = datetime.now()

        frame = cam.read()
        if not schr.mask_initialized:
            schr.initialize_masks(frame.shape)

        # Espejo/rotate si/no?
        if rotate:
            frame = cv2.flip(frame, -1)  # 0 eje x, 1 eje y. -1 ambos (rota 180).

        # Lectura teclas apretadas
        k = cv2.waitKey(1)
        if rfs.evaluate_key(key_pressed=k, camera=cam, searcher=schr, frame=frame):
            break

        # # Tiempo de tregua
        # if datetime.now() - t_start <= timedelta(seconds=1):
        #     continue

        if schr.running == True:
            # analiza imagenes -> obtiene cadenas texto -> busca google

            # Question
            (x1, y1, x2, y2) = schr.roi_question_coords
            question_image_crop = frame[y1:y2, x1:x2]
            cv2.imshow("RECORTE", question_image_crop)
            msgs.question = rfs.extract_text(question_image_crop)

            # # Answers
            # (x1, y1, x2, y2) = schr.roi_answers_coords
            # answers_image_crop = frame[y1:y2, x1:x2]
            # cv2.imshow("RECORTE", answers_image_crop)
            # msgs.answers = rfs.extract_text(answers_image_crop)


        # filtered_image = rfs.filter_image(frame)
        # # msgs.question = rfs.extract_text(filtered_image)

        msgs.print_info_on_image(frame)
        resultado = schr.print_rois_on_image(frame)
        cv2.imshow('General', resultado)

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
