import os
import requests
import msal
import base64
from dotenv import load_dotenv
load_dotenv()


CLIENT_ID = os.getenv("CLIENT_ID")
TENANT_ID = os.getenv("TENANT_ID")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")  
DOWNLOAD_DIR = "../mess_menus"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]


def get_access_token():
    app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    result = app.acquire_token_by_username_password(USERNAME, PASSWORD, scopes=SCOPES)
    if "access_token" not in result:
        raise Exception("Failed to acquire token: " + str(result.get("error_description")))
    return result["access_token"]


def fetch_target_emails(token):
    headers = {"Authorization": f"Bearer {token}"}
    subject_filter = os.getenv("EMAIL_SUBJECT")
    url = f"https://graph.microsoft.com/v1.0/me/messages?$filter=startswith(subject,'{subject_filter}')&$top=10"
    res = requests.get(url, headers=headers)
    return res.json().get("value", [])

def download_attachments(msg_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    att_url = f"https://graph.microsoft.com/v1.0/me/messages/{msg_id}/attachments"
    res = requests.get(att_url, headers=headers)
    attachments = res.json().get("value", [])
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    for att in attachments:
        if att["@odata.type"] == "#microsoft.graph.fileAttachment" and att["name"].endswith(".pdf"):
            file_path = os.path.join(DOWNLOAD_DIR, att["name"])
            with open(file_path, "wb") as f:
                f.write(base64.b64decode(att["contentBytes"]))
            print(f"Saved PDF: {file_path}")


def fetch_pdfs():
    token = get_access_token()
    emails = fetch_target_emails(token)
    emails = fetch_target_emails(token)
    if not emails:
        print("No matching emails found.")
        return
    print(f"Found {len(emails)} matching emails.")
    for msg in emails:
        print(f" {msg['subject']}")
        download_attachments(msg["id"], token)
fetch_pdfs()