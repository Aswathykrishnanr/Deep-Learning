import mediapipe as mp
import cv2
mphands=mp.solutions.hands
hand_drawing=mp.solutions.drawing_utils
hand=mphands.Hands(max_num_hands=1)
import pyttsx3
import time

txt_sp = pyttsx3.init()
voice = txt_sp.getProperty('voices')
txt_sp.setProperty('voice', voice[1].id)   # female
txt_sp.setProperty('volume', 0.9)
last_spoken = "Unknown"
last_spoken_time = 0
cooldown = 1.5   # seconds


video=cv2.VideoCapture(0)
gesture_map = {
    (0,0,0,0,0): "Fist",
    (0,1,0,0,0): "One",
    (0,1,1,0,0): "Two",
    (0,1,1,1,0): "Three",
    (0,1,1,1,1): "Four",
    (1,1,1,1,1): "Five",
    (1,0,0,0,0): "Thumbs Up",
    (1,1,0,0,0): "OK",
    (1,0,0,0,1): "Rock",
    (0,1,0,0,1): "Spiderman"
}
while True:
    suc,img=video.read()
    img1=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result=hand.process(img1)
    #print(result.multi_hand_landmarks)
    tip_id=[4,8,12,16,20]
    lm_list=[]
    gesture = "Unknown"
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

                    gesture = gesture_map.get(tuple(finger_count), "Unknown")
                    
                    
            hand_drawing.draw_landmarks(img,handlms,mphands.HAND_CONNECTIONS)

    # -------- SPEECH WITH COOLDOWN --------
    current_time = time.time()
    if gesture != "Unknown" and gesture != last_spoken:
        if current_time - last_spoken_time > cooldown:
            txt_sp.say(gesture)
            txt_sp.runAndWait()
            last_spoken = gesture
            last_spoken_time = current_time

    display_text = f"Gesture: {gesture}"
    cv2.putText(img, display_text, (35, 100),
                cv2.FONT_HERSHEY_COMPLEX, 1.2, (0, 255, 0), 3)

    cv2.imshow("Finger Count", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()