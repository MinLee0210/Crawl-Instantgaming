# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=maybe-no-member
# pylint: disable=missing-final-newline

import os, logging, time

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

from .utils import set_logger

set_logger()

class GoogleDriveService:
    def __init__(self, credential_dir: str):
        scopes = ['https://www.googleapis.com/auth/drive']
        self.creds = service_account.Credentials.from_service_account_file(
                credential_dir, scopes=scopes)

    def rename(self, orig_name):
        name = '_'.join([orig_name, time.ctime()])
        return name

    def upload_data(self, content_dir, google_drive_id, mimetype, rename=False):
        # mimetype ["image/jpeg", "text/txt"]
        try:
            # create drive api client
            service = build("drive", "v3", credentials=self.creds)
            content_name = content_dir.split(os.sep)[-1]
            if rename:
                content_name = self.rename(content_name)
            file_metadata = {"name": content_name,
                            'parents': [google_drive_id]}
            media = MediaFileUpload(content_dir, mimetype=mimetype, resumable=True)
            file = (
                service.files()
                .create(body=file_metadata, media_body=media, fields="id")
                .execute()
            )
            # print(f'File ID: {file.get("id")}')
            logging.info(msg=f"GoogleDriveServcie upload_data with FileID:{file.get('id')}")
        except HttpError as error:
            print(f"An error occurred: {error}")
            file = None

        return file.get("id")