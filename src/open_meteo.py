# Import libraries
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry

class Temperature:
    def __init__(self, retries=5):
        """
        Setup the Open-Meteo API client with cache and retry on error
        """
        self.cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        self.retry_session = retry(self.cache_session, retries=retries, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=self.retry_session)
        self.url = "https://api.open-meteo.com/v1/forecast"
        self.last_response = None
        self.last_data = None
        self.last_temperature_2m = 0.0
        self.last_rain = False

    def fetch_data(self, latitude=-31.4135, longitude=-64.181):
        """
        Make sure all required weather variables are listed here
        The order of variables in hourly or daily is important to assign them correctly below
        """
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ["temperature_2m", "rain"],
            "timezone": "auto",
            "forecast_days": 1
        }
        try:
            # Let's limit the API response to just one location
            self.last_response = self.openmeteo.weather_api(self.url, params=params)[0]

            # Current values. The order of variables needs to be the same as requested.
            self.last_data = self.last_response.Current()
            self.last_temperature_2m = self.last_data.Variables(0).Value()
            self.last_rain = bool( self.last_data.Variables(1).Value() )
            
            return self.last_temperature_2m, self.last_rain
        except:
            return 0, 0

    def __str__(self):
        text  = f"Coordinates {self.last_response.Latitude()}°N {self.last_response.Longitude()}°E\n"
        text += f"Elevation {self.last_response.Elevation()} m asl\n"
        text += f"Timezone {self.last_response.Timezone()} {self.last_response.TimezoneAbbreviation()}\n"
        text += f"Timezone difference to GMT+0 {self.last_response.UtcOffsetSeconds()} s\n"
        text += f"Current time {self.last_data.Time()}\n"
        text += f"Current temperature_2m {self.last_temperature_2m}\n"
        text += f"Current rain {self.last_rain}\n"
        return text

if __name__ == '__main__':
    obj = Temperature()
    obj.fetch_data()
    print(obj)