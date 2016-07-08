import os
import cv2

from django.conf import settings

CLASSIFIERS_ROOT = settings.CLASSIFIERS_ROOT

face_cascade = cv2.CascadeClassifier(os.path.join(CLASSIFIERS_ROOT, 'haarcascade_frontalface_default.xml'))
eye_cascade = cv2.CascadeClassifier(os.path.join(CLASSIFIERS_ROOT,'haarcascade_eye.xml'))
nose_cascade = cv2.CascadeClassifier(os.path.join(CLASSIFIERS_ROOT,'haarcascade_mcs_nose.xml'))
mouth_cascade = cv2.CascadeClassifier(os.path.join(CLASSIFIERS_ROOT,'haarcascade_mcs_mouth.xml'))


def detect_coordinates(image_path):
    eyes_coordinates = []
    noses_coordinates = []
    mouth_coordinates = []

    img = cv2.imread(image_path)

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_img, 1.05, 5)

    for (p, q, r, s) in faces:
        cv2.rectangle(img, (p, q), (p + r, q + s), (255, 0, 0), 2)
        face_gray = gray_img[q:q + s, p:p + r]
        face_color = img[q:q + s, p:p + r]

        eyes = eye_cascade.detectMultiScale(face_gray)
        for (ep, eq, er, es) in eyes:
            eyes_coordinates.append([ep, eq, er, es])
            cv2.rectangle(face_color, (ep, eq), (ep + er, eq + es), (0, 255, 0), 2)

        nose = nose_cascade.detectMultiScale(face_gray)
        for (np, nq, nr, ns) in nose:
            noses_coordinates.append([np, nq, nr, ns])
            cv2.rectangle(face_color, (np, nq), (np + nr, nq + ns), (0, 0, 0), 2)

        mouth = mouth_cascade.detectMultiScale(face_gray)
        for (mp, mq, mr, ms) in mouth:
            mouth_coordinates.append([mp, mq, mr, ms])
            cv2.rectangle(face_color, (mp, mq), (mp + mr, mq + ms), (255, 255, 255), 2)

    return eyes_coordinates, noses_coordinates, mouth_coordinates, img
