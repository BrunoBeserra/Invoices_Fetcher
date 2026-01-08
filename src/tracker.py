import json
import os

def load_processed_email_ids(filepath):
    if not os.path.exists(filepath):
        return set()

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    return set(data.get("processed_message_ids", []))

def save_processed_email_id(filepath, message_id):
    data = {"processed_message_ids": []}

    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

    if message_id not in data["processed_message_ids"]:
        data["processed_message_ids"].append(message_id)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

def load_processed_files_ids(filepath):
    if not os.path.exists(filepath):
        return set()

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    return set(data.get("processed_files_ids", []))

def save_processed_files_id(filepath, message_id):
    data = {"processed_files_ids": []}

    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

    if message_id not in data["processed_files_ids"]:
        data["processed_files_ids"].append(message_id)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)