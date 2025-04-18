import pandas as pd
import numpy as np
import time
import finnhub
from data.data_manager import DataManager
from external_data.currency_manager import CurrencyManager
import requests

class StockManager:
    DEFAULT_API_KEY_FINHUB = 'cvg3hn1r01qgvsqnbbpgcvg3hn1r01qgvsqnbbq0'
    DEFAULT_API_KEY = '67fd49795d5873.83367399'
    BASE_URL = "https://eodhd.com/api"
    def __init__(self, portfolio_df: pd.DataFrame, api_key: str = None, api_key_finhub: str =None):
        self.df = portfolio_df.copy()
        self.api_key = api_key or self.DEFAULT_API_KEY
        self.api_key_finhub = api_key_finhub or self.DEFAULT_API_KEY_FINHUB
        self.client = finnhub.Client(api_key=self.api_key_finhub)
        self.currency_manager = CurrencyManager()

    def fetch_prices(self, tickers):
        prices = {}
        for symbol in tickers:
            try:
                url = f"{self.BASE_URL}/real-time/{symbol}?api_token={self.api_key}&fmt=json"
                response = requests.get(url)
                data = response.json()
                # בדיקה אם השוק פתוח (אם volume > 0 לדוגמה)
                price = data.get("close")
                if not price:
                    raise ValueError("No price in data")
                prices[symbol] = round(price, 2)
                time.sleep(0.3)  # מניעת rate-limiting
            except Exception as e:
                print(f"❌ Error fetching price for {symbol}: {e}")
        return prices


    def fetch_sectors(self, tickers):
        sector_data = {}
        for symbol in tickers:
            try:
                info = self.client.company_profile2(symbol=symbol)
                sector_data[symbol] = info.get("finnhubIndustry", "Unknown")
            except Exception:
                sector_data[symbol] = "Unknown"
        return sector_data


    def update(self):
        cols = list(self.df.columns)
        if 'Sector' in cols and 'Sub Sector' in cols:
            cols.remove('Sub Sector')
            sector_index = cols.index('Sector')
            cols.insert(sector_index + 1, 'Sub Sector')
            self.df = self.df[cols]


        self.df['Shares'] = pd.to_numeric(self.df['Shares'], errors='coerce').fillna(0).clip(lower=0)
        self.df['Bought At'] = pd.to_numeric(self.df['Bought At'], errors='coerce').fillna(0).clip(lower=0)

        tickers = self.df['Ticker'].tolist()
        prices = self.fetch_prices(tickers)
        self.df['Stock Price'] = self.df['Ticker'].map(prices)

        # סקטורים חסרים
        missing_mask = self.df['Sub Sector'].isnull() | (self.df['Sub Sector'] == '') | (self.df['Sub Sector'] == 'Unknown')
        missing_tickers = self.df.loc[missing_mask, 'Ticker'].tolist()
        if missing_tickers:
            sectors = self.fetch_sectors(missing_tickers)
            self.df.loc[missing_mask, 'Sub Sector'] = self.df.loc[missing_mask, 'Ticker'].map(sectors)
        self.df['Sector'] = self.df['Sector'].fillna('Unknown').replace('', 'Unknown')


        self.df['Current Value (Local)'] = (self.df['Shares'] * self.df['Stock Price']).fillna(0).round(2)


       

        unique_currencies = self.df['Currency'].unique()

        self.conversion_rates = {}
        for currency in unique_currencies:
            if currency == "USD":
                self.conversion_rates[currency] = 1
            else:
                rate = self.currency_manager.get_rate_between(currency, "USD")
                self.conversion_rates[currency] = rate

        self.df["Current Value in $"] = (
            self.df["Current Value (Local)"] * self.df["Currency"].map(self.conversion_rates)
        ).round(2)

        self.df["Total Cost ($)"] = (
            self.df["Shares"] * self.df["Bought At"] * self.df["Currency"].map(self.conversion_rates)
        ).round(2)

        self.df['Total Gain ($)'] = (self.df['Current Value in $'] - self.df['Total Cost ($)']).fillna(0).round(2)

        self.df['Total Return (%)'] = ((self.df['Total Gain ($)'] / self.df['Total Cost ($)'].replace(0, np.nan)).fillna(0) * 100).round(2)

        portfolio_value = self.df['Current Value in $'].sum()
        self.df['Weight (%)'] = ((self.df['Current Value in $'] / portfolio_value) * 100).fillna(0).round(2) if portfolio_value > 0 else 0


    def buy_stock(self, ticker, quantity, price, currency):
        quantity = float(quantity)
        price = float(price)

        if ticker in self.df["Ticker"].values:
            # המניה כבר קיימת – נעדכן את הכמות והמחיר הממוצע
            idx = self.df[self.df["Ticker"] == ticker].index[0]
            current_quantity = self.df.at[idx, "Shares"]
            current_avg_price = self.df.at[idx, "Bought At"]

            new_quantity = current_quantity + quantity
            new_avg_price = (
                (current_avg_price * current_quantity + price * quantity) / new_quantity
            )

            self.df.at[idx, "Shares"] = new_quantity
            self.df.at[idx, "Bought At"] = round(new_avg_price, 2)
            self.df.at[idx, "Currency"] = currency
        else:
            # מניה חדשה – נוסיף שורה
            new_row = {
                "Ticker": ticker,
                "Shares": quantity,
                "Bought At": price,
                "Currency": currency,
                "Sector": "Unknown",
                "Stock Price": 0,
                "Current Value (Local)": 0,
                "Current Value in $": 0,
                "Total Cost ($)": 0,
                "Total Gain ($)": 0,
                "Total Return (%)": 0,
                "Weight (%)": 0,
                "Stop Loss": "No Stop Loss",
                "Exit Strategy": ""
            }
            self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)

    def sell_stock(self, ticker, quantity, sell_price):
        quantity = float(quantity)
        sell_price = float(sell_price)

        if ticker not in self.df["Ticker"].values:
            raise ValueError(f"❌ Cannot sell '{ticker}' – stock not in portfolio.")

        idx = self.df[self.df["Ticker"] == ticker].index[0]
        current_quantity = self.df.at[idx, "Shares"]

        if quantity > current_quantity:
            raise ValueError(f"❌ Cannot sell {quantity} shares – only {current_quantity} available.")

        # ✅ קודם כל נחלץ את הנתונים לפני כל שינוי
        currency = self.df.at[idx, "Currency"]
        cost_basis_per_share = self.df.at[idx, "Bought At"]

        gross = round(sell_price * quantity, 2)
        cost_basis = round(cost_basis_per_share * quantity, 2)
        gain = round(gross - cost_basis, 2)
        tax = round(gain * 0.25, 2) if gain > 0 else 0
        net = round(gross - tax, 2)
        ils_net = round(self.currency_manager.convert(net, currency, "ILS"), 2)
        
        if currency == "USD":
            usd_net = net
        else:
            usd_net = round(self.currency_manager.convert(net, currency, "USD"), 2)
        date = pd.Timestamp.today().strftime('%Y-%m-%d')

        # ✅ רק עכשיו מעדכנים את הטבלה
        if quantity == current_quantity:
            self.df = self.df.drop(idx).reset_index(drop=True)
        else:
            self.df.at[idx, "Shares"] = current_quantity - quantity

        return {
            "Date": date,
            "Ticker": ticker,
            "Quantity": quantity,
            "Currency": currency,
            "Gross": gross,
            "Cost Basis": cost_basis,
            "Gain": gain,
            "Tax Paid": tax,
            "Net Received": net,
            "Net Received in ₪": ils_net,
            "Net Received in $": usd_net
        }

    
    def save(self):
        DataManager().save_data(self.df, "portfolio")       

    def get_df(self):
        return self.df

