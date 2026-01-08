from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import base64
from datetime import datetime

def gdrive_authenticate(scopes, token_path, credentials_path):
    creds = None

    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, scopes
            )
            creds = flow.run_local_server(port=0)

        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    return creds

def get_drive_service(creds):
    return build("drive", "v3", credentials=creds)

def list_gdrive_files_in_folder(service, folder_id):
    query = f"'{folder_id}' in parents and trashed = false"

    results = service.files().list(
        q=query,
        fields="files(id, name, mimeType)"
    ).execute()

    return results.get("files", [])