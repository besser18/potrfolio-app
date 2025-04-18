import pandas as pd
from data.data_manager import DataManager

class CapitalGainsTable:
    FILE_PATH = "capital_gains"

    def __init__(self, data_manager: DataManager, df=None):
        self.data_manager = data_manager
        self.df = self.data_manager.load_data(self.FILE_PATH)

    def add_entry(
        self, date, ticker, quantity, gross, cost_basis,
        gain, tax_paid, net_received, currency, net_ils, net_usd
        ):

        new_row = {
            "Date": date,
            "Ticker": ticker,
            "Quantity": float(quantity),
            "Gross": float(gross),
            "Cost Basis": float(cost_basis),
            "Gain": float(gain),
            "Tax Paid": float(tax_paid),
            "Net Received": float(net_received),
            "Currency": currency,
            "Net Received in ₪": float(net_ils),
            "Net Received in $": float(net_usd)
        }

        entry_df = pd.DataFrame([new_row])
        self.df = pd.concat([self.df, entry_df], ignore_index=True)

    def save(self):
        self.data_manager.save_data(self.df, self.FILE_PATH)

    def load(self):
        return self.data_manager.load_data(self.FILE_PATH)

    def to_dict(self):
        return self.df.to_dict("records")

    def to_dataframe(self):
        return self.df

    def get_last_entry(self):
        if not self.df.empty:
            return self.df.tail(1).to_dict("records")[0]
        return None

    def get_df(self):
        return self.df
    
    def get_today_capital_gains_tax_usd(self, date):
        df = self.get_df()
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df[df["Date"].dt.date == date]
        df.loc[:, "Tax Paid"] = pd.to_numeric(df["Tax Paid"], errors="coerce").fillna(0)
        return df["Tax Paid"].sum().round(2)
