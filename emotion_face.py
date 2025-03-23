
import os
import numpy as np
kernel = np.array([[0, -1, 0],
                   [-1,  5, -1],
                   [0, -1, 0]])
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Disable GPU usage


import cv2
from deepface import DeepFace
import threading
import os
import webbrowser

def detect_emotion():

    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        print("Error: Webcam not available!")
        return None

    ret, frame = capture.read()
    capture.release()
    cv2.destroyAllWindows()

    if not ret:
        print("Error: Could not capture frame!")
        return None
    frame = cv2.resize(frame, (600, 600), interpolation=cv2.INTER_CUBIC)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    sharp_frame = cv2.filter2D(gray_frame, -1, kernel)

    cv2.imwrite("captured_image.jpg", sharp_frame)

    try:
        result = DeepFace.analyze(img_path="captured_image.jpg",
                                  actions=['emotion'],
                                  detector_backend="retinaface")  # Change model here

        emotion = result[0]['dominant_emotion']
        print(f"Detected Emotion: {emotion}")
        return emotion
    except Exception as e:
        print(f"Error detecting emotion: {e}")
        return None


if __name__ == "__main__":
    print(detect_emotion())
# Call GUI script with song URI


