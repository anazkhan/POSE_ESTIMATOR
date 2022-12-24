import cv2
import mediapipe as mp
import time
import math

class poseDetector():

    def __init__(self,mode=False,complexity=2,smooth=True,segmentation=True,smooth_segmentation=True,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.complexity=complexity
        self.smooth=smooth
        self.segmentaton=segmentation
        self.smooth_segmentation=smooth_segmentation
        self.detectionCon=detectionCon
        self.trackCon=trackCon

        self.mpDraw=mp.solutions.drawing_utils
        self.mpPose=mp.solutions.pose
        self.pose=self.mpPose.Pose(self.mode,self.complexity,self.smooth,self.smooth_segmentation,self.detectionCon,self.trackCon)
        


    def findPose(self,frame,draw=True):
        #frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        self.results=self.pose.process(frame)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(frame,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
        return frame

    def findPosition(self,frame,draw=True):
        self.lmlist=[]
        if self.results.pose_landmarks:
            for id,lm in enumerate(self.results.pose_landmarks.landmark):
                #print(id,lm)
                h,w,c=frame.shape
                cx,cy= int(lm.x*w),int(lm.y*h)
                self.lmlist.append([id,cx,cy])
                if draw:
                    cv2.circle(frame,(cx,cy),15,(0,255,0),cv2.FILLED)
        return self.lmlist


    def findAngle(self,frame,p1 ,p2 ,p3 ,draw=True):

        x1,y1 =self.lmlist[p1][1:]
        x2,y2=self.lmlist[p2][1:]
        x3,y3=self.lmlist[p3][1:]


        angle=math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))
        if angle<0:
            angle=angle+360
        #print(angle)

        if draw:
            cv2.line(frame,(x1,y1),(x2,y2),(255,255,255),3)
            cv2.line(frame,(x3,y3),(x2,y2),(255,255,255),3)
            cv2.circle(frame,(x1,y1),10,(255,0,0),cv2.FILLED)
            cv2.circle(frame,(x1,y1),15,(255,0,0),2)
            cv2.circle(frame,(x2,y2),10,(255,0,0),cv2.FILLED)
            cv2.circle(frame,(x2,y2),15,(255,0,0),2)
            cv2.circle(frame,(x3,y3),10,(255,0,0),cv2.FILLED)
            cv2.circle(frame,(x3,y3),15,(255,0,0),2)
            #cv2.putText(frame,str(int(angle)),(x2-50,y2+40),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
        
        return angle


    
def main(): 
    cap=cv2.VideoCapture('/home/akhan/Downloads/football.mp4')
    ptime=0
    ctime=0
    detector=poseDetector()
    while True:
        ret,frame =cap.read()
        frame=detector.findPose(frame) 
        lmlist=detector.findPosition(frame,draw=False)
        #print(lmlist[14])
        cv2.circle(frame,(lmlist[14][1],lmlist[14][2]),15,(255,0,0),cv2.FILLED)



        ctime=time.time()
        fps=1/(ctime-ptime)
        ptime=ctime
        cv2.putText(frame,str(int(fps)),(70,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

        cv2.imshow('video',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()





if __name__ =='__main__' :
    main()