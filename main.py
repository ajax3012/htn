import cv2
import numpy as np
import os
import paho.mqtt.client as mqtt #import the client1
import smtplib, ssl
import requests
from firebase import firebase
from datetime import datetime
from time import time
import base64

# Post data
firebase = firebase.FirebaseApplication('https://nguoilaoi-88576-default-rtdb.firebaseio.com/', None)


# Count time
previous = time()
delta = 0

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "groupnhatnguyet@gmail.com"
receiver_email = "datnvt.14@grad.uit.edu.vn"
password = "Aa123456!"
message = """\
Subject: Nguoi la oi

Nguoi la oi!
Xin cho toi muon bo vai
Tua dau guc nga vi moi met qua
Nguoi la oi!
Xin cho toi muon nu hon
Muon roi toi tra, dung voi vang qua
Nguoi la oi!
Xin hay ghe mua dum toi
ot lieu quen lang, de toi thanh than
Nguoi la oi!
Xin cho toi muon niem vui
De lan yeu duoi nay la lan cuoi thoiiii."""

# Create a secure SSL context
context = ssl.create_default_context()

# Connect to MQTT broker
broker_address="broker.hivemq.com"
client = mqtt.Client("P1")
client.connect(broker_address)

#from keras.models import load_model

#model=load_model("model2-038.h5")

# Nhận dạng tên
recognizer = cv2.face.createLBPHFaceRecognizer()
recognizer.load('trainer.yml')
#faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#iniciate id counter
idz = 0
count = 0
# names related to ids: example ==> Marcelo: id=1,  etc
#names = ['None', 'NH_Khanh', 'NVT_Dat', 'CM_Hoa']


#labels_dict={0: 'no mask',1:'mask'}
#color_dict={0:(0,0,255),1:(0,255,0)}

size = 4
webcam = cv2.VideoCapture(0) #Use camera 0

# We load the xml file
classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    (rval, im) = webcam.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    # detect MultiScale / faces 
    faces = classifier.detectMultiScale(gray,1.2,5)

    current = time()
    delta += current - previous
    previous = current

    # Draw rectangles around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(225,0,0),2)
        idz, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        
        # Check if confidence is less them 100 ==> "0" is perfect match 
        
        if (confidence < 50):    
            cv2.putText(im, "nguoi nha", (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            if (delta > 10):
                my_string1 = base64.b64encode(im)
                now = datetime.now().isoformat()
                #date_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
                data =  { 'DateTime': f'{now}',
                          'IsStranger': 'False',
                          'Node': 'Cong chinh',
                          'Image': f'{my_string1}'
                          }
                result = firebase.post('/nguoilaoi',data)
                delta = 0
        else:
            cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(0,0,255),2)
            cv2.putText(im, "nguoi la oi", (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            if (delta > 10):
                my_string2 = base64.b64encode(im)
                now = datetime.now().isoformat()
                #date_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
                data =  { 'DateTime': f'{now}',
                          'IsStranger': 'True',
                          'Node': 'Cong chinh',
                          'Image': f'{my_string2}'
                          }
                result = firebase.post('/nguoilaoi',data)
                
                # Try to log in to server and send email
                try:
                    server = smtplib.SMTP(smtp_server,port)
                    server.ehlo() # Can be omitted
                    server.starttls(context=context) # Secure the connection
                    server.ehlo() # Can be omitted
                    server.login(sender_email, password)
                    # TODO: Send email here
                    server.sendmail(sender_email, receiver_email, message)
                
                except Exception as e:
                    # Print any error messages to stdout
                    print(e)
                finally:
                    server.quit() 

                delta = 0
        
        #cv2.rectangle(im,(x,y),(x+w,y+h),color_dict[label],2)
        #cv2.rectangle(im,(x,y-40),(x+w,y),color_dict[label],-1)
        
        cv2.putText(im, str(idz), (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        #cv2.putText(im, labels_dict[label], (x+w,y+h), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
       
        cv2.putText(im, str(confidence), (x+5,y+h-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 1)
        


# Send MQTT message here

        client.loop_start() #start the loop
        client.publish("nguoilaoi", f"{str(idz)}")

        

        #count += 1
        #cv2.imwrite(f"D:\wallpaper\\user{label}." + str(count) + ".jpg", cv2.rectangle(im,(x,y),(x+w,y+h),color_dict[label],2))
        #cv2.imwrite(f"D:\wallpaper\\user{label}." + str(count) + ".jpg", cv2.rectangle(im,(x,y-40),(x+w,y),color_dict[label],-1))
        
     
       
          
    # Show the image
    cv2.imshow('LIVE',   im)
    key = cv2.waitKey(10)
    # if Esc key is press then break out of the loop 
    if key == 27: #The Esc key
        break
# Stop video
webcam.release()

# Close all started windows
cv2.destroyAllWindows()
