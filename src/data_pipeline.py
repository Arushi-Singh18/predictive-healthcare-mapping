import os
import requests
import json
import logging
from datetime import datetime
import pandas as pd

# --- Configuration ---
# You will need to get a free API key from OpenWeatherMap (https://openweathermap.org/api)
# It is best practice to store this in an environment variable, but you can hardcode for initial testing.
API_KEY = os.environ.get("OPENWEATHER_API_KEY", "YOUR_API_KEY_HERE")
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Setting up logging so we can track the execution
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_weather_data(city_name):
    """
    Fetches current weather data for a specified city using the OpenWeatherMap API.
    
    Args:
        city_name (str): The name of the city (e.g., 'Lucknow,IN')
        
    Returns:
        dict: A dictionary containing the parsed JSON data, or None if the request failed.
    """
    logging.info(f"Fetching weather data for: {city_name}")
    
    # Construct the API request URL
    # We use metric units for Celsius
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric' 
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        
        data = response.json()
        logging.info("Successfully fetched data.")
        return data
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data from API: {e}")
        return None

def process_weather_data(raw_data):
    """
    Extracts relevant features from the raw OpenWeatherMap JSON response for our predictive model.
    Specifically pulls temperature, humidity, and air quality proxies.
    """
    if not raw_data:
        return None
        
    logging.info("Processing raw weather data...")
    
    try:
        # Extracting specific data points relevant to Public Health modeling
        processed_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'city': raw_data['name'],
            'temperature_celsius': raw_data['main']['temp'],
            'humidity_percent': raw_data['main']['humidity'],
            'pressure_hpa': raw_data['main']['pressure'],
            'weather_condition': raw_data['weather'][0]['main'], # e.g., Rain, Clear, Haze
            'wind_speed_m_s': raw_data['wind']['speed']
        }
        return processed_data
    except KeyError as e:
        logging.error(f"Error parsing data structure (missing key): {e}")
        return None

if __name__ == "__main__":
    print("-" * 50)
    print("Predictive Healthcare Mapping: Data Pipeline Initialized")
    print("-" * 50)
    
    # In a real scenario, this would loop through a list of clinic locations
    target_city = "Lucknow,IN"
    
    # 1. Extract
    raw_weather = fetch_weather_data(target_city)
    
    # 2. Transform
    if raw_weather:
        clean_weather = process_weather_data(raw_weather)
        
        # Display the output
        print("\nProcessed Data Ready for Modeling:")
        print(json.dumps(clean_weather, indent=4))
        
        # 3. Load (Saving to a CSV for our models to use later)
        # We use pandas to easily append this to a dataset
        df = pd.DataFrame([clean_weather])
        
        output_file = "lucknow_weather_log.csv"
        # If file exists, append without writing headers again. Otherwise, write headers.
        if os.path.exists(output_file):
            df.to_csv(output_file, mode='a', header=False, index=False)
            logging.info(f"Appended data to {output_file}")
        else:
            df.to_csv(output_file, mode='w', header=True, index=False)
            logging.info(f"Created new data file {output_file}")
    else:
        print("Failed to retrieve data. Check your API key and internet connection.")
