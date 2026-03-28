import requests
import pandas as pd

class ExchangeRates:
    def __init__(self, table: str = "a", format: str = "json"):
        self.api_url = f"https://api.nbp.pl/api/exchangerates/tables/{table}/?format={format}"
        self.format=format

    def get_data(self):
        try:
            response = requests.get(self.api_url)
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Wystąpił błąd podczas pobierania danych: {e}")
            return None
        
    def convert_to_data_frame(self, data):

        if self.format == "xml":
            raise NotImplementedError("XML not implemented")
        
        elif self.format == "json":
            if not data:
                raise ValueError("Data not provided")
        
            table_data = data[0]

            rates = table_data["rates"]

            df = pd.DataFrame(rates)

            df["effectiveDate"] = table_data["effectiveDate"]
            df["table"] = table_data["table"]

            return df

        else:
            raise ValueError("wrong data format")
        