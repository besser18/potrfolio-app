# 💰 CashManager
import pandas as pd
from external_data.currency_manager import CurrencyManager
from data.data_manager import DataManager

class CashManager:
    def __init__(self, cash_df: pd.DataFrame):
        self.df = cash_df.copy()
        self.currency = CurrencyManager()

    def update(self):
        self.df["Balance"] = pd.to_numeric(self.df["Balance"], errors="coerce").fillna(0)

        def convert(row):
            if row["Currency"] == "USD":
                return round(row["Balance"], 2)
            return round(self.currency.convert(row["Balance"], row["Currency"], "USD"), 2)

        self.df["Value in USD"] = self.df.apply(convert, axis=1)

    def add_cash(self, currency: str, amount: float):
        amount = float(amount)
        currency = currency.upper()

        # אם המטבע כבר קיים, נוסיף אליו
        if currency in self.df["Currency"].values:
            idx = self.df[self.df["Currency"] == currency].index[0]
            self.df.at[idx, "Balance"] += amount
        else:
            # אם לא קיים, נוסיף שורה חדשה
            new_row = {
                "Currency": currency,
                "Balance": amount,
                "Value in USD": 0  # יתעדכן בפונקציית update()
            }
            self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)

        self.update()  # לעדכון 'Value in USD'


    def remove_cash(self, currency: str, amount: float):
        amount = float(amount)
        currency = currency.upper()

        if currency in self.df["Currency"].values:
            idx = self.df[self.df["Currency"] == currency].index[0]
            self.df.at[idx, "Balance"] -= amount

            # אם היתרה היא בדיוק אפס – נמחק את השורה
            if self.df.at[idx, "Balance"] == 0:
                self.df = self.df.drop(idx).reset_index(drop=True)
        else:
            # אם המטבע לא קיים – נוסיף שורה עם יתרה שלילית
            new_row = {
                "Currency": currency,
                "Balance": -amount,
                "Value in USD": 0  # יתעדכן ב-update
            }
            self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)

        self.update()




    def save(self):
        DataManager().save_data(self.df, "cash")

    def get_df(self):
        return self.df