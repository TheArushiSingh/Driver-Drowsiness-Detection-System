from scipy.spatial import distance as dist
import imutils
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import time
import dlib
import cv2
import os
import re
from pygame import mixer 
from mailowner import mail_owner
from tkinter import *
from tkinter import messagebox

driver_name = ""
relative_name = ""
relative_email = ""
snapcounter=0

def draw_ui():
    window = Tk()
    window.geometry("1200x600")
    window.title("DROWSINESS DETECTION AND ALERTING SYSTEM")
    background_label = Label(window)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def check_email():
        pattern = re.compile(r'[a-zA-Z_.0-9]+@[a-zA-Z]+\.[a-zA-Z]{1,3}')
        global driver_name,relative_email,relative_name
        driver_name = str(entry1.get())
        relative_name = str(entry2.get())
        relative_email = str(entry3.get())
        if(pattern.search(relative_email)):
            messagebox.showinfo("Success", "Submitted successfully!")
            entry1.delete(0, END)
            window.destroy()
        else:
            messagebox.showinfo("Error", "e-Mail is not valid")
            entry1.delete(0, END)

    title = Label(
        window,
        text = "DROWSINESS DETECTION AND ALERTING SYSTEM",
        font=("algerian", 32),
        bg="#000000",
        fg="#ffffff"
    )
    title.pack(pady=20)

    qbl = Label(
        window, 
        text="Enter the driver name: ", 
        font=("verdana", 19), 
        fg="#ffffff",
        bg="#BA2F16"
        )
    qbl.pack(pady=4)

    entry1 = Entry(
        window,
        font=("Verdana", 16)
         )
    entry1.pack(ipady=5,ipadx=5)
    qbl2 = Label(
        window, 
        text="Enter the relative name: ", 
        font=("verdana", 19), 
        fg="#ffffff",
        bg="#BA2F16"
        )
    qbl2.pack(pady=(50,10))

    entry2 = Entry(
        window,
        font=("Verdana", 16)
    )
    entry2.pack(ipady=5,ipadx=5)
    qbl3 = Label(
        window, 
        text="Enter the relative email address: ", 
        font=("verdana", 19), 
        fg="#ffffff",
        bg="#BA2F16"
        )
    qbl3.pack(pady=(50,10))

    entry3 = Entry(
        window,
        font=("Verdana", 16)
    )

    entry3.pack(ipady=5,ipadx=5)

    button_check = Button(
        window,
        text = "SUBMIT",
        font=("arial",16),
        bg = "#000000",
        fg = "#6ab04c",
        command=check_email
    )
    button_check.pack(pady=40)

    window.mainloop()

def drowsiness_detector():
        global Ealarm,Yalarm,driver_name,relative_name,relative_email,imagename
        def eye_alarm():
            while Ealarm==True:
                mixer.init()
                sound = mixer.Sound("alarm.wav")
                sound.play()

        def yawn_alarm():
            while Yalarm==True:
                mixer.init()
                sound = mixer.Sound("alarm.wav")
                sound.play()


        def eye_aspect_ratio(eye):
            A = dist.euclidean(eye[1], eye[5])
            B = dist.euclidean(eye[2], eye[4])
            C = dist.euclidean(eye[0], eye[3])
            ear = (A + B) / (2.0 * C)
            return ear

        def final_ear(shape):
            (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
            (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0
            return (ear, leftEye, rightEye)

        def lip_distance(shape):
            top_lip = shape[50:53]
            top_lip = np.concatenate((top_lip, shape[61:64]))

            low_lip = shape[56:59]
            low_lip = np.concatenate((low_lip, shape[65:68]))

            top_mean = np.mean(top_lip, axis=0)
            low_mean = np.mean(low_lip, axis=0)

            distance = abs(top_mean[1] - low_mean[1])
            return distance

        
        
        EYE_AR_THRESH = 0.26
        EYE_AR_CONSEC_FRAMES = 45
        YAWN_THRESH = 25
        
        Ealarm = False
        Yalarm = False
        counter = 0
        mail_counter = 0
        yc = 0

        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        print("Starting video stream")

        vs = VideoStream().start()
        time.sleep(1.0) 
        while True:
            frame = vs.read()
            frame = imutils.resize(frame,width=450)
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        
            rects = detector.detectMultiScale(gray,
                                              scaleFactor=1.1,
                                              minNeighbors=5,
                                              minSize=(30,30)) 
            for (x, y, w, h) in rects:
                rect = dlib.rectangle(int(x), int(y), int(x + w),int(y + h))
                shape = predictor(gray,rect)
                shape = face_utils.shape_to_np(shape)
                eye = final_ear(shape)
                ear = eye[0]
                leftEye = eye[1]
                rightEye = eye[2]

                leftEyeHull = cv2.convexHull(leftEye)          
                rightEyeHull = cv2.convexHull(rightEye)
                cv2.drawContours(frame,[leftEyeHull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
                
                distance = lip_distance(shape)
                lip = shape[48:60]
                cv2.drawContours(frame, [lip], -1, (0, 255, 0), 1)

            

                if ear < EYE_AR_THRESH:
                    counter += 1
                    if counter >= EYE_AR_CONSEC_FRAMES:
                        if Ealarm == False:
                            Ealarm = True
                            t = Thread(target=eye_alarm)
                            t.deamon = True
                            t.start()
                            mail_counter = mail_counter+1
                            if(mail_counter==3):
                                imagename = f"snap{snapcounter}.jpg"
                                mail_thread = Thread(target=mail_owner,args=(relative_name,relative_email,driver_name,imagename))
                                mail_thread.start()
                        cv2.putText(frame,"DROWSINESS ALERT!",(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0, 0, 255),2)
                else:
                    counter = 0
                    Ealarm=False

                if(distance > YAWN_THRESH):
                    if Yalarm == False:
                        if(yc==10):
                            Yalarm = True
                            t2 = Thread(target=yawn_alarm)
                            t2.deamon = True
                            t2.start()
                            yc = yc+1
                            imagename = f"snap{snapcounter}.jpg"
                            cv2.imwrite(imagename,frame)
                            mail_thread = Thread(target=mail_owner,args=(relative_name,relative_email,driver_name,imagename))
                            mail_thread.start()
                    cv2.putText(frame,"Yawn Alert",(10,60),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
                else:
                    Yalarm = False
            
                cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0,0), 2)
                
            
            cv2.imshow("Drowsiness Detection Cam (press q to close)", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()
        vs.stop()


if __name__ == "__main__":
    draw_ui()
    if(relative_email!=""):
        drowsiness_detector()
    else:
        print("Your info not filled correctly!")
