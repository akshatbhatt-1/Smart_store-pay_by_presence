import sys
import os

# add project root (INNOVATION_MARATHON) to Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)

import cv2
import numpy as np
import insightface
import time
from initialize_camera import initialize_camera
from embedding_store import load_embeddings
from face_output_writer import write_face_output


# ---------------- CONFIG ----------------
THRESHOLD = 0.6
PROCESS_EVERY_N_FRAMES = 5        # frame skipping
WRITE_INTERVAL_SEC = 2            # limit JSON writes
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
# ---------------------------------------

frame_count = 0
last_written_id = None
last_write_time = 0
SHOW_UI = True
WINDOW_NAME = "Face"

# Load saved embeddings
db = load_embeddings()
if not db:
    print("❌ No embeddings found. Enroll first.")
    exit()

# Load InsightFace model (Pi optimized)
app = insightface.app.FaceAnalysis(
    name="buffalo_s",
    providers=["CPUExecutionProvider"]
)
app.prepare(ctx_id=0, det_size=(416, 416))

#cap = cv2.VideoCapture(1)

cap = initialize_camera(5)

if cap is None:
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 15)

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
# cap.set(cv2.CAP_PROP_FPS, 15)


def cosine_similarity(a, b):
    return float(np.dot(a, b))


print("✅ Real-time face recognition started (ESC to exit)")
key = cv2.waitKey(1) & 0xFF
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1

    # -------- FRAME SKIPPING --------
    if frame_count % PROCESS_EVERY_N_FRAMES != 0 :
        if SHOW_UI:
            cv2.imshow(WINDOW_NAME, frame)
                # needed for OpenCV GUI to update
        cv2.waitKey(1)

        # if user clicks the ❌ button
        if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1 or key == 27:
            print("1111Window closed by user")
            break

            continue

    # Resize frame (speed boost)
    frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

    faces = app.get(frame)

    for face in faces:
        emb = face.normed_embedding

        best_id = "UNKNOWN"
        best_score = 0.0

        for emp_id, db_emb in db.items():
            score = cosine_similarity(emb, db_emb)
            if score > best_score:
                best_score = score
                best_id = emp_id

        if best_score < THRESHOLD:
            best_id = "UNKNOWN"

        # -------- OUTPUT THROTTLING --------
        now = time.time()
        if (
            best_id != "UNKNOWN"
            and best_score >= THRESHOLD
            and (
                best_id != last_written_id
                or now - last_write_time > WRITE_INTERVAL_SEC
            )
        ):
            write_face_output(best_id, best_score)
            last_written_id = best_id
            last_write_time = now




        if best_id == last_written_id:
            continue





        # -------- VISUALIZATION --------
        x1, y1, x2, y2 = face.bbox.astype(int)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.putText(
            frame,
            f"{best_id} ({best_score:.2f})",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

    if SHOW_UI:
        cv2.imshow(WINDOW_NAME, frame)

            # needed for OpenCV GUI to update
    cv2.waitKey(1)

    # if user clicks the ❌ button
    if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1 or key == 27:
        print("Window closed by user")
        break


cap.release()
cv2.destroyAllWindows()
