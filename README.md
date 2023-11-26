# Virtual Keyboard

## Overview

The Virtual Keyboard is a hand-tracking-based keyboard that allows users to type without the need for a physical keyboard. The system utilizes computer vision techniques to track hand movements and interpret gestures to generate keyboard inputs. It provides an innovative and interactive way of typing, making it accessible for a variety of applications, from basic text editors to web browsers.

## Features

### Hand Tracking

The project leverages the `mediapipe` library for hand tracking. The system can detect and track the position of multiple hands in real-time using the computer's webcam. This forms the foundation for interpreting gestures for typing.

### Gesture-Based Typing

Users can type by hovering their hand over virtual keys displayed on the screen. The system detects the movement of the index and middle fingers to interpret gestures for key selection. Bringing these fingers close to each other simulates pressing a key, providing a unique and intuitive way to input text.

### Dynamic Virtual Keyboard Layout

The virtual keyboard layout is dynamic and adapts to the user's hand movements. The keys are displayed on the screen, and the system highlights the selected key as the user hovers their hand over it. This dynamic interaction provides visual feedback to the user, enhancing the typing experience.

### Real-time Feedback

The system provides real-time feedback, displaying the pressed keys on the screen. Users can see the characters they are typing, enhancing the user experience and confirming successful inputs.

## Getting Started

### Prerequisites

Ensure you have the required Python libraries installed:

```bash
pip install opencv-python
pip install mediapipe
pip install pynput
```

* **JanakiRaman** - *IT Core student* - [JanakiRaman](https://github.com/Janakiraman1021)