# -*- coding: utf-8 -*-

import cv2
import numpy as np
from PIL import Image
import pytesseract
import modes
from rady_messages import Messages

msgs = Messages()

def cv2pil(image):
    """
    Recibe imagen -np.array- de opencv (BGR)
    Devuelve imagen Image de PIL
    """
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_image)
    return pil_image


def extract_text(image):
    """
    :param image: Image. PIL.Image or np.ndarray (OpenCV image)
    :return: text in image.
    """

    # if type(image) is np.ndarray:
    #     # case image is and opencv image
    #     image = cv2pil(image)

    text = pytesseract.image_to_string(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), config="--psm 6", lang="spa")
    # text = pytesseract.image_to_string(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), config="--psm 6", lang="eng")
    parsed_text = text.replace('º', 'o')
    # print(image.shape)
    print(parsed_text)
    return parsed_text

def evaluate_key(key_pressed, camera, searcher, frame):
    """
    :param key_pressed: identificacion tecla pulsada (return del waitKey de opencv)
    :param camera:
    :param searcher:
    :param frame: imagen fresca
    :return: Retorna True si el programa principal debe acabaaaaaaaaaaaaarr
    """
    k = key_pressed
    if k == ord('q'):
        return True
    elif k == 27:
        return True
    elif k == ord('w'):
        camera.menu_config()
    elif k == ord('z'):
        # clicka zona preguntas
        msgs.set_info("Clicka dos puntos para seleccionar el area de la pregunta!")
        searcher.mode = modes.QUESTION_SET_FIRST_POINT

    elif k == ord('x'):
        # click zona respuestas
        msgs.set_info("Clicka dos puntos para seleccionar el area de las respuestas!")
        searcher.mode = modes.ANSWERS_SET_FIRST_POINT

    elif k == ord('r'):
        searcher.running = True
        text = "Running..."
        print(text)
        msgs.set_info(text)
        # corre deteccion en las zonas

    elif k == ord('s'):
        searcher.running = False

    elif k == ord('m'):
        # analiza a mano foto actual:
        filtered_image = filter_image(frame)
        text = extract_text(filtered_image)
        print("\nBinarization", text)
    elif k == ord('n'):
        text = extract_text(frame)
        print("\nSin filtros", text)


def color(color_name="white"):
    """
    :param color_text: name of the color
    :return: BGR tuple of that color
    """
    if color_name == "green":       bgr = (0, 255, 0)
    elif color_name == "cyan":      bgr = (255, 255, 0)
    elif color_name == "yellow":    bgr = (0, 255, 255)
    elif color_name == "blue":      bgr = (255, 0, 0)
    elif color_name == "red":       bgr = (0, 0, 255)
    elif color_name == "black":     bgr = (0,0,0)
    else:                           bgr = (255, 255, 255)  # white
    return bgr


def print_overlays(frame, searcher):
    cv2.rectangle(frame, (420, 205), (595, 385), (0, 0, 255), -1)
    cv2.addWeighted(frame, alpha, output, 1 - alpha, 0, output)


def filter_image(image):
    # load the example image and convert it to grayscale)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # make a check to see if median blurring should be done to remove
    # noise
    gray = cv2.medianBlur(gray, 3)
    result = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    print("Tamano gray:", gray.shape)
    print("Tamano result:", result.shape)
    cv2.imshow("Filtrada", gray)

    return result

