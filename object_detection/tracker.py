# import cv2
# import time
# import mediapipe as mp
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision
# from ultralytics import YOLO


# class Tracker:
#     def __init__(self, imgsz=480, conf=0.3):
#         self.imgsz = imgsz
#         self.conf = conf

#         BaseOptions = python.BaseOptions
#         HandLandmarker = vision.HandLandmarker
#         HandLandmarkerOptions = vision.HandLandmarkerOptions
#         VisionRunningMode = vision.RunningMode

#         # CHANGE: use IMAGE mode instead of LIVE_STREAM
#         options = HandLandmarkerOptions(
#             base_options=BaseOptions(
#                 model_asset_path="object_detection/hand_landmarker.task"
#             ),
#             running_mode=VisionRunningMode.IMAGE,
#             num_hands=1
#         )

#         self.hand_landmarker = HandLandmarker.create_from_options(options)
#         self.object_model = YOLO("models/best.pt")

#     def _intersection_area(self, a, b):
#         xA, yA = max(a[0], b[0]), max(a[1], b[1])
#         xB, yB = min(a[2], b[2]), min(a[3], b[3])
#         if xA >= xB or yA >= yB:
#             return 0
#         return (xB - xA) * (yB - yA)
#     def _iou(self, boxA, boxB):
#         xA = max(boxA[0], boxB[0])
#         yA = max(boxA[1], boxB[1])
#         xB = min(boxA[2], boxB[2])
#         yB = min(boxA[3], boxB[3])

#         if xA >= xB or yA >= yB:
#             return 0.0

#         interArea = (xB - xA) * (yB - yA)

#         boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
#         boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

#         return interArea / float(boxAArea + boxBArea - interArea)
#     def _nms(self, objects, iou_threshold=0.5):

#         filtered = []

#         for obj in objects:
#             keep = True
#             for kept in filtered:
#                 if obj["label"] == kept["label"]:
#                     if self._iou(obj["bbox"], kept["bbox"]) > iou_threshold:
#                         keep = False
#                         break
#             if keep:
#                 filtered.append(obj)

#         return filtered
#     def process(self, frame):

#         h, w, _ = frame.shape
#         rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#         mp_image = mp.Image(
#             image_format=mp.ImageFormat.SRGB,
#             data=rgb
#         )

#         # 🔥 CHANGE: synchronous detection
#         result = self.hand_landmarker.detect(mp_image)

#         hand_bbox = None

#         if result.hand_landmarks:
#             pts = [
#                 (int(lm.x * w), int(lm.y * h))
#                 for lm in result.hand_landmarks[0]
#             ]

#             xs = [p[0] for p in pts]
#             ys = [p[1] for p in pts]

#             hand_bbox = [
#                 min(xs) - 20, min(ys) - 20,
#                 max(xs) + 20, max(ys) + 20
#             ]

#         # ---------------- YOLO OBJECT DETECTION ----------------
#         results = self.object_model(
#             frame,
#             imgsz=self.imgsz,
#             conf=self.conf,
#             verbose=False
#         )[0]

#         objects = []

#         for box in results.boxes:
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             cls_id = int(box.cls[0])
#             label = self.object_model.names[cls_id]

#             objects.append({
#                 "bbox": [x1, y1, x2, y2],
#                 "label": label
#             })
#         objects = self._nms(objects, iou_threshold=0.5)
#         overlapping_objects = []

#         if hand_bbox:
#             for obj in objects:
#                 if self._intersection_area(hand_bbox, obj["bbox"]) > 50:
#                     overlapping_objects.append(obj)

#         return {
#             "hand_bbox": hand_bbox,
#             "objects": objects,
#             "overlapping_objects": overlapping_objects
#         }


# # import cv2
# # from ultralytics import YOLO


# # class Tracker:
# #     def __init__(self, imgsz=480, conf=0.3):

# #         self.imgsz = imgsz
# #         self.conf = conf

# #         # Product detection model
# #         self.object_model = YOLO("models/best.pt")

# #         # Pretrained hand detection model
# #         self.hand_model = YOLO("yolov8n.pt")

# #     def _iou(self, boxA, boxB):
# #         xA = max(boxA[0], boxB[0])
# #         yA = max(boxA[1], boxB[1])
# #         xB = min(boxA[2], boxB[2])
# #         yB = min(boxA[3], boxB[3])

# #         if xA >= xB or yA >= yB:
# #             return 0.0

# #         interArea = (xB - xA) * (yB - yA)
# #         boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
# #         boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

# #         return interArea / float(boxAArea + boxBArea - interArea)

# #     def _nms(self, objects, iou_threshold=0.5):
# #         filtered = []

# #         for obj in objects:
# #             keep = True
# #             for kept in filtered:
# #                 if obj["label"] == kept["label"]:
# #                     if self._iou(obj["bbox"], kept["bbox"]) > iou_threshold:
# #                         keep = False
# #                         break
# #             if keep:
# #                 filtered.append(obj)

# #         return filtered

# #     def process(self, frame):

# #         # ---------------- PRODUCT DETECTION ----------------
# #         obj_results = self.object_model(
# #             frame,
# #             imgsz=self.imgsz,
# #             conf=self.conf,
# #             verbose=False
# #         )[0]

# #         objects = []

# #         for box in obj_results.boxes:
# #             x1, y1, x2, y2 = map(int, box.xyxy[0])
# #             cls_id = int(box.cls[0])
# #             label = self.object_model.names[cls_id].lower()

# #             objects.append({
# #                 "bbox": [x1, y1, x2, y2],
# #                 "label": label
# #             })

# #         objects = self._nms(objects, 0.5)

# #         # ---------------- HAND DETECTION ----------------
# #         hand_bbox = None

# #         hand_results = self.hand_model(
# #             frame,
# #             imgsz=320,
# #             conf=0.4,
# #             verbose=False
# #         )[0]

# #         for box in hand_results.boxes:
# #             cls_id = int(box.cls[0])
# #             label = self.hand_model.names[cls_id].lower()

# #             if label == "person":
# #                 x1, y1, x2, y2 = map(int, box.xyxy[0])
# #                 hand_bbox = [x1, y1, x2, y2]
# #                 break

# #         return {
# #             "objects": objects,
# #             "hand_bbox": hand_bbox
# #         }
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from ultralytics import YOLO


class Tracker:
    def __init__(self, imgsz=480, conf=0.3):
        self.imgsz = imgsz
        self.conf = conf

        # -------- HAND DETECTOR (MediaPipe) --------
        BaseOptions = python.BaseOptions
        HandLandmarker = vision.HandLandmarker
        HandLandmarkerOptions = vision.HandLandmarkerOptions
        VisionRunningMode = vision.RunningMode

        options = HandLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path="object_detection/hand_landmarker.task"
            ),
            running_mode=VisionRunningMode.IMAGE,
            num_hands=1
        )

        self.hand_landmarker = HandLandmarker.create_from_options(options)

        # -------- OBJECT DETECTOR (YOLO) --------
        self.object_model = YOLO("models/best.pt")

    def _iou(self, boxA, boxB):
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        if xA >= xB or yA >= yB:
            return 0.0

        interArea = (xB - xA) * (yB - yA)
        boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
        boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

        return interArea / float(boxAArea + boxBArea - interArea)

    def _nms(self, objects, iou_threshold=0.5):
        filtered = []

        for obj in objects:
            keep = True
            for kept in filtered:
                if obj["label"] == kept["label"]:
                    if self._iou(obj["bbox"], kept["bbox"]) > iou_threshold:
                        keep = False
                        break
            if keep:
                filtered.append(obj)

        return filtered

    def process(self, frame):

        h, w, _ = frame.shape

        # -------- HAND DETECTION --------
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb
        )

        result = self.hand_landmarker.detect(mp_image)

        hand_bbox = None

        if result.hand_landmarks:

            pts = [
                (int(lm.x * w), int(lm.y * h))
                for lm in result.hand_landmarks[0]
            ]

            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]

            # Slightly expand box for stability
            pad = 30

            hand_bbox = [
                max(0, min(xs) - pad),
                max(0, min(ys) - pad),
                min(w - 1, max(xs) + pad),
                min(h - 1, max(ys) + pad)
            ]

        # -------- OBJECT DETECTION --------
        results = self.object_model(
            frame,
            imgsz=self.imgsz,
            conf=self.conf,
            verbose=False
        )[0]

        objects = []

        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls_id = int(box.cls[0])
            label = self.object_model.names[cls_id]

            objects.append({
                "bbox": [x1, y1, x2, y2],
                "label": label
            })

        objects = self._nms(objects, 0.5)

        return {
            "hand_bbox": hand_bbox,
            "objects": objects,
            "overlapping_objects": []  # kept for compatibility
        }