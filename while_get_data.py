import time
import requests
import concurrent.futures
import os
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
import gspread
import datetime
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
load_dotenv() 

# Replace YOUR_API_KEY with the actual API key you got from OpenWeatherMap
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Define the interval in seconds (3 hours = 3 * 60 * 60 seconds)
interval_seconds = 2

# Define the number of runs per day
runs_per_day = 8

# Initialize a dictionary to store all hourly results
all_temp_data = {}

states = [
    "Akure", "Abuja", "Kano", "Lagos", "Port Harcourt",
    "Ibadan", "Benin City", "Calabar", "Abeokuta"
]

def get_temp(city_name):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    return data['main']['temp']

# Run the loop until the desired number of runs are completed
for run_number in range(1, runs_per_day + 1):
    
    # Initialize a dictionary to store hourly results for this run
    hourly_results = {}
    
    # Fetch temperatures for all states concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        temperatures = list(executor.map(get_temp, states))

    # Store hourly results for each state in the hourly_results dictionary
    for state, temperature in zip(states, temperatures):
        if state not in all_temp_data:
            all_temp_data[state] = []
        all_temp_data[state].append(temperature)
    
    print(f"{datetime.datetime.now()}: Run {run_number} completed")
    
    # If all runs are completed, break out of the loop
    if run_number == runs_per_day:
        break
    
    # Wait for the next interval
    time.sleep(interval_seconds)

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
    url = "https://docs.google.com/spreadsheets/d/1PcTnb59FcwhrKYhC9E92BjQvqezQo5KQqbi4oiUKEGc/edit#gid=0"
    
    workbook_sheet = access_spreadsheet(cred, url)

    all_temp_data_avg= {}
    for state in states:
        daily_avg = round(sum(all_temp_data[state]) / len(all_temp_data[state]), 2)
        all_temp_data_avg[state]= daily_avg

    print(f"\nAverage Temperature on {datetime.date.today()}: {all_temp_data_avg}")


    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(update_google_sheet, state, all_temp_data_avg[state], workbook_sheet) for state in states]
        for future in concurrent.futures.as_completed(futures):
            future.result()
    print("\nData Successfully Uploaded ! ! !")


if __name__ == '__main__':
    save_daily_record()
