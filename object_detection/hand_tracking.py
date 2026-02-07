import sys
import os

# add project root (INNOVATION_MARATHON) to Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)
import cv2
import mediapipe as mp
import numpy as np
import time

from initialize_camera import initialize_camera
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# ---------------- RUNNING MODE (THIS FIXES YOUR ERROR) ----------------
options = vision.HandLandmarkerOptions(
    base_options=python.BaseOptions(
        model_asset_path="object_detection\hand_landmarker.task"
    ),
    running_mode=vision.RunningMode.VIDEO,   # IMPORTANT
    num_hands=2,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5,
)

detector = vision.HandLandmarker.create_from_options(options)


# ----------- HAND CONNECTIONS -----------
HAND_CONNECTIONS = [
    (0,1),(1,2),(2,3),(3,4),
    (0,5),(5,6),(6,7),(7,8),
    (5,9),(9,10),(10,11),(11,12),
    (9,13),(13,14),(14,15),(15,16),
    (13,17),(17,18),(18,19),(19,20),
    (0,17)
]


def draw_landmarks(frame, result):
    h, w, _ = frame.shape

    if result.hand_landmarks:
        for hand in result.hand_landmarks:
            pts = []

            for lm in hand:
                x = int(lm.x * w)
                y = int(lm.y * h)
                pts.append((x, y))
                cv2.circle(frame, (x, y), 5, (0,255,0), -1)

            for s, e in HAND_CONNECTIONS:
                cv2.line(frame, pts[s], pts[e], (255,0,0), 2)

    return frame


# ---------------- WEBCAM ----------------
cap = initialize_camera(5)

if cap is None:
    exit()


if not cap.isOpened():
    print("Camera not found. Try changing 0 to 1.")
    exit()

prev = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB,
        data=rgb
    )

    timestamp = int(time.time() * 1000)

    # THIS NOW MATCHES VIDEO MODE
    result = detector.detect_for_video(mp_image, timestamp)

    frame = draw_landmarks(frame, result)

    # FPS
    now = time.time()
    fps = 1/(now-prev) if prev else 0
    prev = now

    cv2.putText(frame, f"FPS: {int(fps)}", (10,30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

    cv2.imshow("MediaPipe Hands", frame) 
        # needed for OpenCV GUI to update
    cv2.waitKey(1)
    WINDOW_NAME = "MediaPipe Hands"

    # if user clicks the ❌ button
    if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
        print("Window closed by user")
        break

cap.release()
cv2.destroyAllWindows()
