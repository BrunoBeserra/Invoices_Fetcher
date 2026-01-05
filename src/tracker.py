import json
import os

def load_processed_ids(filepath):
    if not os.path.exists(filepath):
        return set()

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    return set(data.get("processed_message_ids", []))

def save_processed_id(filepath, message_id):
    data = {"processed_message_ids": []}

    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

    if message_id not in data["processed_message_ids"]:
        data["processed_message_ids"].append(message_id)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)