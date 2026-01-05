import os
from pathlib import Path
from dotenv import load_dotenv

class ConfigError(Exception):
    """Raised when configuration is invalid."""
    pass

def load_config():
    load_dotenv()

    gmail_scopes = os.getenv("GMAIL_SCOPES")
    gmail_invoice_folder = os.getenv("GMAIL_INVOICE_FOLDER")
    drive_folder_id = os.getenv("DRIVE_INVOICE_FOLDER_ID")
    drive_scopes = [os.getenv("DRIVE_SCOPES")]

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

    invoice_path = Path(gmail_invoice_folder)
    invoice_path.mkdir(parents=True, exist_ok=True)

    tracker_path = Path("metadata/processed_emails.json")
    tracker_path.parent.mkdir(exist_ok=True)

    if not tracker_path.exists():
        tracker_path.write_text(
            '{ "processed_message_ids": [] }',
            encoding="utf-8"
        )

    credentials_file = Path("credentials.json")
    if not credentials_file.exists():
        raise ConfigError(
            "credentials.json not found in project root. "
            "Download it from Google Cloud Console."
        )

    return {
        "gmail_scopes": [gmail_scopes],
        "drive_scopes": [drive_scopes],
        "drive_folder_id": drive_folder_id,
        "invoice_dir": invoice_path,
        "tracker_path": tracker_path,
        "credentials_file": credentials_file,
    }