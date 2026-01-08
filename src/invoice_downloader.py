import os
import io
import base64
from datetime import datetime
from googleapiclient.http import MediaIoBaseDownload

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


def download_gdrive_files(service, files, output_dir):
    if not files:
        print("No Drive files to download.")
        return

    for each in files:
        file_id = each.get("id")
        file_name = each.get("name")

        if not file_id or not file_name:
            print(f"Skipping invalid entry: {each}")
            continue

        try:
            request = service.files().get_media(fileId=file_id)
            #file_data = request.execute()

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            safe_filename = f"{timestamp}_{file_name}"
            file_path = os.path.join(output_dir, safe_filename)

            #with open(file_path, "wb") as out_f:
            #    out_f.write(file_data)

            with open(file_path, "wb") as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while not done:
                    _, done = downloader.next_chunk()

            print(f"Saved: {file_path}")
        except Exception as e:
            print(f"Failed to download {file_id} ({file_name}): {e}")

    