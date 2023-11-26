import cv2
import mediapipe as mp
import numpy as np

# Function to check if a point is inside a rectangle
def point_inside_rect(point, rect):
    x, y, w, h = rect
    return x < point[0] < x + w and y < point[1] < y + h

# Function to change the transparency of a key
def change_transparency(frame, key_rect, transparency):
    x, y, w, h = key_rect
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 255, 0), -1)  # Green rectangle as an example
    cv2.addWeighted(overlay, transparency, frame, 1 - transparency, 0, frame)

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Open webcam
cap = cv2.VideoCapture(0)

# Define the QWERTY layout for the virtual keyboard
keyboard_layout = [
    '1234567890',
    'qwertyuiop',
    'asdfghjkl',
    'zxcvbnm'
]

# Calculate the size of each key based on the screen size
screen_width, screen_height = 800, 600  # Set your desired screen resolution
key_width = screen_width // 10  # Adjust the number of keys per row as needed
key_height = screen_height // len(keyboard_layout)

# Flag to track whether the user is clicking
clicking = False

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        continue

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the BGR image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and detect hands
    results = hands.process(rgb_frame)

    # Check if hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the index finger tip location
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Convert landmark to pixel coordinates
            h, w, c = frame.shape
            index_px = (int(index_tip.x * w), int(index_tip.y * h))

            # Check if the index finger is over a key and change transparency
            for row_idx, row in enumerate(keyboard_layout):
                for col_idx, key in enumerate(row):
                    key_rect = (col_idx * key_width, row_idx * key_height, key_width, key_height)
                    if point_inside_rect(index_px, key_rect):
                        change_transparency(frame, key_rect, 0.25)  # Set transparency to 0.25 for the key
                        clicking = True
                    else:
                        change_transparency(frame, key_rect, 1.0)  # Set transparency back to 1.0 if not over the key

    # Check for mouse click event
    if clicking and cv2.waitKey(1) & 0xFF == ord('c'):
        clicking = False
        print("Mouse Click!")

    # Display the frame
    cv2.imshow("Virtual Keyboard", frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
