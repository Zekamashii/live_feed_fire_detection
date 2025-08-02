import os
import threading
import time

import cv2
import numpy as np
import playsound

# Global flags to track alarm and fire detection status
Alarm_Status = False
Fire_Reported = 0

# Path to the alarm sound file (must be in the same directory or provide full path)
ALARM_SOUND_PATH = 'alarm-sound.mp3'

# Cross-platform absolute path to the folder where drone videos are saved
# This uses the user's home directory and appends the standard Videos/DroneFeed path
VIDEO_FOLDER_PATH = os.path.join(os.path.expanduser("~"), "Videos", "DroneFeed")


def play_alarm_sound():
    """
    Plays an alarm sound in a separate thread when fire is detected.
    """
    playsound.playsound(ALARM_SOUND_PATH, False)
    time.sleep(3)


def detect_fire(frame):
    """
    Detects fire-like colors in the given video frame using HSV color filtering.
    If fire is detected, triggers the alarm sound.
    """
    global Fire_Reported, Alarm_Status

    # Resize frame for consistent processing
    resized_frame = cv2.resize(frame, (960, 540))

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(resized_frame, (21, 21), 0)

    # Convert frame to HSV color space
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Define HSV range for fire-like colors (orange/yellow)
    lower = np.array([18, 50, 50], dtype="uint8")
    upper = np.array([35, 255, 255], dtype="uint8")

    # Create a mask for fire-colored regions
    mask = cv2.inRange(hsv, lower, upper)

    # Apply mask to original frame
    output = cv2.bitwise_and(resized_frame, resized_frame, mask=mask)

    # Count the number of fire-colored pixels
    fire_pixels = cv2.countNonZero(mask)

    # If enough fire-colored pixels are detected, report fire
    if fire_pixels > 15000:
        Fire_Reported += 1
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Fire detected!")

        # Play alarm sound if not already triggered
        if not Alarm_Status:
            threading.Thread(target=play_alarm_sound).start()
            Alarm_Status = True

    # Display the processed frame with fire detection overlay
    cv2.imshow("Fire Detection", output)


def get_latest_video_file(folder):
    """
    Returns the most recently modified video file in the given folder.
    """
    files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith((".mp4", ".avi"))]
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def process_live_video(video_path):
    """
    Continuously reads frames from the given video file and performs fire detection.
    Assumes the file is being written to by another process.
    """
    cap = cv2.VideoCapture(video_path)

    while True:
        ret, frame = cap.read()

        # If no frame is available, wait and try again
        if not ret:
            time.sleep(0.5)
            continue

        # Analyze the current frame for fire
        detect_fire(frame)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()


if __name__ == "__main__":
    # Check if the video folder exists
    if not os.path.exists(VIDEO_FOLDER_PATH):
        print(f"Video folder not found: {VIDEO_FOLDER_PATH}")
    else:
        print("Monitoring folder for live video...")

        # Continuously monitor the folder for the latest video file
        while True:
            latest_file = get_latest_video_file(VIDEO_FOLDER_PATH)
            if latest_file:
                print(f"Analyzing: {latest_file}")
                process_live_video(latest_file)
            else:
                print("No video found. Waiting...")
                time.sleep(2)

    # Clean up OpenCV windows
    cv2.destroyAllWindows()
