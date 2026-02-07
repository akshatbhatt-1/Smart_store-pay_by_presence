import json
from datetime import datetime

OUTPUT_FILE = "face_output.json"

def write_face_output(employee_id, confidence):
    event = {
        "employee_id": employee_id,
        "confidence": round(float(confidence), 2),

        "timestamp": datetime.now().isoformat()
    }

    try:
        with open(OUTPUT_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(event)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)
