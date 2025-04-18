import pandas as pd
import numpy as np
from data.data_manager import DataManager


data_manager = DataManager()

class ActionsTable:
    FILE_PATH = "stock_market_actions"

    def __init__(self, data_manager, df=None):
        self.data_manager = data_manager
        self.df = pd.DataFrame(df).copy() if df is not None else pd.DataFrame(columns=[
            "Note", "Action", "Currency", "Ticker", "Price", "Quantity",
            "Commission", "Total Price of Action", "Total Price of Action in $", "Date"
        ])



    def get_default_row(self):
        return {
            "Note": "",
            "Action": "",
            "Currency": "",
            "Ticker": "",
            "Price": 0,
            "Quantity": 0,
            "Commission": 0,
            "Total Price of Action": 0,
            "Total Price of Action in $": 0,
            "Date": "",
            "Executed": False
        }

    def add_row(self, date=None):
        new_row = self.get_default_row()
        if date:
            new_row["Date"] = date
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)

    def add_empty_row(self):
        self.add_row()

    def validate_required_fields(self):
        df = self.df.copy()

        df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
        df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")

        cond_action = df["Action"].isnull() | (df["Action"] == "")
        cond_currency = df["Currency"].isnull() | (df["Currency"] == "")
        cond_ticker = df["Ticker"].isnull() | (df["Ticker"] == "")
        cond_date = df["Date"].isnull() | (df["Date"] == "")

        cond_price = df["Price"].isnull() | (df["Price"] <= 0)
        cond_quantity = df["Quantity"].isnull() | (df["Quantity"] <= 0)

        missing = cond_action | cond_currency | cond_ticker | cond_date | cond_price | cond_quantity

        return not missing.any()


    def needs_calculation(self):
        return not self.df[self.df["Executed"] != True].empty


    def fill_missing_total_prices(self):

        try:
            mask = self.df["Total Price of Action"].isnull() | (self.df["Total Price of Action"] == 0)

            prices = self.df.loc[mask, "Price"].astype(float)
            quantities = self.df.loc[mask, "Quantity"].astype(float)
            commissions = self.df.loc[mask, "Commission"].astype(float)
            is_sell = self.df.loc[mask, "Action"] == "Sell"

            signs = np.where(is_sell, -1, 1)
            total_price = (prices * quantities + commissions) * signs

            self.df["Total Price of Action"] = self.df["Total Price of Action"].astype(float)
            self.df.loc[mask, "Total Price of Action"] = np.round(total_price, 2)

        except Exception as e:
            print(f"❌ Error in fill_missing_total_prices: {e}")
            raise


    def fill_missing_usd_prices(self, currency_manager):

        try:
            mask = self.df["Total Price of Action in $"].isnull() | (self.df["Total Price of Action in $"] == 0)

            converted_values = []

            for idx in self.df[mask].index:
                try:
                    row = self.df.loc[idx]

                    if row["Currency"] == "USD":
                        converted = row["Total Price of Action"]
                    else:
                        rate = currency_manager.get_rate_between(row["Currency"], "USD")
                        converted = row["Total Price of Action"] * rate

                    # להבטיח טיפוס float נקי
                    converted = float(round(converted, 2))
                    converted_values.append(converted)

                except Exception as inner_e:
                    print(f"❌ Failed to convert row {idx}: {inner_e}")
                    converted_values.append(0.0)

            self.df["Total Price of Action in $"] = self.df["Total Price of Action in $"].astype(float)
            self.df.loc[mask, "Total Price of Action in $"] = converted_values

        except Exception as e:
            print(f"❌ Critical error in fill_missing_usd_prices: {e}")
            raise





    def save(self):
        self.data_manager.save_data(self.df, self.FILE_PATH)

    def load(self):
        self.df = self.data_manager.load_data(self.FILE_PATH)

    def to_dict(self):
        return self.df.to_dict("records")

    def process_actions(self, stock_manager, cash_manager, capital_gains_table):
        """
        Processes all unexecuted actions in the action table.
        Executes buys/sells, updates stock and cash managers, and logs capital gains.
        Raises exceptions on any invalid data.
        """
        # חישוב מחירים חסרים
        self.fill_missing_total_prices()
        self.fill_missing_usd_prices(currency_manager=stock_manager.currency_manager)

        # סינון שורות לביצוע
        df = self.df[self.df["Executed"] != True].copy()
        if df.empty:

            return [], []

        results = []

        for i, row in df.iterrows():
            if not row["Date"]:
                raise ValueError(f"❌ Row {i+1} skipped – missing date.")

            action = str(row["Action"])
            ticker = str(row["Ticker"])
            quantity = float(row["Quantity"])
            price = float(row["Price"])
            currency = str(row["Currency"])
            commission = float(row.get("Commission") or 0)

            print(f"➡️ Processing {action} for {ticker} – Qty: {quantity}, Price: {price}, Currency: {currency}")

            if action == "Buy":
                stock_manager.buy_stock(ticker, quantity, price, currency)
                cash_manager.remove_cash(currency, quantity * price + commission)

            elif action == "Sell":
                sell_result = stock_manager.sell_stock(ticker, quantity, price)

                if not isinstance(sell_result, dict):
                    raise TypeError("sell_stock did not return a dictionary")

                net_after_commission = sell_result["Net Received"] - commission
                cash_manager.add_cash(sell_result["Currency"], net_after_commission)

                capital_gains_table.add_entry(
                    sell_result["Date"],
                    sell_result["Ticker"],
                    sell_result["Quantity"],
                    sell_result["Gross"],
                    sell_result["Cost Basis"],
                    sell_result["Gain"],
                    sell_result["Tax Paid"],
                    sell_result["Net Received"],
                    sell_result["Currency"],
                    sell_result["Net Received in ₪"],
                    sell_result["Net Received in $"]
                )

            else:
                raise ValueError(f"❌ Unknown action type: '{action}'")

            self.df.at[i, "Executed"] = True
            results.append(f"✅ {action} {quantity} of {ticker}")

        return results, []
    

    def get_total_buy_usd_on_date(self, date: pd.Timestamp) -> float:
        self.load()
        df = self.df.copy()
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df[df["Date"].dt.date == date]
        df = df[df["Action"] == "Buy"]
        df["Total Price of Action in $"] = pd.to_numeric(df["Total Price of Action in $"], errors="coerce").fillna(0)
        return df["Total Price of Action in $"].sum().round(2)

    def get_total_sell_usd_on_date(self, date: pd.Timestamp) -> float:
        self.load()
        df = self.df.copy()
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df[df["Date"].dt.date == date]
        df = df[df["Action"] == "Sell"]
        df["Total Price of Action in $"] = pd.to_numeric(df["Total Price of Action in $"], errors="coerce").fillna(0)
        return df["Total Price of Action in $"].sum().round(2)

    def get_number_of_actions_on_date(self, date: pd.Timestamp) -> int:
        self.load()
        df = self.df.copy()
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df[df["Date"].dt.date == date]
        return len(df)

