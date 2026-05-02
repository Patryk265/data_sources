import requests
import pandas as pd


class ExchangeRates:
    def __init__(self, table: str = "a", format: str = "json"):
        # Kursy walut
        self.api_url = f"https://api.nbp.pl/api/exchangerates/tables/{table}/?format={format}"
        
        # Cena złota
        self.gold_url = f"https://api.nbp.pl/api/cenyzlota/?format={format}"
        
        self.format = format

    def get_data(self):
        """
        Pobiera kursy walut oraz cenę złota
        """
        try:
            # Exchange rates
            response_rates = requests.get(self.api_url)
            response_rates.raise_for_status()
            rates_data = response_rates.json()

            # Gold prices zł / gram
            response_gold = requests.get(self.gold_url)
            response_gold.raise_for_status()
            gold_data = response_gold.json()

            return {
                "rates": rates_data,
                "gold": gold_data
            }

        except requests.exceptions.RequestException as e:
            print(f"Wystąpił błąd podczas pobierania danych: {e}")
            return None

    def convert_to_data_frame(self, data):

        if self.format == "xml":
            raise NotImplementedError("XML not implemented")

        elif self.format == "json":
            if not data:
                raise ValueError("Data not provided")

            # Exchange rates
            table_data = data["rates"][0]
            rates = table_data["rates"]

            df_rates = pd.DataFrame(rates)
            df_rates["effectiveDate"] = table_data["effectiveDate"]

            # Gold price
            gold = data["gold"][0]

            df_gold = pd.DataFrame([gold])
            df_gold.rename(columns={"data": "effectiveDate", "cena": "goldPrice"}, inplace=True)

            return df_rates, df_gold

        else:
            raise ValueError("wrong data format")

