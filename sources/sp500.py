import requests
import pandas as pd

class SP500:
    def __init__(self, data):
        self.api_url = f"http://api.marketstack.com/v1/eod?access_key=3b53b71a2e0497f0db02037530459f68&symbols=SPY"

    def get_data(self):
        try:
            response = requests.get(self.api_url)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Wystąpił błąd podczas pobierania danych: {e}")
            return None
        
    def convert_to_data_frame(self, data):

        return pd.DataFrame(data['data'])

