# import json
# import os
# from datetime import datetime

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# LOG_PATH = os.path.join(BASE_DIR, "transactions.json")


# class TransactionLogger:
#     def __init__(self):
#         if not os.path.exists(LOG_PATH):
#             with open(LOG_PATH, "w") as f:
#                 json.dump([], f)

#     def log_removal(self, item, confidence, weight):
#         try:
#             with open(LOG_PATH, "r") as f:
#                 data = json.load(f)
#         except:
#             data = []

#         entry = {
#             "item": item,
#             "confidence": confidence,
#             "weight": round(weight, 2),
#             "timestamp": datetime.now().isoformat()
#         }

#         data.append(entry)

#         with open(LOG_PATH, "w") as f:
#             json.dump(data, f, indent=4)

#         print("Transaction saved:", entry)
import os
import json
from datetime import datetime


class TransactionLogger:

    def __init__(self):

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(BASE_DIR, "data")

        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

        self.file_path = os.path.join(self.data_dir, "transactions.json")

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as f:
                json.dump([], f)

    def log_removal(self, item, confidence, weight):

        with open(self.file_path, "r") as f:
            data = json.load(f)

        entry = {
            "item": item,
            "confidence": confidence,
            "weight": weight,
            "timestamp": datetime.now().isoformat()
        }

        data.append(entry)

        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

        print("Transaction saved:", entry)