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
            # Get the index and thumb finger tip locations
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            # Convert landmarks to pixel coordinates
            h, w, c = frame.shape
            index_px = (int(index_tip.x * w), int(index_tip.y * h))
            thumb_px = (int(thumb_tip.x * w), int(thumb_tip.y * h))

            # Define the virtual keyboard keys (rectangles) - Adjust as needed
            key_a_rect = (50, 50, 50, 50)  # Example key 'A' rectangle (x, y, width, height)
            key_b_rect = (110, 50, 50, 50)  # Example key 'B' rectangle

            # Check if the index finger is over a key and change transparency
            if point_inside_rect(index_px, key_a_rect):
                change_transparency(frame, key_a_rect, 0.5)  # Set transparency to 0.5 for key 'A'
            else:
                change_transparency(frame, key_a_rect, 1.0)  # Set transparency back to 1.0 if not over key 'A'

            if point_inside_rect(index_px, key_b_rect):
                change_transparency(frame, key_b_rect, 0.5)  # Set transparency to 0.5 for key 'B'
            else:
                change_transparency(frame, key_b_rect, 1.0)  # Set transparency back to 1.0 if not over key 'B'

    # Display the frame
    cv2.imshow("Virtual Keyboard", frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
