# Sample Project - Interview
# Bruno Beserra

# ----------------------------
# --- Gmail Source Library ---
# ----------------------------


# Import Libraries
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os
import base64
from datetime import datetime


def gmail_authenticate(scopes: list, token_path, credentials_path):
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

def get_gmail_service(creds):
    return build("gmail", "v1", credentials=creds)

def search_invoice_emails(service, max_results=20):
    query = (
        "has:attachment "
        "(invoice OR receipt OR bill)"
    )

    result = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=max_results
    ).execute()

    return result.get("messages", [])

# def get_message_metadata(service, message_id):
#     message = service.users().messages().get(
#         userId="me",
#         id=message_id,
#         format="metadata",
#         metadataHeaders=["Subject", "From", "Date"]
#     ).execute()

#     headers = message["payload"]["headers"]
#     return {h["name"]: h["value"] for h in headers}