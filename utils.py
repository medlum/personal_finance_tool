import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
import io
import streamlit as st
import json

# manually created json and hide the info in st.secrets
service_account_info = {
    "type": f"{st.secrets['type']}",
    "project_id": f"{st.secrets['project_id']}",
    "private_key_id": f"{st.secrets['private_key_id']}",
    "private_key": f"{st.secrets['private_key']}",
    "client_email": f"{st.secrets['client_email']}",
    "client_id": f"{st.secrets['client_id']}",
    "auth_uri": f"{st.secrets['auth_uri']}",
    "token_uri": f"{st.secrets['token_uri']}",
    "auth_provider_x509_cert_url": f"{st.secrets['auth_provider_x509_cert_url']}",
    "client_x509_cert_url": f"{st.secrets['client_x509_cert_url']}",
    "universe_domain": f"{st.secrets['universe_domain']}"

}

# ------ SETUP GOOGLE DRIVE ACCESS ------#
# define the Google Drive API scopes and service account file path
SCOPES = ['https://www.googleapis.com/auth/drive']

# if using json file --->
# # SERVICE_ACCOUNT_FILE = "woofwoofgpt.json"
# credentials = service_account.Credentials.from_service_account_file(
#    SERVICE_ACCOUNT_FILE, scopes=SCOPES)


# else i used service_account_info
credentials = service_account.Credentials.from_service_account_info(
    service_account_info, scopes=SCOPES)

# Build the Google Drive service
drive_service = build('drive', 'v3', credentials=credentials)


def uploadFile(filepath, mimetype, file_id):
    """
    - filepath: data file in local 
    - mimetype: file type
    - file_id: existing file id
    """
    media = MediaFileUpload(filepath,
                            mimetype=mimetype)

    file = drive_service.files().update(fileId=file_id,
                                        media_body=media).execute()

    print('File ID: %s' % file.get('id'))


@st.cache_resource(show_spinner=False)
def download_file(file_id, destination_path):
    """Download a file from Google Drive by its ID."""
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination_path, mode='wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

# ------ CHECK FOR DIGITS ENTRY ------#


def is_number(amount):
    # check for digits
    try:
        return float(amount)
    except ValueError:
        return ValueError


# ------ STREAMLIT FORM OPTIONS  ------#
data_dict = {
    "location": ["select one", "singapore", "chiang mai"],

    "spouse": ["select one", "wifey", "hubby"],

    "expense": ["select one",
                "parent allowance",
                "kids allowance",
                "mortgage",
                "insurance",
                "medishield (hospitalisation)",
                "groceries",
                "utilities",
                "phone or data plan",
                "subscription",
                "others"
                ],

    "income": ["select one",
               "rental",
               "dividend",
               "annuity plan",
               "salary",
               "fixed deposit",
               "bond",
               "cpf",
               "others"],

    "details": ["income",
                "insurance",
                "subscription"],

}
# to give permission in a folder use this email from google developer console
# personal-finance@woofwoofgpt.iam.gserviceaccount.com
