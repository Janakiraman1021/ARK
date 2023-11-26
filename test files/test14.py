import cv2
import mediapipe as mp
from time import sleep
from pynput import keyboard
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, 600)  # Set width
cap.set(4, 700)  # Set height

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)

keyboard_ctrl = Controller()

keys = [
    ["Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"],
    ["~", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="],
    ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
    ["CapsLock", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "Enter"],
    ["Shift", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "Shift"],
    ["Ctrl", "Win", "Alt", " ", "Alt", "Ctrl"]
]

finalText = ""

class Button():
    def __init__(self, pos, text, size=[60, 60]):
        self.pos = pos
        self.size = size
        self.text = text

buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([60 * j, 60 * i], key))

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_px = (int(index_tip.x * img.shape[1]), int(index_tip.y * img.shape[0]))
                distance = abs(index_px[0] - button.pos[0]) + abs(index_px[1] - button.pos[1])

                if x < index_px[0] < x + w and y < index_px[1] < y + h:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green borders
                    cv2.putText(img, button.text, (x + 5, y + 40),
                                cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                    spcl_keys = ["Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"]
                    if distance < 30:
                        if button.text == "Tab":
                            keyboard_ctrl.press(keyboard.Key.tab)
                        elif button.text == "CapsLock":
                            keyboard_ctrl.press(keyboard.Key.caps_lock)
                        elif button.text == "Shift":
                            keyboard_ctrl.press(keyboard.Key.shift)
                        elif button.text == "Ctrl":
                            keyboard_ctrl.press(keyboard.Key.ctrl)
                        elif button.text == "Alt":
                            keyboard_ctrl.press(keyboard.Key.alt)
                        elif button.text == "Win":
                            keyboard_ctrl.press(keyboard.Key.cmd)
                        elif button.text == "Enter":
                            keyboard_ctrl.press(keyboard.Key.enter)
                        elif button.text in spcl_keys:
                            pass
                        else:
                            keyboard_ctrl.press(button.text)

                        finalText += button.text
                        sleep(0.25)

    # Draw keys with green borders
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green borders
        cv2.putText(img, button.text, (x + 5, y + 40),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    # Display pressed keys
    cv2.rectangle(img, (10, 550), (590, 690), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (20, 640),
                cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
