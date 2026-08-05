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

    # Pobierz listę wszystkich skoroszytów
    metadata = sheet.get(spreadsheetId=sheet_id).execute()
    sheets = metadata.get("sheets", [])

    output = {}

    for s in sheets:
        title = s["properties"]["title"]  # nazwa zakładki
        result = sheet.values().get(
            spreadsheetId=sheet_id,
            range=f"{title}!A:ZZ"
        ).execute()

        values = result.get("values", [])
        output[title] = values

    # Zapisz wszystkie zakładki do jednego JSON
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
