from gmail_source import (
    gmail_authenticate, 
    get_gmail_service, 
    search_invoice_emails,
    load_trusted_senders,
    get_email_sender,
    is_trusted_sender
)

from tracker import (
    load_processed_email_ids, 
    save_processed_email_id, 
    load_processed_files_ids, 
    save_processed_files_id
)

from gdrive_source import (
    get_drive_service, 
    list_gdrive_files_in_folder, 
    gdrive_authenticate
)

from aws_s3_source import authenticate_s3, list_s3_objects
from config import load_config, ConfigError
from invoice_downloader import (
    download_gmail_attachments, 
    download_gdrive_files, 
    download_s3_files
)

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
    trusted_senders = load_trusted_senders(config["gmail_trust_senders_path"])
    messages = search_invoice_emails(gmail_service)

    print(f"Found {len(messages)} messages.")
    for msg in messages:
        message_id = msg["id"]

        if message_id in processed_email_ids:
            continue

        sender = get_email_sender(gmail_service, message_id).lower()

        if not is_trusted_sender(sender, trusted_senders):
            print(f"Skipping untrusted sender: {sender}")
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
    
    # AWS S3 Process
    s3_client = authenticate_s3(config["aws_access_key_id"], 
        config["aws_secret_access_key"], 
        config["aws_s3_region_name"])
    
    if s3_client:
        print("AWS S3 Client authenticated.")

    s3_objects = list_s3_objects(s3_client, config["aws_s3_bucket_name"])
    print(f"Found {len(s3_objects)} objects in S3 bucket.")

    processed_s3_keys = load_processed_files_ids(config["aws_s3_tracker_path"])

    new_s3_objects = [obj for obj in s3_objects if obj["Key"] not in processed_s3_keys]
    
    download_s3_files(
        s3_client,
        config["aws_s3_bucket_name"],
        new_s3_objects,
        config["aws_s3_invoice_dir"]
    )

    for each in new_s3_objects:
        save_processed_files_id(config["aws_s3_tracker_path"], each["Key"])

    if new_s3_objects:
        print("Download of Invoices in AWS S3 Complete!")

if __name__ == "__main__":
    main()