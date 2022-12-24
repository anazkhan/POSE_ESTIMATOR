import cv2
import mediapipe as mp
import numpy as np
import time
import posedetector as pd

detector=pd.poseDetector()
ptime=0


cap=cv2.VideoCapture('/home/akhan/python/PoseEstimator/curl5.mp4')
#cap=cv2.VideoCapture(0)
count=0
dir=0

while True:
    ret,frame=cap.read()
    frame=cv2.resize(frame,(1280,720))

    frame=detector.findPose(frame,draw=False)
    lmlist=detector.findPosition(frame,draw=False)
    #print(lmlist)
    if len(lmlist)!=0:
        #detector.findAngle(frame,12,14,16) #right arm
        detector.findAngle(frame,11,13,15) #left arm
        angle=detector.findAngle(frame,11,13,15)
        per =np.interp(angle,(205,290),(0,100))
        bar=np.interp(angle,(205,290),(500,150))
        #print(angle,per)

        #curl count

        if per ==100:
            if dir ==0:
                count+=0.5
                dir=1
        if per==0:
            if dir==1:
                count+=0.5
                dir=0
        
        cv2.rectangle(frame,(1150,150),(1175,500),(0,0,0),3)
        cv2.rectangle(frame,(1150,int(bar)),(1175,500),(0,0,255),cv2.FILLED)
        #cv2.putText(frame,str(int(per)),(1100,75),cv2.FONT_HERSHEY_PLAIN,5,(255,0,0),5)


        #angle
        #cv2.putText(frame,str(int(angle)),(150,300),cv2.FONT_HERSHEY_PLAIN,5,(255,0,0),5)

        cv2.rectangle(frame,(0,450),(250,720),(0,0,0),cv2.FILLED)
        cv2.putText(frame,str(int(count)),(50,680),cv2.FONT_HERSHEY_PLAIN,15,(255,255,255),25)

    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    #cv2.putText(frame,str(int(fps)),(50,100),cv2.FONT_HERSHEY_PLAIN,5,(255,0,0),5)

    cv2.imshow('video',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
