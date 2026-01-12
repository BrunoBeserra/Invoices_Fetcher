import os
from pathlib import Path
from dotenv import load_dotenv

class ConfigError(Exception):
    """Raised when configuration is invalid."""
    pass

def load_config():
    load_dotenv()

    # Gmail Configuration
    gmail_scopes = os.getenv("GMAIL_SCOPES")
    gmail_token_path = os.getenv("GMAIL_TOKEN_PATH")
    gmail_credentials_path = os.getenv("GMAIL_CREDENTIALS")
    gmail_invoice_folder = os.getenv("GMAIL_INVOICE_FOLDER")
    metadata_processed_emails = os.getenv("METADATA_PROCESSED_EMAILS")
    trust_senders_file = os.getenv("GMAIL_TRUST_SENDERS")


    if not gmail_scopes:
        raise ConfigError(
            "Missing GMAIL_SCOPES in .env file. "
            "Example: https://www.googleapis.com/auth/gmail.readonly"
        )

    if not gmail_invoice_folder:
        raise ConfigError(
            "Missing GMAIL_INVOICE_FOLDER in .env file."
            "Example: invoices/gmail"
        )
    
    if not gmail_token_path:
        raise ConfigError(
            "Missing GMAIL_TOKEN in .env file. "
            "Example: token_gmail.json"
        )

    gmail_invoice_path = Path(gmail_invoice_folder)
    gmail_invoice_path.mkdir(parents=True, exist_ok=True)

    gmail_tracker_path = Path(metadata_processed_emails)
    gmail_tracker_path.parent.mkdir(exist_ok=True)

    if not gmail_tracker_path.exists():
        gmail_tracker_path.write_text(
            '{ "processed_message_ids": [] }',
            encoding="utf-8"
        )

    gmail_credentials_file = Path(gmail_credentials_path)
    if not gmail_credentials_file.exists():
        raise ConfigError(
            f"{gmail_credentials_path} not found in project root. "
            "Download it from Google Cloud Console."
        )
    
    # Gmail - Trust Senders Configuration
    trust_senders_path = Path(trust_senders_file)
    trust_senders_path.parent.mkdir(exist_ok=True)

    if not trust_senders_path.exists():
        trust_senders_path.write_text(
            '{ "trusted_senders": [] }',
            encoding="utf-8"
        )
    
    # Drive Configuration
    drive_folder_id = os.getenv("DRIVE_INVOICE_FOLDER_ID")
    drive_scopes = os.getenv("DRIVE_SCOPES")
    drive_token_path = os.getenv("DRIVE_TOKEN_PATH")
    drive_credentials_path = os.getenv("DRIVE_CREDENTIALS")
    drive_invoice_folder = os.getenv("GDRIVE_INVOICE_FOLDER")
    drive_metadata_processed_files = os.getenv("METADATA_PROCESSED_GDRIVE_FILES")

    if not drive_folder_id:
        raise ConfigError(
            "Missing DRIVE_INVOICE_FOLDER_ID in .env file."
            "Example: https://drive.google.com/drive/folders/ -> (1AbCdEfGhIjKlMn)"
        )

    if not drive_scopes:
        raise ConfigError(
            "Missing DRIVE_SCOPES in .env file."
            "Example: https://www.googleapis.com/auth/drive.readonly"
        )
    
    if not drive_token_path:
        raise ConfigError(
            "Missing GDRIVE_TOKEN in .env file. "
            "Example: token_gdrive.json"
        )
    
    if not drive_invoice_folder:
        raise ConfigError(
            "Missing GDRIVE_INVOICE_FOLDER in .env file."
            "Example: invoices/gdrive"
        )
    
    gdrive_invoice_path = Path(drive_invoice_folder)
    gdrive_invoice_path.mkdir(parents=True, exist_ok=True)

    gdrive_tracker_path = Path(drive_metadata_processed_files)
    gdrive_tracker_path.parent.mkdir(exist_ok=True)
    
    if not gdrive_tracker_path.exists():
        gdrive_tracker_path.write_text(
            '{ "processed_files_ids": [] }',
            encoding="utf-8"
        )

    gdrive_credentials_file = Path(drive_credentials_path)
    if not gdrive_credentials_file.exists():
        raise ConfigError(
            f"{drive_credentials_path} not found in project root. "
            "Download it from Google Cloud Console."
        )
    
    # AWS S3 Configuration
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_s3_bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
    aws_s3_region_name = os.getenv("AWS_S3_REGION_NAME")
    metadata_processed_s3_files = os.getenv("METADATA_PROCESSED_S3_FILES")
    aws_s3_invoice_folder = os.getenv("AWS_S3_INVOICE_FOLDER")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ConfigError(
            "Missing AWS S3 configuration in .env file. "
            "Please provide AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY of your IAM access key from your AWS Account."
        )

    if not aws_s3_bucket_name:
        raise ConfigError(
            "Missing AWS_S3_BUCKET_NAME in .env file. "
            "Example: test.automation.ccl.interview"
        )
    
    if not aws_s3_region_name:
        raise ConfigError(
            "Missing AWS_S3_REGION_NAME in .env file. "
            "Example: us-east-1"
        )
    
    if not aws_s3_invoice_folder:
        raise ConfigError(
            "Missing AWS_S3_INVOICE_FOLDER in .env file."
            "Example: invoices/aws_s3"
        )
    
    aws_s3_tracker_path = Path(metadata_processed_s3_files)
    aws_s3_tracker_path.parent.mkdir(exist_ok=True)
    
    if not aws_s3_tracker_path.exists():
        aws_s3_tracker_path.write_text(
            '{ "processed_files_ids": [] }',
            encoding="utf-8"
        )
    
    return {
        "gmail_scopes": [gmail_scopes],
        "gmail_token_path": gmail_token_path,
        "gmail_credentials_file": gmail_credentials_file,
        "gmail_invoice_dir": gmail_invoice_path,
        "gmail_tracker_path": gmail_tracker_path,
        "gmail_trust_senders_path": trust_senders_path,
        "gdrive_folder_id": drive_folder_id,
        "gdrive_scopes": [drive_scopes],
        "gdrive_invoice_dir": gdrive_invoice_path,
        "gdrive_token_path": drive_token_path,
        "gdrive_credentials_file": gdrive_credentials_file,
        "gdrive_tracker_path": gdrive_tracker_path,
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key,
        "aws_s3_bucket_name": aws_s3_bucket_name,
        "aws_s3_region_name": aws_s3_region_name,
        "aws_s3_tracker_path": aws_s3_tracker_path,
        "aws_s3_invoice_dir": aws_s3_invoice_folder
    }