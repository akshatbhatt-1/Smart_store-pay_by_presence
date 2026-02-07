import sys
import os

# add project root (INNOVATION_MARATHON) to Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)

import cv2
import numpy as np
import insightface
from initialize_camera import initialize_camera
from embedding_store import load_embeddings
from face_output_writer import write_face_output

SHOW_UI = False

# Threshold for recognition
THRESHOLD = 0.6
frame_count = 0
PROCESS_EVERY_N_FRAMES = 3

# Load saved embeddings
db = load_embeddings()
if not db:
    print("❌ No embeddings found. Enroll first.")
    exit()

# Load InsightFace model
app = insightface.app.FaceAnalysis(
    name="buffalo_l",
    providers=["CPUExecutionProvider"]
)
app.prepare(ctx_id=0, det_size=(640, 640))

cap = initialize_camera(5)

if cap is None:
    exit()


def cosine_similarity(a, b):
    return np.dot(a, b)

print("✅ Real-time face recognition started (ESC to exit)")

while True:
    ret, frame = cap.read()
    if not ret:
        break

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
                # Send output to Part 3 / Final system
        if best_id != "UNKNOWN" and best_score >= THRESHOLD:
            write_face_output(best_id, best_score)


        x1, y1, x2, y2 = face.bbox.astype(int)
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)

        cv2.putText(
            frame,
            f"{best_id} ({best_score:.2f})",
            (x1, y1-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

    if SHOW_UI:
       cv2.imshow("1D - Face Recognition", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
