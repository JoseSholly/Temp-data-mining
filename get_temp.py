import requests
import json
import time
import concurrent.futures
import os
from dotenv import load_dotenv
import subprocess
load_dotenv() 

# Replace YOUR_API_KEY with the actual API key you got from OpenWeatherMap
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# f = open('nigerian-states.json')
# nigerian_states = json.load(f)

t1 = time.perf_counter()

current_temp_data = {}

def get_temp(city_name):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    current_temp_data[data['name']] = [data['main']['temp']]
    print(f"Location: {data['name']} \t\tCurrent Temperature: {data['main']['temp']}")

def is_daily_data(result):
    for state in states:
        if len(result[state])<=6:
            return True
        return False

def save_data(data, filename):
    if os.path.exists(filename):
        new_data= {}
        with open(filename, 'r+') as file:
            try:
                file_data = json.load(file)
                if is_daily_data(file_data) is True:
                    for key, value in file_data.items():
                        if key in current_temp_data:
                            # print(key, file_data[key],current_temp_data[key])
                            file_data[key]+=current_temp_data[key]
                            new_data.update(file_data)
                        else:
                            file_data[key] = value
                    with open(filename, "w+") as f:
                        json.dump(new_data, f, )
                            
                    # print(f"Updated record: {file_data}")
                else:
                    print("Processing for yesterday's record")
                    subprocess.run(["python", "save_temp_record.py"])
                    with open(filename, "w+") as f:
                        json.dump(current_temp_data, f, )
            except Exception as e:

                json.dump(current_temp_data, file)
             
    else:
        with open(filename, 'w') as file:
            json.dump(current_temp_data, file)

if __name__ == '__main__':
    states = [
        "Akure", "Abuja", "Kano", "Lagos", "Port Harcourt",
        "Ibadan", "Benin City", "Calabar", "Abeokuta"
    ]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(get_temp, states)

    # Save the data to a JSON file
    save_data(current_temp_data, 'temperature_data.json')

    t2 = time.perf_counter()
    print(f'Finished in {t2-t1} seconds')