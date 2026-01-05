import os
import base64
from datetime import datetime

def download_gmail_attachments(service, message_id, output_dir):
    message = service.users().messages().get(
        userId="me",
        id=message_id
    ).execute()

    parts = message["payload"].get("parts", [])

    for part in parts:
        filename = part.get("filename")
        body = part.get("body", {})

        if filename and "attachmentId" in body:
            attachment_id = body["attachmentId"]

            attachment = service.users().messages().attachments().get(
                userId="me",
                messageId=message_id,
                id=attachment_id
            ).execute()

            file_data = base64.urlsafe_b64decode(attachment["data"])

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            safe_filename = f"{timestamp}_{filename}"

            file_path = os.path.join(output_dir, safe_filename)

            with open(file_path, "wb") as f:
                f.write(file_data)
            
            print(f"Saved: {file_path}")
