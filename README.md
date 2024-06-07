# Temperature Date Mining in diffrent Nigeria Cities

# Scheduled Temperature Data Collection

This project collects temperature data from various Nigerian states at scheduled intervals using the OpenWeatherMap API. The data is collected every 3 hours and stored for further analysis.

## Project Structure

- `get_temp.py`: Main script to fetch temperature data.
- `.env`: Environment variables file containing API keys and other secrets.
- `requirements.txt`: Python dependencies.
- `start.sh`: Shell script to run the Python script.
- `README.md`: Project documentation.

## Prerequisites

- Python 3.x
- Git
- PythonAnywhere account

## Setup

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### 2. Install Dependencies
Create a virtual environment and install the required dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3.Set Up Environment Variables
Create a .env file in the root directory of your project and add the necessary environment variables:

```env
OPENWEATHER_API_KEY=your_openweathermap_api_key
GOOGLE_APPLICATION_CREDENTIALS=path_to_your_google_service_account.json
```


## Running Locally
To test the setup locally, you can run the following command:


```bash
source .env
python get_temp.py
```
