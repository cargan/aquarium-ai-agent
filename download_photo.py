import io
from datetime import datetime

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account


def download_latest_photo_from_drive():
    # Naudojame GitHub Secrets įkeltą JSON raktą
    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
    SERVICE_ACCOUNT_FILE = (
        "service_account.json"  # GitHub Actions sukurs šį failą iš Secrets
    )

    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    service = build("drive", "v3", credentials=creds)
    folder_id = "12jvj3QJ57lzqKwMXXEC4_LcAmWw7Y-GK"

    # Surandame naujausią failą aplanke
    results = (
        service.files()
        .list(
            q=f"'{folder_id}' in parents and mimeType contains 'image/'",
            orderBy="createdTime desc",
            pageSize=1,
            fields="files(id, name)",
        )
        .execute()
    )

    items = results.get("files", [])
    if not items:
        print("Folderis tuščias!")
        return None

    file_id = items[0]["id"]
    file_name = items[0]["name"]
    today_date = datetime.now().strftime("%Y-%m-%d")
    new_filename = f"{today_date}.jpeg"

    # Atsisiunčiame failą į snapshots folderį
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(f"snapshots/{new_filename}", "wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()

    return new_filename
