import base64

import cv2
import face_recognition
import numpy as np

haar_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml")


class MultiFaceException(Exception):
    pass


class NoFaceException(Exception):
    pass


class EncodeException(Exception):
    pass


def base_to_img(data):
    encoded_data = data.split(',')[-1]
    np_arr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    im = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    return im


def get_face_vec(im):
    """
    get face vector from im(RGB)
    """
    faces_rect = haar_cascade.detectMultiScale(im, scaleFactor=1.2, minNeighbors=5)
    if len(faces_rect) == 1:
        face_encoding = face_recognition.face_encodings(im, known_face_locations=faces_rect)
    else:
        face_encoding = face_recognition.face_encodings(im, model="large")
    return face_encoding


def pipeline(im1, im2):
    im1, im2 = list(map(lambda x: base_to_img(x), [im1, im2]))
    en1, en2 = list(map(lambda x: get_face_vec(x), [im1, im2]))

    if len(en1) == 0 or len(en2) == 0:
        raise NoFaceException
    if len(en1) > 1 or len(en2) > 1:
        raise MultiFaceException
    en1, en2 = en1[0], en2[0]
    try:
        similarity = (1 - np.sum(np.square(en1 - en2))) * 100
    except Exception as e:
        raise EncodeException("Encoding error")
    return int(similarity)
