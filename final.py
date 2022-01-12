import cv2
import numpy as np
from PIL import Image
import pickle
import sqlite3

face_casade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
# cam = cv2.VideoCapture(0);
#Input Video
#cap = cv2.VideoCapture('VideoTrain/Ronaldo.mp4')
cap = cv2.VideoCapture('Video/Shark_Hung.mp4')

rec = cv2.face.LBPHFaceRecognizer_create();
rec.read("recognizer/trainingData.yml")
id = 0
# set text style
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 1
fontcolor = (0, 255, 0)


# get data from sqlite by ID
def getProfile(id):
    conn = sqlite3.connect("Data.db")
    query = "SELECT * FROM People WHERE ID=" + str(id)
    cursor = conn.execute(query)
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile


while (True):

    # camera read
    ret, frame = cap.read();
    # Lật mặt
    #frame = cv2.flip(frame, 1)
    # Ảnh xám
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face = face_casade.detectMultiScale(gray)
    for (x, y, w, h) in face:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        id, cofidence = rec.predict(roi_gray)
        print('ID: ', id)
        print('gia tri: ', cofidence)
        if cofidence > 50:
            cv2.putText(frame, "Name: Unknown", (x, y + h + 30), fontface, fontscale, fontcolor, 2)
        else:
            profile = getProfile(id)
            if (profile != None):
                cv2.putText(frame, "Name: " + str(profile[1]), (x, y + h + 30), fontface, fontscale, fontcolor, 2)
                cv2.putText(frame, "Age: " + str(profile[2]), (x, y + h + 60), fontface, fontscale, fontcolor, 2)
                cv2.putText(frame, "Gender: " + str(profile[3]), (x, y + h + 90), fontface, fontscale, fontcolor, 2)

    cv2.imshow('Face', frame)
    if (cv2.waitKey(1) == ord('q')):
        break;
cap.release()
cv2.destroyAllWindows()
# # Lật khuôn mặt
# img = cv2.flip(img, 1)
# # Vẽ khung chữ nhật để định vị vùng người dùng đưa mặt vào
# centerH = img.shape[0] // 2;
# centerW = img.shape[1] // 2;
# sizeboxW = 300;
# sizeboxH = 400;
#
# cv2.rectangle(img, (centerW - sizeboxW // 2, centerH - sizeboxH // 2),
#               (centerW + sizeboxW // 2, centerH + sizeboxH // 2), (255, 255, 255), 5)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# faces = faceDetect.detectMultiScale(gray, 1.3, 5);

# for (x, y, w, h) in faces:
#     # Vẽ hình chữ nhật quanh mặt
#     cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
#     id, conf = rec.predict(gray[y:y + h, x:x + w])
#     print('Gia tri: ', conf)
#     if conf > 40 :
#         profile = getProfile(id)
#         # set text to window
#         if (profile != None):
#             # cv2.PutText(cv2.fromarray(img),str(id),(x+y+h),font,(0,0,255),2);
#             cv2.putText(img, "Name: " + str(profile[1]), (x, y + h + 30), fontface, fontscale, fontcolor, 2)
#             cv2.putText(img, "Age: " + str(profile[2]), (x, y + h + 60), fontface, fontscale, fontcolor, 2)
#             cv2.putText(img, "Gender: " + str(profile[3]), (x, y + h + 90), fontface, fontscale, fontcolor, 2)
#     else:
#         cv2.putText(img, "Name: Unknown", (x, y + h + 30), fontface, fontscale, fontcolor, 2)
# cv2.imshow('Face', img)
