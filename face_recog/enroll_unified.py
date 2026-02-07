import sys
import os

# add project root (INNOVATION_MARATHON) to Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)
import cv2
import numpy as np
import insightface
import os
from embedding_store import save_embedding
from initialize_camera import initialize_camera

# ---------------- CONFIG ----------------
MODEL_NAME = "buffalo_s"
REQUIRED_SAMPLES = 5

# ----------------------------------------
SHOW_UI = False

# Load InsightFace
app = insightface.app.FaceAnalysis(
    name=MODEL_NAME,
    providers=["CPUExecutionProvider"]
)
app.prepare(ctx_id=0, det_size=(640, 640))


def extract_embedding(frame):
    faces = app.get(frame)
    if len(faces) == 1:
        return faces[0].normed_embedding
    return None


def enroll_from_images(folder):
    embeddings = []
    for file in os.listdir(folder):
        if file.lower().endswith((".jpg", ".png", ".jpeg")):
            img = cv2.imread(os.path.join(folder, file))
            emb = extract_embedding(img)
            if emb is not None:
                embeddings.append(emb)
                print(f"Captured from {file}")
        if len(embeddings) >= REQUIRED_SAMPLES:
            break
    return embeddings


def enroll_from_video(path):
    embeddings = []
    cap = cv2.VideoCapture(path)

    while cap.isOpened() and len(embeddings) < REQUIRED_SAMPLES:
        ret, frame = cap.read()
        if not ret:
            break

        emb = extract_embedding(frame)
        if emb is not None:
            embeddings.append(emb)
            print(f"Captured {len(embeddings)}/{REQUIRED_SAMPLES}")

        if SHOW_UI:
            cv2.imshow("1D - Face Recognition", frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    return embeddings


def enroll_from_camera():
    embeddings = []
    cap = initialize_camera(5)

    if cap is None:
        exit()

    print("Press SPACE to capture, ESC to exit")

    while len(embeddings) < REQUIRED_SAMPLES:
        ret, frame = cap.read()
        if not ret:
            break

        faces = app.get(frame)
        if len(faces) == 1:
            x1, y1, x2, y2 = faces[0].bbox.astype(int)
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)

        cv2.putText(
            frame,
            f"Captured {len(embeddings)}/{REQUIRED_SAMPLES}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )

        cv2.imshow("1D - Face Recognition", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == 32 and len(faces) == 1:
            embeddings.append(faces[0].normed_embedding)
            print("Captured")
        
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    return embeddings


# ---------------- MAIN ----------------

employee_id = input("Enter Employee ID: ")

print("\nSelect input type:")
print("1 - Image folder")
print("2 - Video file")
print("3 - Live camera")

choice = input("Enter choice (1/2/3): ")

if choice == "1":
    folder = input("Enter image folder path: ")
    embeddings = enroll_from_images(folder)

elif choice == "2":
    video = input("Enter video file path: ")
    embeddings = enroll_from_video(video)

elif choice == "3":
    embeddings = enroll_from_camera()

else:
    print("Invalid choice")
    exit()

# ---------- SAVE FINAL EMBEDDING ----------

if len(embeddings) >= REQUIRED_SAMPLES:
    final_embedding = np.mean(embeddings, axis=0)
    final_embedding /= np.linalg.norm(final_embedding)
    save_embedding(employee_id, final_embedding)
    print("✅ Enrollment successful. Embedding saved.")
else:
    print("❌ Enrollment failed. Not enough valid samples.")
