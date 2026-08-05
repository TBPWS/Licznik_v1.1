import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def main():
    creds_dict = json.loads(os.environ["GOOGLE_CREDENTIALS"])
    creds = service_account.Credentials.from_service_account_info(creds_dict)

    sheet_id = os.environ["SHEET_ID"]

    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()

    result = sheet.values().get(
        spreadsheetId=sheet_id,
        range="A:Z"
    ).execute()

    values = result.get("values", [])

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(values, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
