import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()  # Load environment variables from .env file

class GoogleSheetsCRUD:
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    CREDENTIALS_FILE = os.getenv('CREDENTIALS_FILE')
    SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

    def __init__(self):
        self.creds = self.getUserCredentials()
        self.service = build("sheets", "v4", credentials=self.creds)

    def getUserCredentials(self):
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.CREDENTIALS_FILE, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds

    def createSpreadsheet(self, title, data=None):
        """Create a new sheet and optionally populate it with data."""
        try:
            # Create the new sheet
            spreadsheet = {
                "properties": {"title": title},
                "sheets": [{"properties": {"title": title}}]
            }
            response = self.service.spreadsheets().create(
                body=spreadsheet,
                fields="spreadsheetId"
            ).execute()

            spreadsheet_id = response.get("spreadsheetId")
            print(f"Created new spreadsheet with ID: {spreadsheet_id}")

            # If data is provided, populate the new sheet
            if data:
                self.append_row_to_sheet(spreadsheet_id, title, data)

            return spreadsheet_id
        except HttpError as err:
            print(f"An error occurred: {err}")
            return None

    def createSheet(self, sheet_name):
        """Create a new sheet in an existing spreadsheet."""
        try:
            # Define the request to add a new sheet
            requests = [{
                "addSheet": {
                    "properties": {
                        "title": sheet_name
                    }
                }
            }]

            # Send the request to the API
            response = self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.SPREADSHEET_ID,
                body={"requests": requests}
            ).execute()

            # Extract the sheet ID from the response
            sheet_id = response['replies'][0]['addSheet']['properties']['sheetId']
            
            print(f"Sheet '{sheet_name}' created with ID: {sheet_id}")
            return sheet_id

        except HttpError as err:
            print(f"An error occurred: {err}")
            return None
    
    def createSheetAndInsertData(self, sheet_name, data):
        """Create a new sheet and insert data into it."""
        try:
            self.createSheet( sheet_name )
            self.insertData(sheet_name, data)

        except HttpError as err:
            print(f"An error occurred: {err}")
            
    def insertData(self, sheet_name, data):
        try:
            values = self.readSheet(sheet_name)
            start_row = len(values)+1
            range_name = f"{sheet_name}!A"+str(start_row)
            
            # Insert data into the new sheet
            response = self.service.spreadsheets().values().update(
                spreadsheetId=self.SPREADSHEET_ID,
                range=range_name,
                valueInputOption="RAW",
                body={"values": data}
            ).execute()

            print(f"Data inserted into sheet '{sheet_name}'.")
            print(f"Update response: {response}")

        except HttpError as err:
            print(f"An error occurred: {err}")

    def readSheet(self, sheet_name):
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.SPREADSHEET_ID,
                range=sheet_name
            ).execute()
            values = result.get("values", [])
            return values
        except HttpError as err:
            print(f"An error occurred: {err}")
            return None

    def appendRow(self, row_data, sheet_name):
        try:
            response = self.service.spreadsheets().values().append(
                spreadsheetId=self.SPREADSHEET_ID,
                range=sheet_name,
                valueInputOption="RAW",
                body={"values": [row_data]}
            ).execute()
            return response
        except HttpError as err:
            print(f"An error occurred: {err}")
            return None

    def prependRow(self, new_row, sheet_name):
        try:
            values = self.readSheet(sheet_name)
            updated_values = [new_row] + values
            range_to_update = f"{sheet_name}!A1:Z"
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.SPREADSHEET_ID,
                range=range_to_update,
                valueInputOption="RAW",
                body={"values": updated_values}
            ).execute()
            print("New row prepended successfully.")
            print(f"Update response: {result}")
        except HttpError as err:
            print(f"An error occurred: {err}")

    def updateRow(self, row_index, row_data, sheet_name):
        try:
            range_name = f"{sheet_name}!A{row_index}:Z{row_index}"
            response = self.service.spreadsheets().values().update(
                spreadsheetId=self.SPREADSHEET_ID,
                range=range_name,
                valueInputOption="RAW",
                body={"values": [row_data]}
            ).execute()
            return response
        except HttpError as err:
            print(f"An error occurred: {err}")
            return None

    def deleteRow(self, row_index, sheet_name):
        try:
            values = self.readSheet(sheet_name)
            if not values or row_index > len(values):
                print("Row index out of range.")
                return
            clear_range = f"{sheet_name}!A{row_index}:Z{row_index}"
            result = self.service.spreadsheets().values().clear(
                spreadsheetId=self.SPREADSHEET_ID,
                range=clear_range
            ).execute()
            print(f"Row {row_index} deleted.")
        except HttpError as err:
            print(f"An error occurred: {err}")

    def deleteRowAndShiftUp(self, row_index, sheet_name):
        try:
            values_original = self.readSheet(sheet_name)
            length_data = len(values_original)
            if not values_original or row_index > length_data:
                print("Row index out of range.")
                return
            clear_range = f"{sheet_name}!A{row_index}:Z{row_index}"
            result = self.service.spreadsheets().values().clear(
                spreadsheetId=self.SPREADSHEET_ID,
                range=clear_range
            ).execute()
            values_to_update = values_original[row_index:]
            range_to_update = f"{sheet_name}!A{row_index}:Z"
            self.service.spreadsheets().values().update(
                spreadsheetId=self.SPREADSHEET_ID,
                range=range_to_update,
                valueInputOption="RAW",
                body={"values": values_to_update}
            ).execute()
            clear_range = f"{sheet_name}!A{length_data}:Z{length_data}"
            result = self.service.spreadsheets().values().clear(
                spreadsheetId=self.SPREADSHEET_ID,
                range=clear_range
            ).execute()
            print(f"Row {row_index} deleted and rows shifted up.")
        except HttpError as err:
            print(f"An error occurred: {err}")
