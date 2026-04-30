import cv2
import mediapipe as mp
import pyautogui
import time
import math


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
last_action_time = 0
cooldown = 1.0  
print("Starting Air Dashboard MVP... Pinch your index and thumb to trigger Spacebar.")

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
         
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            
            h, w, c = img.shape
            thumb_x, thumb_y = int(hand_landmarks.landmark[4].x * w), int(hand_landmarks.landmark[4].y * h)
            index_x, index_y = int(hand_landmarks.landmark[8].x * w), int(hand_landmarks.landmark[8].y * h)

            cv2.circle(img, (thumb_x, thumb_y), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (index_x, index_y), 10, (255, 0, 255), cv2.FILLED)


            length = math.hypot(index_x - thumb_x, index_y - thumb_y)

            
            if length < 30:
                current_time = time.time()
                if current_time - last_action_time > cooldown:
                    print("Pinch Detected! Triggering Spacebar...")
                    pyautogui.press('space')
                    last_action_time = current_time

    cv2.imshow("Air Dashboard Engine", img)

  
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()