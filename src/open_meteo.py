# Import libraries
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

class Temperature:
    def __init__(self, max_retries=5):
        """
        Setup the Open-Meteo API client with cache and retry on error
        """
        self.cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        self.retry_session = retry(self.cache_session, retries=max_retries, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=self.retry_session)
        self.url = "https://api.open-meteo.com/v1/forecast"
        self.last_response = None
        self.last_data = None
        self.last_temperature_2m = 0.0
        self.last_rain = False
        self.max_retries = max_retries

    def fetch_data(self, latitude=-31.4135, longitude=-64.181):
        """
        Make sure all required weather variables are listed here
        The order of variables in hourly or daily is important to assign them correctly below
        """
        retries = 0
        while retries < self.max_retries:
            print(f'Getting data from Open Meteo... Try {retries + 1}/{self.max_retries}')
            try:
                params = {
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": ["temperature_2m", "rain"],
                    "timezone": "auto",
                    "forecast_days": 1
                }
                # Let's limit the API response to just one location
                self.last_response = self.openmeteo.weather_api(self.url, params=params)[0]

                # Current values. The order of variables needs to be the same as requested.
                self.last_data = self.last_response.Current()
                self.last_temperature_2m = self.last_data.Variables(0).Value()
                self.last_rain = bool(self.last_data.Variables(1).Value())

                return self.last_temperature_2m, self.last_rain
            except Exception as e:
                retries += 1
        return None, None

    def __str__(self):
        text  = f"Data:\n"
        try:
            text += f"\t - Coordinates {self.last_response.Latitude()}°N {self.last_response.Longitude()}°E\n"
            text += f"\t - Elevation {self.last_response.Elevation()} m asl\n"
            text += f"\t - Timezone {self.last_response.Timezone()} {self.last_response.TimezoneAbbreviation()}\n"
            text += f"\t - Timezone difference to GMT+0 {self.last_response.UtcOffsetSeconds()} s\n"
            text += f"\t - Current time {self.last_data.Time()}\n"
        except:
            pass
        text += f"\t - Current temperature_2m {self.last_temperature_2m}\n"
        text += f"\t - Current rain {self.last_rain}\n"
        return text

if __name__ == '__main__':
    obj = Temperature(max_retries = 10)
    rain, temp = obj.fetch_data()
    print(obj)
    print(rain)
    print(temp)