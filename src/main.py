import os

from gmail_source import (
    gmail_authenticate, 
    get_gmail_service, 
    search_invoice_emails
)

from invoice_downloader import download_gmail_attachments
from tracker import load_processed_ids, save_processed_id
from config import load_config, ConfigError

def main():

    try:
        config = load_config()
        print("Configuration Successful!")
    except ConfigError as e:
        print(f"Configuration error: {e}")
        return
    
    scopes = config["gmail_scopes"]
    gmail_dir = os.getenv("GMAIL_INVOICE_FOLDER")
    tracker_path = os.getenv("METADATA_PROCESSED_EMAILS")


    creds = gmail_authenticate(scopes)

    if creds and creds.valid:
        print("Gmail authentication successful.")
    else:
        print("Gmail authentication failed.")
    
    service = get_gmail_service(creds)

    processed_ids = load_processed_ids(tracker_path)
    messages = search_invoice_emails(service)

    print(f"Found {len(messages)} messages.")
    for msg in messages:
        message_id = msg["id"]

        if message_id in processed_ids:
            print(f"Skipping already processed email: {message_id}")
            continue

        download_gmail_attachments(service, msg["id"], gmail_dir)
        save_processed_id(tracker_path, message_id)

    print("Download of Invoices Complete!")


if __name__ == "__main__":
    main()