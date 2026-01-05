from googleapiclient.discovery import build
from pathlib import Path
import base64

def get_drive_service(creds):
    return build("drive", "v3", credentials=creds)

def list_files_in_folder(service, folder_id):
    query = f"'{folder_id}' in parents and trashed = false"

    results = service.files().list(
        q=query,
        fields="files(id, name, mimeType)"
    ).execute()

    return results.get("files", [])