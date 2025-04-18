import pandas as pd
import numpy as np
from data.data_manager import DataManager

class FutureDividendsTable:
    FILE_PATH = "future_dividends"

    def __init__(self, data_manager, df=None):
        self.data_manager = data_manager
        self.df = df if df is not None else pd.DataFrame(columns=[
            "Ex-Date", "Payment Date", "Ticker", "Amount per Share (USD)", 
            "Shares Held", "Expected Total (USD)", "Note", "Currency", 
            "Amount per Share (Local Currency)"
        ])

    def add_empty_row(self):
        new_row = {
            "Ex-Date": "",
            "Payment Date": "", 
            "Ticker": "",
            "Currency": "",
            "Amount per Share (Local Currency)": 0.0,
            "Amount per Share (USD)": 0.0, 
            "Shares Held": 0.0,
            "Expected Total (USD)": 0.0,
            'Expected Net (USD)': 0.0,
            "Note": ""
        }
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)

    def validate_required_fields(self):
        df = self.df.copy()

        required_fields = [
            "Ex-Date", "Payment Date", "Ticker", "Currency", "Amount per Share (Local Currency)"
        ]

        missing_values = {}

        for field in required_fields:
            missing = df[df[field] == ""]
            if not missing.empty:
                missing_values[field] = missing.index.tolist()

        return not missing_values

    def calculate_expected_total(self, currency_manager):
        # טען את פורטפוליו המניות והכנס את כמות המניות לכל טיקר
        portfolio_df = self.data_manager.load_data("portfolio")
        ticker_to_shares = portfolio_df.set_index('Ticker')["Shares"].to_dict()
        self.df["Shares Held"] = self.df["Ticker"].map(ticker_to_shares).fillna(0)
    

        # ודא שהעמודות הרלוונטיות הן מספריות
        self.df["Amount per Share (Local Currency)"] = pd.to_numeric(self.df["Amount per Share (Local Currency)"], errors="coerce").fillna(0)

        self.df["Shares Held"] = pd.to_numeric(self.df["Shares Held"], errors="coerce").fillna(0)

        # המרת מטבע במידת הצורך
        self.df["Amount per Share (USD)"] = self.df.apply(
            lambda row: currency_manager.convert(
                row["Amount per Share (Local Currency)"], row["Currency"], "USD"
            ) if row["Currency"] != "USD" else row["Amount per Share (Local Currency)"],
            axis=1
        )

        self.df["Amount per Share (USD)"] = pd.to_numeric(self.df["Amount per Share (USD)"], errors="coerce").fillna(0)

        # חישוב הסכום הצפוי
        self.df["Expected Total (USD)"] = (
            self.df["Amount per Share (USD)"] * self.df["Shares Held"]
        ).round(2)

        self.df['Expected Net (USD)'] = (self.df['Expected Total (USD)'] * 0.75).round(2)

        self.df = self.df[self.df["Shares Held"] > 0].reset_index(drop=True)




    def save(self):
        self.data_manager.save_data(self.df, self.FILE_PATH)

    def load(self):
        self.df = self.data_manager.load_data(self.FILE_PATH)

    def to_dict(self):
        return self.df.to_dict("records")