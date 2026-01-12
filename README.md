# Invoice Fetcher

**Automated Gmail, Google Drive, and AWS S3 invoice downloader in Python**

This project automates fetching invoices from multiple sources and saving them locally in a structured folder. It demonstrates skills in **Python automation, API integration, data ingestion, and secure metadata handling**.

---

## Features

- **Gmail Integration**
  - Searches for emails with attachments containing keywords: `invoice`, `receipt`, `bill`
  - Downloads attachments only from **trusted senders**
  - Tracks processed emails to avoid duplicates

- **Google Drive Integration**
  - Fetches files from folders based on their IDs, 
  - Downloads files to local machine
  - Tracks downloaded files to prevent duplicates

- **AWS S3 Integration**
  - Downloads objects from configured S3 buckets
  - Filters out zero-byte files
  - Tracks processed objects

- **Metadata & Configuration**
  - All settings, credentials, and trackers are stored in `metadata/`
  - Trusted Gmail senders configurable via `metadata/trusted_gmail_senders.json`

- **Extensible & Config-driven**
  - Add new sources easily
  - Update trusted senders without changing code
  - Timestamped filenames prevent collisions

---

## Project Structure

Invoices_Fetcher/
│
├── invoices/
│   ├── aws/
│   ├── gdrive/
|   └── gmail/
|
├── metadata/
│   ├── trusted_gmail_senders.json
│   ├── gmail_tracker.json
│   ├── gdrive_tracker.json
|   └── trust_senders.json
│
├── src/
│   ├── main.py
│   ├── config.py
│   ├── gmail_source.py
│   ├── gdrive_source.py
│   ├── aws_s3_source.py
|   ├── invoice_downloader.py
|   └── tracker.py
│
├── .env
├── credentials.json
├── requirements.txt
└── setup.ps1

---

## Setup

### 1. Create Python Environment

```
powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt 
```
Or run setup.ps1 to automatically set up the environment

### 2. Add Credentials

- Gmail: OAuth 2.0 client credentials JSON from Google Cloud Console
- Google Drive: OAuth 2.0 client credentials JSON from Google Cloud Console
- AWS S3: IAM user with S3 access from AWS Management Console

### 3. Configure Trusted Senders in Metadata folder

Create or edit metadata/trusted_gmail_senders.json
Example:
{
  "trusted_senders": [
    "billing@companya.com",
    "@companyb.com"
  ]
}

### 4. Configure .env file

- Open .env_sample and modify the variables that need to be changed.
- After done, rename it to `.env`

### 5. Run the Project

python src/main.py

All invoices will be downloaded to folders configured in .env.