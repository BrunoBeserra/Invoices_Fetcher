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
import json


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

def load_trusted_senders(filepath):
    if not os.path.exists(filepath):
        return set()

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    trusted_senders = set(data.get("trusted_senders", []))
    return {each.lower() for each in trusted_senders}

def get_email_sender(service, message_id):
    message = service.users().messages().get(
        userId="me",
        id=message_id,
        format="metadata",
        metadataHeaders=["From"]
    ).execute()

    headers = message.get("payload", {}).get("headers", [])
    for header in headers:
        if header["name"].lower() == "from":
            return header["value"].lower()

    return ""

def is_trusted_sender(sender, trusted_senders):
    if not sender:
        return False

    for trusted in trusted_senders:
        if trusted.startswith("@") and sender.endswith(trusted):
            return True

        if trusted in sender:
            return True
        
    return False