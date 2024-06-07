import requests
import time
import concurrent.futures
import os
from dotenv import load_dotenv
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

# print(f"{datetime.date.today()} Temperature Report:")



def get_temp(city_name):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    current_temp_data[data['name']] = [data['main']['temp']]
    # print(f"Location: {data['name']} \t\tCurrent Temperature: {data['main']['temp']}°C")

    return current_temp_data


if __name__ == '__main__':
    states = [
        "Akure", "Abuja", "Kano", "Lagos", "Port Harcourt",
        "Ibadan", "Benin City", "Calabar", "Abeokuta"
    ]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(get_temp, states)
    # print(current_temp_data)

    t2 = time.perf_counter()
    # print(f'Finished in {t2-t1} seconds')