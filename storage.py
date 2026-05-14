import os
import json
from datetime import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def save_to_history(new_data):
    history_file = "aquarium_history.json"

    # Pridedame laiko žymą
    new_data["timestamp"] = datetime.now().isoformat()

    if os.path.exists(history_file):
        with open(history_file, "r+", encoding="utf-8") as f:
            data = json.load(f)
            data.append(new_data)
            f.seek(0)
            json.dump(data, f, indent=2, ensure_ascii=False)
    else:
        with open(history_file, "w", encoding="utf-8") as f:
            json.dump([new_data], f, indent=2, ensure_ascii=False)

    print(f"📂 Duomenys sėkmingai išsaugoti į {history_file}")


def update_google_sheets(ai_report):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open("Aqua Duomenys").sheet1

    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ai_report.get("vandens_skaidrumas", ""),
        ai_report.get("augalų_būklė", ""),
        ai_report.get("gyventojų_patikra", ""),
        ai_report.get("rekomendacija", ""),
    ]

    sheet.append_row(row)
    print("📊 Google Sheets lentelė atnaujinta!")


def save_to_logs(log_data):
    file_path = os.path.join("logs", f"{datetime.now().strftime('%Y-%m-%d')}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(log_data)
