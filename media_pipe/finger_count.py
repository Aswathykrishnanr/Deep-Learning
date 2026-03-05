import mediapipe as mp
import cv2
mphands=mp.solutions.hands
hand_drawing=mp.solutions.drawing_utils
hand=mphands.Hands(max_num_hands=1)
video=cv2.VideoCapture(0)
while True:
    suc,img=video.read()
    img1=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result=hand.process(img1)
    #print(result.multi_hand_landmarks)
    tip_id=[4,8,12,16,20]
    lm_list=[]
    if result.multi_hand_landmarks:
        for handlms in result.multi_hand_landmarks:
            for id,lm in enumerate(handlms.landmark):
                lm_list.append([id,lm.x, lm.y])
                #print(lm_list)
                if len(lm_list)!=0 and len(lm_list)==21:
                    finger_count=[]
                    if lm_list[12][1] < lm_list[20][1]:
                        if lm_list[4][1] > lm_list[3][1]:
                            finger_count.append(0)          #closed
                        else:
                            finger_count.append(1)          #open
                    else:
                        if lm_list[4][1] < lm_list[3][1]:
                            finger_count.append(0)
                        else:
                            finger_count.append(1)
                    for i in range(1,5):
                        if lm_list[tip_id[i]][2] > lm_list[tip_id[i]-2][2]:
                         
                            finger_count.append(0)  # closed
                        else:
                            finger_count.append(1)  #open
                    #print(finger_count)
                    #print("Finger state:", finger_count)
                    if len(finger_count)!=0:
                        finger_count1=finger_count.count(1)
                    #print(finger_count1)
                    cv2.putText(img,str(finger_count1),(35,400),cv2.FONT_HERSHEY_COMPLEX,3,(0,0,255))
                    #print("Total fingers:", sum(finger_count))
                
            hand_drawing.draw_landmarks(img,handlms,mphands.HAND_CONNECTIONS)
#index(x,y,z) == ennumerate   
       
    cv2.imshow("Finger Count",img)
    if cv2.waitKey(1) & 0XFF==ord('q'):
        break

video.release()
cv2.destroyAllWindows()


