import mediapipe as mp
import cv2 
import math

mp_facemesh=mp.solutions.face_mesh
mp_drawing=mp.solutions.drawing_utils
face_mesh=mp_facemesh.FaceMesh()

def distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

video=cv2.VideoCapture(0)
while True:
    suc,img=video.read()
    img1=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result=face_mesh.process(img1)
    if result.multi_face_landmarks:
        for x in result.multi_face_landmarks:
            mp_drawing.draw_landmarks(img,x,mp_facemesh.FACEMESH_TESSELATION)
            landmarks = x.landmark

            mouth_width = distance(landmarks[61], landmarks[291])
            mouth_open = distance(landmarks[13], landmarks[14])
            left_brow_eye = distance(landmarks[65], landmarks[159])
            right_brow_eye = distance(landmarks[295], landmarks[386])
            avg_brow_eye = (left_brow_eye + right_brow_eye) / 2
            left_eye_open = distance(landmarks[159], landmarks[145])
            right_eye_open = distance(landmarks[386], landmarks[374])
            avg_eye_open = (left_eye_open + right_eye_open) / 2
            if mouth_open > 0.03 and avg_eye_open > 0.02:
                emotion = "Surprised "
            elif mouth_width > 0.08:
                emotion = "Happy "
            elif avg_eye_open < 0.015:
                emotion = "Sad "
            elif mouth_open > 0.05 and avg_eye_open > 0.03 and avg_brow_eye > 0.03:
                emotion = "Fear "
            elif avg_brow_eye < 0.025 and avg_eye_open < 0.03:
                emotion = "Angry 😠"
            else:
                emotion = "Neutral "
            cv2.putText(img, emotion, (30,50),cv2.FONT_HERSHEY_SIMPLEX,1, (0,255,0), 2)
    
    cv2.imshow("Face Emotion", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()