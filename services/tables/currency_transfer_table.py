import pandas as pd
from datetime import datetime
from data.data_manager import DataManager

class CurrencyTransferTable:
    FILE_PATH = "currency_transfers"

    def __init__(self, data_manager, df=None):
        self.data_manager = data_manager
        self.df = df if df is not None else pd.DataFrame(columns=[
            "Date", "From Currency", "To Currency", "Amount", "Rate",
            "Amount in To Currency", "Conversion Fee", "Net Amount Received", "Note", "Executed"
        ])
        for col in ["Amount", "Rate", "Amount in To Currency", "Conversion Fee", "Net Amount Received"]:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors="coerce").astype("float")


    def get_default_row(self):
        return {
            "Date": datetime.today().strftime('%Y-%m-%d'),
            "From Currency": "USD",
            "To Currency": "ILS",
            "Amount": 0.0,
            "Rate": 1.0,
            "Amount in To Currency": 0.0,
            "Conversion Fee": 0.0,
            "Net Amount Received": 0.0,
            "Note": "",
            "Executed": False
        }

    def add_empty_row(self):
        new_row = self.get_default_row()
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)

    def validate_required_fields(self):
        df = self.df.copy()

        # המרה לערכים נומריים
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        df["Rate"] = pd.to_numeric(df["Rate"], errors="coerce")

        # בדיקה אם אחד השדות החיוניים חסר או לא תקין
        missing_from_currency = df["From Currency"].isnull() | (df["From Currency"].astype(str).str.strip() == "")
        missing_to_currency = df["To Currency"].isnull() | (df["To Currency"].astype(str).str.strip() == "")
        invalid_amount = df["Amount"].isnull() | (df["Amount"] <= 0)
        invalid_rate = df["Rate"].isnull() | (df["Rate"] <= 0)

        any_missing = missing_from_currency | missing_to_currency | invalid_amount | invalid_rate

        return not any_missing.any()


    def needs_calculation(self):
        if "Executed" not in self.df.columns:
            return False
        return not self.df[self.df["Executed"] != True].empty

    def process_currency_transfers(self, cash_manager, currency_manager):
        mask = self.df["Executed"] != True
        messages = []

        for idx, row in self.df[mask].iterrows():
            from_curr = row["From Currency"]
            to_curr = row["To Currency"]
            amount = float(row["Amount"])
            fee = float(row.get("Conversion Fee") or 0)

            if from_curr == to_curr:
                raise ValueError(f"⚠️ Cannot convert from {from_curr} to the same currency (row {idx}).")

            rate = float(row.get("Rate") or 1)
            if rate == 1:
                rate = currency_manager.get_rate_between(from_curr, to_curr)

            if rate == 0:
                raise ValueError(f"⚠️ Invalid conversion rate (0) between {from_curr} and {to_curr} (row {idx}).")

            amount_in_to_currency = amount * rate
            net_amount = amount_in_to_currency - fee

            # עדכון ישיר של self.df
            self.df.at[idx, "Rate"] = round(rate, 4)
            self.df.at[idx, "Amount in To Currency"] = round(amount_in_to_currency, 2)
            self.df.at[idx, "Net Amount Received"] = round(net_amount, 2)
            self.df.at[idx, "Executed"] = True

            # עדכון מאזן מזומן
            cash_manager.remove_cash(from_curr, amount)
            cash_manager.add_cash(to_curr, net_amount)

            messages.append(
                f"✅ Converted {amount} {from_curr} to {round(net_amount, 2)} {to_curr} (Rate: {round(rate, 4)})"
            )

        self.save()
        return messages


    def save(self):
        self.data_manager.save_data(self.df, self.FILE_PATH)

    def load(self):
        self.df = self.data_manager.load_data(self.FILE_PATH)

    def to_dict(self):
        return self.df.to_dict("records")
