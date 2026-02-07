import time
import cv2

def initialize_camera(timeout=5):
    print("Searching for camera...")

    start = time.time()
    cap = None

    while time.time() - start < timeout:

        # Try external webcam first
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        if cap.isOpened():
            print("Using external webcam (index 1)")
            return cap

        cap.release()

        # Try laptop webcam
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if cap.isOpened():
            print("Using internal webcam (index 0)")
            return cap

        cap.release()
        time.sleep(0.8)  # retry interval

    print("No camera detected after 5 seconds. Exiting.")
    return None
