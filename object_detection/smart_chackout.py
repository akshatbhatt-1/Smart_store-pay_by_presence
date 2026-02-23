# # import cv2
# import time
import sys
import os

# add project root (INNOVATION_MARATHON) to Python path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)
import cv2
import time

from tracker import Tracker
from initialize_camera import initialize_camera
from config_loader import load_config
from transaction_logger import TransactionLogger
from shelf_memory import ShelfMemory

from core.arduino_weight import ArduinoWeightReceiver
from core.fusion_engine import FusionEngine


# ---------------- LOAD CONFIG ----------------
config = load_config()

known_weights = config["known_weights"]
tolerance = config["weight_tolerance"]

# ---------------- INIT MODULES ----------------
tracker = Tracker(
    imgsz=config["yolo_imgsz"],
    conf=config["yolo_conf"]
)

cap = initialize_camera(config["camera_name"])

receiver = ArduinoWeightReceiver(port="COM5")
fusion = FusionEngine(known_weights, tolerance)

logger = TransactionLogger()
shelf_memory = ShelfMemory()

print("SMART CHECKOUT SYSTEM STARTED (Weight-Primary Mode)")

# ---------------- HAND ACTIVITY TRACKING ----------------
last_hand_time = 0
hand_timeout = 1.5  # seconds

# ---------------- MAIN LOOP ----------------
while True:

    ret, frame = cap.read()
    if not ret:
        break

    tracker_data = tracker.process(frame)

    # ---------------- DETECT HAND INTERACTION ----------------
    if tracker_data.get("hands"):
        last_hand_time = time.time()

    hand_active = (time.time() - last_hand_time) < hand_timeout

    # ---------------- DRAW OBJECTS ----------------
    # ---------------- DRAW OBJECTS ----------------
    for obj in tracker_data.get("objects", []):
        x1, y1, x2, y2 = obj["bbox"]
        label = obj["label"]

        cv2.rectangle(frame, (x1, y1), (x2, y2),
                    (0, 255, 0), 2)

        cv2.putText(frame, label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2)

    # ---------------- DRAW HAND ----------------
    hand_bbox = tracker_data.get("hand_bbox")

    if hand_bbox:
        x1, y1, x2, y2 = hand_bbox

        cv2.rectangle(frame, (x1, y1), (x2, y2),
                    (255, 0, 0), 3)

        cv2.putText(frame, "HAND",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 0, 0),
                    2)

        last_hand_time = time.time()

    hand_active = (time.time() - last_hand_time) < 1.5
    # ---------------- READ DROP ----------------
    drop = receiver.read_drop()

    if drop:
        print("DROP RECEIVED:", drop)

        if hand_active:
            result = fusion.process_drop(drop)

            if result:
                print("CONFIRMED:", result.item, "Qty:", result.quantity)

                for _ in range(result.quantity):
                    shelf_memory.register_pickup(result.item)
                    logger.log_removal(
                        item=result.item,
                        confidence=0.99,
                        weight=drop
                    )

                cv2.putText(frame,
                            f"CONFIRMED {result.item} x{result.quantity}",
                            (50, 80),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 255, 0),
                            3)
            else:
                print("DROP IGNORED (no weight match)")
        else:
            print("DROP IGNORED (no hand activity)")

    cv2.imshow("SMART CHECKOUT", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# ---------------- CLEANUP ----------------
cap.release()
receiver.close()
cv2.destroyAllWindows()


# import cv2
# import time

# from tracker import Tracker
# from initialize_camera import initialize_camera
# from config_loader import load_config
# from transaction_logger import TransactionLogger
# from shelf_memory import ShelfMemory

# from core.arduino_weight import ArduinoWeightReceiver
# from core.fusion_engine import FusionEngine


# # ---------------- LOAD CONFIG ----------------
# config = load_config()

# known_weights = config["known_weights"]
# tolerance = config["weight_tolerance"]

# # ---------------- INIT MODULES ----------------
# tracker = Tracker(
#     imgsz=config["yolo_imgsz"],
#     conf=config["yolo_conf"]
# )

# cap = initialize_camera(config["camera_name"])

# receiver = ArduinoWeightReceiver(port="COM5")
# fusion = FusionEngine(known_weights, tolerance)

# logger = TransactionLogger()
# shelf_memory = ShelfMemory()

# print("SMART CHECKOUT SYSTEM STARTED (Weight-Primary Mode)")

# # ---------------- HAND ACTIVITY TRACKING ----------------
# last_hand_time = 0
# hand_timeout = 1.5  # seconds


# # ---------------- MAIN LOOP ----------------
# while True:

#     ret, frame = cap.read()
#     if not ret:
#         break

#     tracker_data = tracker.process(frame)
#     # print(tracker_data.keys())

#     # ---------------- DRAW OBJECTS ----------------
#     for obj in tracker_data.get("objects", []):
#         x1, y1, x2, y2 = obj["bbox"]
#         label = obj["label"]

#         cv2.rectangle(frame, (x1, y1), (x2, y2),
#                       (0, 255, 0), 2)

#         cv2.putText(frame, label,
#                     (x1, y1 - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.6,
#                     (0, 255, 0),
#                     2)

#     # ---------------- DRAW HANDS ----------------
#     # ---------------- DRAW HAND ----------------
#     hand_bbox = tracker_data.get("hand_bbox")

#     if hand_bbox:
#         x1, y1, x2, y2 = hand_bbox

#         cv2.rectangle(frame, (x1, y1), (x2, y2),
#                     (255, 0, 0), 2)

#         cv2.putText(frame, "HAND",
#                     (x1, y1 - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX,
#                     0.6,
#                     (255, 0, 0),
#                     2)

#         last_hand_time = time.time()
#     # ---------------- READ DROP FROM ARDUINO ----------------
#     drop = receiver.read_drop()
#     hand_active = (time.time() - last_hand_time) < 1.5
#     if drop:
#         print("DROP RECEIVED:", drop)

#         if hand_active:

#             result = fusion.process_drop(drop)

#             if result:
#                 print("CONFIRMED:", result.item, "Qty:", result.quantity)

#                 for _ in range(result.quantity):
#                     shelf_memory.register_pickup(result.item)
#                     logger.log_removal(
#                         item=result.item,
#                         confidence=0.99,
#                         weight=drop
#                     )

#                 cv2.putText(frame,
#                             f"CONFIRMED {result.item} x{result.quantity}",
#                             (50, 80),
#                             cv2.FONT_HERSHEY_SIMPLEX,
#                             1,
#                             (0, 255, 0),
#                             3)

#             else:
#                 print("DROP IGNORED (no weight match)")

#         else:
#             print("DROP IGNORED (no hand activity)")

#     cv2.imshow("SMART CHECKOUT", frame)

#     if cv2.waitKey(1) & 0xFF == 27:
#         break


# # ---------------- CLEANUP ----------------
# cap.release()
# receiver.close()
# cv2.destroyAllWindows()