import cv2
import os
import numpy as np
import pickle
import cvzone
# from cvzone.ImageProcessing import putTextRect
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Importing the students Images
folderPath="Images"

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://facerecognitionrealtime-5cee5-default-rtdb.asia-southeast1.firebasedatabase.app/"
})
# from EncodeGenerator import encodeListKnownWithIds, studentIds

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

imgBackground=cv2.imread('Resources/Live Monitoring.png')

# Importing the Mode Images
folderModePath="Resources/Modes"
modePathList=os.listdir(folderModePath)
imgModeList=[]

for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))
# print(len(imgModeList))

#Load the Encoding File
print("Loading Encoded File")
file=open('EncodeFile.p','rb')
encodeListKnownWithIds=pickle.load(file)
file.close()
encodeListKnown,studentIds=encodeListKnownWithIds
# print(studentIds)
print("Encode File Loaded")
print(studentIds)

modeType=0
counter=0
id=0

while True:
    success,img=cap.read()

    imgS =cv2.resize(img,(0,0),None,0.25,0.25)
    imgS =cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)

    faceCurFrame=face_recognition.face_locations(imgS)
    encodeCurFrame=face_recognition.face_encodings(imgS,faceCurFrame)

    imgBackground[162:162+480,55:55+640]=img
    imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceloc in zip(encodeCurFrame,faceCurFrame):
            matches=face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis=face_recognition.face_distance(encodeListKnown,encodeFace)
            # print("matches",matches)
            # print("faceDis",faceDis)

            matchIndex=np.argmin(faceDis)
            # print("Match Index",matchIndex)

            print(faceDis)
            print(matches)
            #Later add threshold of matchIndex=0.5
            if matches[matchIndex] and faceDis[matchIndex]< 0.5:
                # print("Known Face detected")
                # print(studentIds[matchIndex])
                y1,x2,y2,x1=faceloc
                y1, x2, y2, x1=y1*4,x2*4,y2*4,x1*4
                bbox = 55+x1,162+y1,x2-x1,y2-y1
                imgBackground=cvzone.cornerRect(imgBackground,bbox,rt=0)
                id=studentIds[matchIndex]

                # # 🟢 Save the cropped face image
                # face_img = img[y1:y2, x1:x2]
                # face_img = cv2.resize(face_img, (200, 200))
                #
                # # Make sure the folder exists
                # os.makedirs("ExtractedFaces", exist_ok=True)
                #
                # # Create a unique filename with ID and timestamp
                # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                # filename = f"ExtractedFaces/face_{id}_{timestamp}.jpg"
                #
                # # Save the face image
                # cv2.imwrite(filename, face_img)
                # print(f"Saved face image: {filename}")

                if counter==0:
                    # cv2.putText(imgBackground,"Loading",(275,400))
                    # cv2.imshow("Face Attendance",imgBackground)
                    # cv2.waitKey(1)
                    counter=1
                    modeType=1
            else:
                print("Going for unknown face")

                # Inside your 'else' block for unmatched face
                y1, x2, y2, x1 = faceloc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                face_img = img[y1:y2, x1:x2]

                # Encode the unknown face
                unknown_face_rgb = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
                encodings = face_recognition.face_encodings(unknown_face_rgb)
                if encodings:
                    # mode should be set to one---> mode=1

                    os.makedirs("Images", exist_ok=True)

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                    filename = f"Images/unknown_{timestamp}.jpg"
                    saved=cv2.imwrite(filename, face_img)
                    if saved:
                        print(f"✅ Saved unknown face image: {filename}")
                    else:
                        print(f"❌ Failed to save image at: {filename}")
                    print(f"Saved unknown face image: {filename}")
                    encode = encodings[0]
                    id = f"unknown_{timestamp}"

                    # Load existing
                    if os.path.exists("EncodeFile.p"):
                        with open("EncodeFile.p", 'rb') as file:
                            encodeListKnown, studentIds = pickle.load(file)
                    else:
                        encodeListKnown, studentIds = [], []

                    # Append and save
                    encodeListKnown.append(encode)
                    studentIds.append(id)
                    with open("EncodeFile.p", 'wb') as file:
                        pickle.dump([encodeListKnown, studentIds], file)
                    print(f"Encoding for unknown face saved with ID: {id}")

                    # add to the database
                    ref = db.reference('Students')
                    data = {
                        id: {
                            "Name": id,
                            "total_count": 1,
                            'last_check_in_time': timestamp
                        }
                    }
                    for key, value in data.items():
                        ref.child(key).set(value)

                    print("Added to the database")
                    # continue
                else:
                    print("No encodings found in unknown face")

        if counter!=0:
            if counter==1:
                #get the data
                studentInfo=db.reference(f'Students/{id}').get()
                print(studentInfo)

                if studentInfo:
                    print("Student found:", studentInfo)
                else:
                    print("Unknown person detected (not in database)")
                    continue
                #get the image from storage
                # Find the correct file with the given ID
                file_name = next((f for f in os.listdir(folderPath) if f.startswith(id)), None)

                # Load image into a variable if found
                print("I am here")
                if file_name:
                    img_path = os.path.join(folderPath, file_name)
                    img_st = cv2.imread(img_path)
                    if img_st is not None:
                        img_st = cv2.resize(img_st, (216, 216))
                    else:
                        continue
                # img_st = cv2.imread(os.path.join(folderPath, file_name)) if file_name else None
                # img_st = cv2.resize(img_st, (216, 216))


                # img_st = cv2.imread(image_path)
                # cv2.imshow(f"Student {id}", img_st)
                #------------------------------
                print(file_name)
                print(img_st)
                print("I came")
                #Update data of attendance
                datetimeObject=datetime.strptime(studentInfo['last_check_in_time'],"%Y%m%d_%H%M%S")
                # datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%dT%H:%M:%S.%f")
                secondsElapsed=(datetime.now()-datetimeObject).total_seconds()
                # print(secondsElapsed)

                if secondsElapsed>30:
                    ref=db.reference(f'Students/{id}')
                    studentInfo['total_count']+=1
                    ref.child('total_count').set(studentInfo['total_count'])
                    ref.child('last_check_in_time').set(datetime.now().strftime("%Y%m%d_%H%M%S"))
                else:
                    modeType=3
                    counter=0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType!=3:
                if 10<counter<20:
                    modeType=2

                imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]

                if counter<=10:
                    cv2.putText(imgBackground,str(studentInfo['total_count']),(861,125),
                                cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                    #
                    # cv2.putText(imgBackground, str(studentInfo['major']), (1006,550),
                    #             cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    # cv2.putText(imgBackground, str(id), (1006,493),
                    #             cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                    # cv2.putText(imgBackground, str(studentInfo['standing']), (910,625),
                    #             cv2.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)
                    # cv2.putText(imgBackground, str(studentInfo['Year']), (1025,625),
                    #             cv2.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)
                    # cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125,625),
                    #             cv2.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)
                    (w,h),_=cv2.getTextSize(studentInfo['Name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
                    offset=(414-w)//2
                    cv2.putText(imgBackground, str(studentInfo['Name']), (808+offset, 445),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                    imgBackground[175:175 + 216, 909:909 + 216] = img_st
                    cv2.waitKey(1)
                # image_path=os.path.join(folderPath,f"{id}.png")
                # print(image_path)
                # image_path = os.path.abspath(os.path.join(folderPath, f"{id}.png"))
                # print("Corrected Path:", image_path)

                counter+=1

                if counter>=20:
                    counter=0
                    modeType=0
                    studentInfo=[]
                    img_st=None
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType=0
        counter=0
    # cv2.imshow("Webcam",img)
    cv2.imshow("Face Recognition",imgBackground)
    cv2.waitKey(1)
