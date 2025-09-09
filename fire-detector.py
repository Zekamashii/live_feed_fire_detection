import time

import cv2
import numpy as np

# Global flag to track fire detection status
Fire_Reported = 0


def detect_fire(frame):
    """
    Detects fire-like colors in the given video frame using HSV color filtering.
    """
    global Fire_Reported

    resized_frame = cv2.resize(frame, (720, 480))
    blurred = cv2.GaussianBlur(resized_frame, (21, 21), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # HSV range for fire-like colors
    lower = np.array([18, 50, 50], dtype="uint8")
    upper = np.array([35, 255, 255], dtype="uint8")

    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(resized_frame, resized_frame, mask=mask)
    fire_pixels = cv2.countNonZero(mask)

    if fire_pixels > 15000:
        Fire_Reported += 1
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Fire detected!")

    cv2.imshow("Fire Detection", output)


def process_webcam_feed():
    """
    Captures live video from the default webcam and performs fire detection in real time.
    """
    # cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Use this line for Windows
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("Starting real-time fire detection from webcam...")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame.")
            break

        detect_fire(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    process_webcam_feed()
