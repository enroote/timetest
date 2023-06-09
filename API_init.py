from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import logging
from datetime import datetime, date, timedelta

# Google Sheets API credentials
SCOPE = ['https://www.googleapis.com/auth/spreadsheets.readonly']
CREDS_FILE = '/home/pi/foehr/client_secret.json'  # Update with your credentials file path
SPREADSHEET_ID = '1wlNa6wFahS_dpV6Qav5nk4iLkFCXIWOEgsqbFsSUtnY'  # Update with the ID of the "next_4_tides" spreadsheet
SHEET_NAME = 'display HW NW'  # Update with the name of the sheet containing the desired data
RANGE = f"{SHEET_NAME}!A2:G5"  # Specify the sheet name and range of cells

# Google Sheets API setup
credentials = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPE)
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

logging.basicConfig(level=logging.DEBUG)


def fetch_data_from_Google():
    logging.info("Fetching data from Google Sheets...")
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE).execute()
    values = result.get('values', [])

    tide1 = get_tide_label(values[0][0])
    tide2 = get_tide_label(values[1][0])

    time1 = datetime.strptime(values[0][2], "%d.%m.%Y %H:%M:%S").strftime("%H:%M")
    time2 = datetime.strptime(values[1][2], "%d.%m.%Y %H:%M:%S").strftime("%H:%M")

    return tide1, tide2, time1, time2



def get_tide_label(cell_value):
    if cell_value == "H":
        return "Flut"
    elif cell_value == "N":
        return "Ebbe"
    else:
        return ""
    
# Call the function
# data = fetch_data_from_Google()

# if data:
#     tide1, tide2, time1, time2 = data
    
#     # Print the fetched data
#     print("Tide 1:", tide1)
#     print("Tide 2:", tide2)
#     print("Time 1:", time1)
#     print("Time 2:", time2)

#     # Prompt for user input to confirm proceeding
#     answer = input("Do you want to proceed? (y/n): ")
#     if answer.lower() == "y":
#         # Proceed with further steps
#         print("Proceeding with the next steps...")
#     else:
#         print("Process aborted.")

# else:
#     print("Failed to fetch data from Google Sheets.")