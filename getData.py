import cv2
import numpy
import sqlite3
import os

sampleNum = 0


# Thêm hoặc cập nhật vào SqLite
def insertOrUpdate(id, name, age, gender):
    # Gọi data
    conn = sqlite3.connect('Data.db')

    query = "Select * from People Where ID= " + str(id)

    cursor = conn.execute(query)

    issRecordExist = 0

    for row in cursor:
        issRecordExist = 1

    if (issRecordExist == 0):
        # Insert into People(ID, Name, Age, Gender) values( id,'name','age','gender')
        query = "Insert into People(ID, Name, Age, Gender) values(" + str(id) + ",'" + str(name) + "','" + str(
            age) + "','" + str(gender) + "')"
    else:
        # Update People set Name = 'name', Age= 'age', Gender= 'gender' Where ID= id
        query = "Update People set Name = '" + str(name) + "', Age= '" + str(age) + "', Gender= '" + str(
            gender) + "' Where ID= " + str(id)

    conn.execute(query)
    conn.commit()
    conn.close()


# insert vào db
id = input('- Nhập ID:       |')
name = input('- Nhập tên:      |')
age = input('- Nhập tuổi:     |')
gender = input('- Nhập giới tính:|')
insertOrUpdate(id, name, age, gender)
# load
face_cassade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture('Video/Shark_Hung.mp4')

while (True):
    # Camera
    ret, frame = cap.read()

    # frame = cv2.flip(frame, 1)
    # Vẽ khung chữ nhật để định vị vùng người dùng đưa mặt vào
    # centerH = frame.shape[0] // 2;
    # centerW = frame.shape[1] // 2;
    # sizeboxW = 300;
    # sizeboxH = 400;
    # cv2.rectangle(frame, (centerW - sizeboxW // 2, centerH - sizeboxH // 2),
    #               (centerW + sizeboxW // 2, centerH + sizeboxH // 2), (255, 255, 255), 5)
    # Chuyển ảnh xám
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cassade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # Vẽ hình chữ nhật xung quanh mặt
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
        sampleNum = sampleNum + 1
        cv2.imwrite('dataSet/User.' + str(id) + '.' + str(sampleNum) + '.jpg', gray[y:y + h, x:x + w])

    cv2.imshow('Camera', frame)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
    elif sampleNum > 300:
        break

cap.release()
cv2.destroyAllWindows()
