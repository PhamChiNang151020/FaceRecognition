import cv2, os
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
path = 'dataSet'


def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    print(imagePaths)
    faces = []
    IDs = []
    for imagePaths in imagePaths:
        faceImg = Image.open(imagePaths).convert('L');
        faceNp = np.array(faceImg, 'uint8')
        print(faceNp)
        # split to get ID of the image
        ID = int(imagePaths.split('\\')[-1].split('.')[1])
        faces.append(faceNp)
        # print ID
        IDs.append(ID)
        cv2.imshow("traning", faceNp)
        cv2.waitKey(10)
    return faces, IDs


faces, IDs = getImagesAndLabels(path)
# trainning
recognizer.train(faces, np.array(IDs))
# Luu
if not os.path.exists('recognizer'):
    os.makedirs('recognizer')
recognizer.save('recognizer/trainingData.yml')
cv2.destroyAllWindows()
