import cv2
import numpy as np
import os


#Mo camera scan du lieu khuon mat
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap = cv2.VideoCapture(0)
id = input("ID: ")
name = input("Ten: ")
# insertOrUpdate(id, name)

datauser = 0
while(True):
    (ret, frame) = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x +w, y +h), (0,255,0) , 2)
       
        datauser += 1
        cv2.imwrite('/home/nhatnguyet/Downloads/HTN-20210501T081952Z-001/HTN/data/2User.'+str(id)+'.'+str(datauser)+ '.jpg', gray[y: y+h, x: x+w])

    cv2.imshow('frame', frame)
    cv2.waitKey(1)

    if datauser > 100:
        break;

cap.release()
cv2.destroyAllWindows()
