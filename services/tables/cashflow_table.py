import pandas as pd
import numpy as np
from data.data_manager import DataManager
from datetime import datetime

class CashFlowTable:
    FILE_PATH = "cash_flow"

    def __init__(self, data_manager, df=None):
        self.data_manager = data_manager
        self.df = df if df is not None else pd.DataFrame(columns=[
            "Note", "Category", "Currency", "Amount", "Amount in USD", "Type", "Date", "Executed"
        ])
        for col in ["Amount", "Amount in USD"]:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors="coerce").astype("float")

    def get_default_row(self):
        return {
            "Note": "",
            "Category": "",
            "Currency": "USD",
            "Amount": 0.0,
            "Amount in USD": 0.0,
            "Type": "Income",
            "Date": datetime.today().strftime('%Y-%m-%d'),
            "Executed": False
        }
    
    def add_empty_row(self):
        new_row = self.get_default_row()
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)



    def validate_required_fields(self):
        df = self.df.copy()

        required_fields = ["Type", "Currency", "Category", "Date", "Amount"]

        # בדיקה עבור כל שורה אם יש בה ערכים חסרים או אפס ב-Amount
        for idx, row in df.iterrows():
            if (
                pd.isnull(row["Amount"]) or row["Amount"] == 0 or
                any(pd.isnull(row[field]) or row[field] == "" for field in required_fields if field != "Amount")
            ):
                return False

        return True

    def needs_calculation(self):
        if "Executed" not in self.df.columns:
            return False
        return not self.df[self.df["Executed"] != True].empty

    def fill_missing_amounts_and_usd(self, df, currency_manager):
        df["Amount"] = df.apply(
            lambda row: -abs(row["Amount"]) if row["Type"] == "Withdrawal" else abs(row["Amount"]),
            axis=1
        )

        df["Amount in USD"] = df.apply(
            lambda row: round(
                currency_manager.convert(abs(row["Amount"]), row["Currency"], "USD") *
                (-1 if row["Type"] == "Withdrawal" else 1),
                2
            ),
            axis=1
        )

        # עדכון לתוך הטבלה הראשית
        self.df.update(df)


    def process_cash_flows(self, cash_manager, currency_manager):
        """
        Processes all unexecuted cash flow entries and updates the cash manager accordingly.
        """
        # סינון שורות לביצוע
        df = self.df[self.df["Executed"] != True].copy()
        if df.empty:
            return []

        # המרות והכנות
        self.fill_missing_amounts_and_usd(df, currency_manager)

        results = []

        for i, row in df.iterrows():
            currency = row["Currency"]
            amount = float(row["Amount"])
            flow_type = row["Type"]
            note = row.get("Note", "")
            idx = row.name

            if flow_type == "Deposit":
                cash_manager.add_cash(currency, amount)
                results.append(f"✅ Deposit of {amount} {currency} {f'({note})' if note else ''}")

            elif flow_type == "Withdrawal":
                cash_manager.remove_cash(currency, abs(amount))  # רק לוודא שהכמות חיובית
                results.append(f"✅ Withdrawal of {abs(amount)} {currency} {f'({note})' if note else ''}")

            else:
                raise ValueError(f"❌ Unknown cash flow type: {flow_type}")

            self.df.at[idx, "Executed"] = True

        # שמירה
        cash_manager.save()
        self.save()

        return results


    def save(self):
        self.data_manager.save_data(self.df, self.FILE_PATH)

    def load(self):
        self.df = self.data_manager.load_data(self.FILE_PATH)

    def to_dict(self):
        return self.df.to_dict("records")

    def get_today_deposits_usd(self, date):
        self.load()
        df = self.df.copy()
        date = pd.to_datetime(date).date()
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df[df["Date"].dt.date == date]
        df = df[df["Type"].str.lower() == "deposit"]
        df["Amount in USD"] = pd.to_numeric(df["Amount in USD"], errors="coerce").fillna(0)
        return df["Amount in USD"].sum().round(2)

    def get_today_withdrawals_usd(self, date):
        self.load()
        df = self.df.copy()
        date = pd.to_datetime(date).date()
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df[df["Date"].dt.date == date]
        df = df[df["Type"].str.lower() == "withdrawal"]
        df["Amount in USD"] = pd.to_numeric(df["Amount in USD"], errors="coerce").fillna(0)
        return abs(df["Amount in USD"].sum().round(2))



