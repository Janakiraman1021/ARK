import cv2
import mediapipe as mp
from time import sleep
from pynput import keyboard
from pynput.keyboard import Controller

class Button:
    def __init__(self, pos, text, size=[60, 60]):
        self.pos = pos
        self.size = size
        self.text = text

class VirtualKeyboard:
    def __init__(self, width=600, height=700):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(3, width)
        self.cap.set(4, height)

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=2)

        self.keyboard_ctrl = Controller()

        self.keys = [
            ["Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"],
            ["~", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "="],
            ["Tab", "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]", "\\"],
            ["CL", "A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "Enter"],
            ["Shift", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "Shift"],
            ["Ctl", "Win", "Alt", " ", "Alt", "Ctl"]
        ]

        self.finalText = ""
        self.buttonList = []

        for i in range(len(self.keys)):
            for j, key in enumerate(self.keys[i]):
                self.buttonList.append(Button([60 * j, 60 * i], key))

    def process_keys(self, index_px, button):
        x, y = button.pos
        w, h = button.size

        distance = abs(index_px[0] - x) + abs(index_px[1] - y)

        if x < index_px[0] < x + w and y < index_px[1] < y + h:
            cv2.rectangle(self.img, (x, y), (x + w, y + h), (0 , 85 , 255), 2)  # Green borders
            cv2.putText(self.img, button.text, (x + 5, y + 40),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0 , 85 , 255), 2)

            if distance < 30:
                self.press_key(button)

    def press_key(self, button):
        spcl_keys = ["Esc", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"]

        if button.text == "Tab":
            self.keyboard_ctrl.press(keyboard.Key.tab)
        elif button.text == "CapsLock":
            self.keyboard_ctrl.press(keyboard.Key.caps_lock)
        elif button.text == "Shift":
            self.keyboard_ctrl.press(keyboard.Key.shift)
        elif button.text == "Ctrl":
            self.keyboard_ctrl.press(keyboard.Key.ctrl)
        elif button.text == "Alt":
            self.keyboard_ctrl.press(keyboard.Key.alt)
        elif button.text == "Win":
            self.keyboard_ctrl.press(keyboard.Key.cmd)
        elif button.text == "Enter":
            self.keyboard_ctrl.press(keyboard.Key.enter)
        elif button.text == "Backspace":
            self.keyboard_ctrl.press(keyboard.Key.backspace)
        elif button.text in spcl_keys:
            pass
        else:
            self.keyboard_ctrl.press(button.text)

        self.finalText += button.text
        sleep(0.25)

    def draw_keys(self):
        for button in self.buttonList:
            x, y = button.pos
            w, h = button.size
            cv2.rectangle(self.img, (x, y), (x + w, y + h), (8, 0, 255), 2)  # Green borders
            cv2.putText(self.img, button.text, (x + 5, y + 40),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0 , 85 , 255), 2)

    def display_pressed_keys(self):
        cv2.rectangle(self.img, (10, 550), (590, 690), (175, 0, 175), cv2.FILLED)
        cv2.putText(self.img, self.finalText, (20, 640),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

    def run(self):
        while True:
            success, self.img = self.cap.read()
            img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            results = self.hands.process(img_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    for button in self.buttonList:
                        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                        index_px = (int(index_tip.x * self.img.shape[1]), int(index_tip.y * self.img.shape[0]))
                        self.process_keys(index_px, button)

            # Draw keys with green borders
            self.draw_keys()

            # Display pressed keys
            self.display_pressed_keys()

            cv2.imshow("Virtual Keyboard", self.img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

# Create an instance of VirtualKeyboard and run it
virtual_keyboard = VirtualKeyboard()
virtual_keyboard.run()
