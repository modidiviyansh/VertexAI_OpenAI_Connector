import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from converter_md_docx import markdown_to_docx

# Define your SCOPES, in this case Google Drive read/write permissions
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def upload_file_and_get_docs_link(file_path):
    """Upload a .docx file, convert to Google Docs, and return the Google Docs link."""
    
    creds = None
    # Load token if it exists
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If credentials are not available or are invalid, get a new token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Build the Google Drive service
    service = build('drive', 'v3', credentials=creds)
    
    # Define metadata for the file and set it to be converted to Google Docs format
    file_metadata = {
        'name': os.path.basename(file_path),
        'mimeType': 'application/vnd.google-apps.document'  # Convert to Google Docs format
    }

    # Upload the .docx file and convert it to Google Docs format
    media = MediaFileUpload(file_path, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # Get file ID and create the Google Docs link
    file_id = file.get('id')
    link = f"https://docs.google.com/document/d/{file_id}/edit"

    return link

# Example usage
def upload_clean_file_to_googledrive(file_path):
    clean_file_path = markdown_to_docx(file_path)
    print(f"Uploading {clean_file_path} to Google Drive...");
    google_doc_link = upload_file_and_get_docs_link(clean_file_path)
    return google_doc_link



