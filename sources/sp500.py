import requests
import pandas as pd
import os
from datetime import datetime


class SP500:
    def __init__(self, access_key):
        self.access_key = access_key or os.getenv("MARKETSTACK_API_KEY")

        if not self.access_key:
            raise ValueError("Brak access key")
        
        self.api_url = f"http://api.marketstack.com/v1/eod?access_key={access_key}&symbols=SPY"
        self.file_name = "spy_data.csv"

    def get_data(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Błąd pobierania danych: {e}")
            return None

    def convert_to_data_frame(self, data):
        return pd.DataFrame(data["data"])

    def get_last_loaded_date(self):
        if not os.path.exists(self.file_name):
            return None

        df = pd.read_csv(self.file_name)

        if df.empty:
            return None

        return df["date"].max()

    def incremental_load(self):
        data = self.get_data()

        if not data:
            return

        new_df = self.convert_to_data_frame(data)

        new_df["date"] = pd.to_datetime(new_df["date"])

        last_date = self.get_last_loaded_date()

        if last_date:
            last_date = pd.to_datetime(last_date)

            new_df = new_df[new_df["date"] > last_date]

        if new_df.empty:
            print("Brak nowych danych.")
            return

        if os.path.exists(self.file_name):
            old_df = pd.read_csv(self.file_name)
            final_df = pd.concat([old_df, new_df], ignore_index=True)
        else:
            final_df = new_df

        final_df.to_csv(self.file_name, index=False)

        print(f"Loaded {len(new_df)} new records.")



api = SP500()
api.incremental_load()

# incremantal loading w databricks