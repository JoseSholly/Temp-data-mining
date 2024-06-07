import requests
import json
import time
import concurrent.futures
import os
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
import subprocess
from google.oauth2.service_account import Credentials
import gspread
import datetime
import os

load_dotenv() 

# Replace YOUR_API_KEY with the actual API key you got from OpenWeatherMap
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# f = open('nigerian-states.json')
# nigerian_states = json.load(f)

t1 = time.perf_counter()

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
current_temp_data = {}

print(f"{datetime.date.today()} Temperature Report:")



def get_temp(city_name):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    current_temp_data[data['name']] = data['main']['temp']
    print(f"Location: {data['name']} \t\tCurrent Temperature: {data['main']['temp']}°C")
    return current_temp_data

def access_spreadsheet(cred, url):
    credentials = Credentials.from_service_account_file(cred, scopes=SCOPES)
    client = gspread.authorize(credentials)
    workbook = client.open_by_url(url)
    workbook_sheet = workbook.worksheet("Sheet1")
    return workbook_sheet

def update_google_sheet(state, avg_temp, workbook_sheet):
    cell = workbook_sheet.find(state)
    location_col_values = workbook_sheet.col_values(cell.col)
    workbook_sheet.update_cell(len(location_col_values) + 1, cell.col, avg_temp)
    workbook_sheet.update_cell(len(location_col_values) + 1, 1, f"{datetime.date.today()}")

def save_daily_record():
    cred = os.getenv("GOOGLE_APPLICATION_CREDENTIALS") 
    # url = "https://docs.google.com/spreadsheets/d/1PcTnb59FcwhrKYhC9E92BjQvqezQo5KQqbi4oiUKEGc/edit#gid=0"

    url="https://docs.google.com/spreadsheets/d/1M2ZVt2DO_ZOfjWuBATF2F6NAqWhpidlmrOLXlao8MYM/edit#gid=0"
    
    workbook_sheet = access_spreadsheet(cred, url)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(update_google_sheet, state, current_temp_data[state], workbook_sheet) for state in states]
        for future in concurrent.futures.as_completed(futures):
            future.result()
    print("Data Successfully uploaded ! ! !")


if __name__ == '__main__':
    states = [
        "Akure", "Abuja", "Kano", "Lagos", "Port Harcourt",
        "Ibadan", "Benin City", "Calabar", "Abeokuta"
    ]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(get_temp, states)

    save_daily_record()

    t2 = time.perf_counter()
    print(f'Finished in {t2-t1} seconds')