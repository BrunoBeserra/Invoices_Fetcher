import os
from gmail_source import (
    gmail_authenticate, 
    get_gmail_service, 
    search_invoice_emails
)

from tracker import (
    load_processed_email_ids, 
    save_processed_email_id, 
    load_processed_files_ids, 
    save_processed_files_id
)

from gdrive_source import get_drive_service, list_gdrive_files_in_folder, gdrive_authenticate
from config import load_config, ConfigError
from invoice_downloader import download_gmail_attachments, download_gdrive_files



def main():
    try:
        config = load_config()
        print("Configuration Successful!")
    except ConfigError as e:
        print(f"Configuration error: {e}")
        return
    
    # Gmail Process 
    gmail_creds = gmail_authenticate(config["gmail_scopes"], config["gmail_token_path"], config["gmail_credentials_file"])

    if gmail_creds and gmail_creds.valid:
        print("Gmail authentication successful.")
    else:
        print("Gmail authentication failed.")
    
    gmail_service = get_gmail_service(gmail_creds)

    processed_email_ids = load_processed_email_ids(config["gmail_tracker_path"])
    messages = search_invoice_emails(gmail_service)

    print(f"Found {len(messages)} messages.")
    for msg in messages:
        message_id = msg["id"]

        if message_id in processed_email_ids:
            continue

        download_gmail_attachments(gmail_service, msg["id"], config["gmail_invoice_dir"])
        save_processed_email_id(config["gmail_tracker_path"], message_id)

    print("Download of Invoices Complete!")

    # Gdrive Process 
    gdrive_creds = gdrive_authenticate(config["gdrive_scopes"], config["gdrive_token_path"], config["gdrive_credentials_file"])

    if gdrive_creds and gdrive_creds.valid:
        print("Gdrive authentication successful.")
    else:
        print("Gdrive authentication failed.")
    
    drive_service = get_drive_service(gdrive_creds)
    gdrive_files = list_gdrive_files_in_folder(drive_service, config["gdrive_folder_id"])
    processed_gdrive_file_ids = load_processed_files_ids(config["gdrive_tracker_path"])

    new_gdrive_files = [f for f in gdrive_files if f["id"] not in processed_gdrive_file_ids]

    download_gdrive_files(drive_service, new_gdrive_files, config["gdrive_invoice_dir"])

    for each in new_gdrive_files:
        save_processed_files_id(config["gdrive_tracker_path"], each["id"])
    
    if new_gdrive_files:
        print("Download of Invoices in Drive Complete!")


if __name__ == "__main__":
    main()