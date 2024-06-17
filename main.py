import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands= mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
tipid = [4,8,12,16,20]
passliste =[]

while True:
    success ,img =cap.read()
    img =cv2.flip(img, 1)

    imgRgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #badil min bgr to rbg bich inajim ya3mil analyse li sora
    results = hands.process(imgRgb)
    
    lmlist= []
    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:
            for id,lm, in enumerate(handlms.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x * w), int(lm.y * h) # i7dathiyat points of hands
                lmlist.append([id, cx,cy])
                mpDraw.draw_landmarks(img,handlms,mpHands.HAND_CONNECTIONS)
                if id == 8:
                    cv2.circle(img,(cx,cy),10,(0,255,0),cv2.FILLED) # green circle in point 8 of hand
                if len(lmlist) == 21:
                  fingers =[]
                  if lmlist[tipid[0]][1] < lmlist[tipid[0]-2][1]:
                          fingers.append(1)
                  else:
                      fingers.append(0)

                  for i in range(1,5):
                      if lmlist[tipid[i]][2] < lmlist[tipid[i]-2][2]:
                          fingers.append(1)
                      else:
                       fingers.append(0)
          
                  totalfinger =fingers.count(1)
                  print(totalfinger)
                  cv2.putText(img,f'{totalfinger}',(30,50),cv2.FONT_HERSHEY_SIMPLEX,
                               1.5, (0,0,255),3)
                  res =1234
                  
                  passliste.append(totalfinger)
                  ch = ''.join(str(x) for x in passliste)
                  cv2.putText(img,f'{ch}',(80,90),cv2.FONT_HERSHEY_SIMPLEX,
                               1.5, (0,0,255),3)

                          

    cv2.imshow("hand tracker",img)
    if cv2.waitKey(5) and 0xff ==27:
        break
