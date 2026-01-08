import os
from pathlib import Path
from dotenv import load_dotenv

class ConfigError(Exception):
    """Raised when configuration is invalid."""
    pass

def load_config():
    load_dotenv()

    # Gmail
    gmail_scopes = os.getenv("GMAIL_SCOPES")
    gmail_token_path = os.getenv("GMAIL_TOKEN_PATH")
    gmail_credentials_path = os.getenv("GMAIL_CREDENTIALS")
    gmail_invoice_folder = os.getenv("GMAIL_INVOICE_FOLDER")
    # Drive
    drive_folder_id = os.getenv("DRIVE_INVOICE_FOLDER_ID")
    drive_scopes = os.getenv("DRIVE_SCOPES")
    drive_token_path = os.getenv("DRIVE_TOKEN_PATH")
    drive_credentials_path = os.getenv("DRIVE_CREDENTIALS")
    drive_invoice_folder = os.getenv("GDRIVE_INVOICE_FOLDER")

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
    

    gmail_invoice_path = Path(gmail_invoice_folder)
    gmail_invoice_path.mkdir(parents=True, exist_ok=True)

    gdrive_invoice_path = Path(drive_invoice_folder)
    gdrive_invoice_path.mkdir(parents=True, exist_ok=True)

    gmail_tracker_path = Path("metadata/processed_emails.json")
    gmail_tracker_path.parent.mkdir(exist_ok=True)

    gdrive_tracker_path = Path("metadata/gdrive_processed_files.json")
    gdrive_tracker_path.parent.mkdir(exist_ok=True)


    if not gmail_tracker_path.exists():
        gmail_tracker_path.write_text(
            '{ "processed_message_ids": [] }',
            encoding="utf-8"
        )
    
    if not gdrive_tracker_path.exists():
        gdrive_tracker_path.write_text(
            '{ "processed_files_ids": [] }',
            encoding="utf-8"
        )

    gmail_credentials_file = Path(gmail_credentials_path)
    if not gmail_credentials_file.exists():
        raise ConfigError(
            f"{gmail_credentials_path} not found in project root. "
            "Download it from Google Cloud Console."
        )
    
    gdrive_credentials_file = Path(drive_credentials_path)
    if not gdrive_credentials_file.exists():
        raise ConfigError(
            f"{drive_credentials_path} not found in project root. "
            "Download it from Google Cloud Console."
        )

    return {
        "gmail_scopes": [gmail_scopes],
        "gmail_token_path": gmail_token_path,
        "gmail_credentials_file": gmail_credentials_file,
        "gmail_invoice_dir": gmail_invoice_path,
        "gmail_tracker_path": gmail_tracker_path,
        "gdrive_folder_id": drive_folder_id,
        "gdrive_scopes": [drive_scopes],
        "gdrive_invoice_dir": gdrive_invoice_path,
        "gdrive_token_path": drive_token_path,
        "gdrive_credentials_file": gdrive_credentials_file,
        "gdrive_tracker_path": gdrive_tracker_path
    }