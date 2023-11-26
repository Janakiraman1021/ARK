import cv2
import mediapipe as mp
from time import sleep
from pynput import keyboard
from pynput.keyboard import Controller

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 640)
cap.set(4, 480)

keyboard_controller = Controller()

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

final_text = ""

class Button:
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


button_list = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        button_list.append(Button([100*j+50, 100*i+50], key))

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for button in button_list:
                x, y = button.pos
                w, h = button.size

                lm_list = hand_landmarks.landmark
                hand_center = (int((lm_list[0].x + lm_list[5].x) * img.shape[1] / 2),
                               int((lm_list[0].y + lm_list[5].y) * img.shape[0] / 2))

                if x < hand_center[0] < x+w and y < hand_center[1] < y+h:
                    cv2.rectangle(img, (x-5, y-5), (x+w+5, y+h+5), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x+20, y+65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    distance = int(
                        abs(lm_list[8].x * img.shape[1] - lm_list[12].x * img.shape[1]))
                    print(distance)

                    if distance < 30:
                        keyboard_controller.press(button.text)
                        cv2.rectangle(img, button.pos, (x+w, y+h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x+20, y+65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        final_text += button.text
                        sleep(0.25)

    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, final_text, (60, 425),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) == 27:  # Press Esc to exit
        break

cap.release()
cv2.destroyAllWindows()
