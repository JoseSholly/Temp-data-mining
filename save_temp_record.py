import json
import time
from google.oauth2.service_account import Credentials
import gspread
import datetime
import concurrent.futures
import os


t1 = time.perf_counter()

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
print(f"{datetime.date.today()} Temperature Report:")
def access_spreadsheet(cred, url):
    credentials = Credentials.from_service_account_file(cred, scopes=SCOPES)
    client = gspread.authorize(credentials)
    workbook = client.open_by_url(url)
    workbook_sheet = workbook.worksheet("Sheet1")
    return workbook_sheet

def calc_daily_avg(state, data):
    daily_avg = round(sum(data[state]) / len(data[state]), 2)
    return state, daily_avg

def update_google_sheet(state, avg_temp, workbook_sheet):
    cell = workbook_sheet.find(state)
    location_col_values = workbook_sheet.col_values(cell.col)
    workbook_sheet.update_cell(len(location_col_values) + 1, cell.col, avg_temp)
    workbook_sheet.update_cell(len(location_col_values) + 1, 1, f"{datetime.date.today()}")

def save_daily_record(states):
    cred = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") 
    url = "https://docs.google.com/spreadsheets/d/1PcTnb59FcwhrKYhC9E92BjQvqezQo5KQqbi4oiUKEGc/edit#gid=0"
    temp_data_path = "temperature_data.json"
    
    workbook_sheet = access_spreadsheet(cred, url)
    
    with open(temp_data_path, "r+") as file:
        data = json.load(file)
    
    avg_temps = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(calc_daily_avg, state, data) for state in states]
        for future in concurrent.futures.as_completed(futures):
            state, avg_temp = future.result()
            print(f"State: {state} \t\t Average Temperature: {avg_temp} °C")
            avg_temps[state] = avg_temp
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(update_google_sheet, state, avg_temps[state], workbook_sheet) for state in states]
        for future in concurrent.futures.as_completed(futures):
            future.result()

if __name__ == '__main__':
    states = [
        "Akure", "Abuja", "Kano", "Lagos", "Port Harcourt",
        "Ibadan", "Benin City", "Calabar", "Abeokuta"
    ]
    save_daily_record(states)
    t2 = time.perf_counter()
    print(f'Finished in {t2-t1} seconds')
