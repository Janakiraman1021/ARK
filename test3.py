import cv2
import mediapipe as mp
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QFont, QColor
from pynput.keyboard import Controller
import threading

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

class ARKeyboard(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 800, 200)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        self.final_text = ""
        self.keyboard_controller = Controller()

        keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
                ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

        self.layout = QVBoxLayout(self)

        self.button_list = []
        for i in range(len(keys)):
            for j, key in enumerate(keys[i]):
                button = ARButton([100*j+50, 100*i+50], key, self)
                self.button_list.append(button)
                self.layout.addWidget(button)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_keyboard)
        self.timer.start(50)  # Update every 50 milliseconds

    def update_keyboard(self):
        for button in self.button_list:
            if button.is_pressed:
                self.keyboard_controller.press(button.text)
                button.is_pressed = False

        self.setWindowTitle(self.final_text)

    def keyPressEvent(self, event):
        key = event.text().upper()
        for button in self.button_list:
            if button.text == key:
                button.is_pressed = True
                break

class ARButton(QWidget):
    def __init__(self, pos, text, parent):
        super().__init__(parent)
        self.pos = pos
        self.text = text
        self.is_pressed = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.fillRect(self.rect(), QColor(255, 0, 255))

        font = QFont()
        font.setPointSize(16)
        painter.setFont(font)

        painter.drawText(self.rect(), Qt.AlignCenter, self.text)

class HandTrackingThread(threading.Thread):
    def __init__(self, ar_keyboard):
        super().__init__()
        self.ar_keyboard = ar_keyboard

    def run(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        cap.set(3, 640)  # Set width to 640
        cap.set(4, 480)  # Set height to 480

        while True:
            success, img = cap.read()

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    for button in self.ar_keyboard.button_list:
                        x, y = button.pos
                        w, h = 85, 85  # Assuming fixed size for simplicity

                        lm_list = hand_landmarks.landmark
                        hand_center = (int((lm_list[0].x + lm_list[5].x) * img.shape[1] / 2),
                                       int((lm_list[0].y + lm_list[5].y) * img.shape[0] / 2))

                        if x < hand_center[0] < x+w and y < hand_center[1] < y+h:
                            button.is_pressed = True

            cv2.imshow("AR Keyboard", img)
            if cv2.waitKey(1) == 27:  # Press Esc to exit
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    ar_keyboard = ARKeyboard()
    ar_keyboard.show()

    hand_tracking_thread = HandTrackingThread(ar_keyboard)
    hand_tracking_thread.start()

    sys.exit(app.exec_())
