# ⭐ GoldManager
import pandas as pd
from external_data.gold_price_fetcher import GoldPriceFetcher
from data.data_manager import DataManager

class GoldManager:
    def __init__(self, gold_df: pd.DataFrame):
        self.df = gold_df.copy()
        self.gold_fetcher = GoldPriceFetcher()

    def update(self):
        self.df["Amount"] = pd.to_numeric(self.df["Amount"], errors="coerce").fillna(0)
        self.df["Value"] = self.df["Amount"].apply(self.gold_fetcher.calculate_price_for_grams)

    def save(self):
        DataManager().save_data(self.df, "gold")

    def get_df(self):
        return self.df
    def set_data(self, new_data):
        self.df = pd.DataFrame(new_data)
