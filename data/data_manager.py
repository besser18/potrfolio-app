import pandas as pd
import os
from google.cloud import storage
from io import StringIO


class DataManager:
    def __init__(self):
        self.IS_CLOUD = os.environ.get("GAE_ENV") is not None or os.environ.get("K_SERVICE") is not None
        self.BUCKET_NAME = 'portfolio-app-data'
        self.DATA_FOLDER = "data/" if not self.IS_CLOUD else ""

        self.FILE_PATHS = {
            'portfolio': os.path.join(self.DATA_FOLDER, "portfolio_data.csv") if not self.IS_CLOUD else "portfolio_data.csv",
            'cash': os.path.join(self.DATA_FOLDER, "cash_data.csv") if not self.IS_CLOUD else "cash_data.csv",
            'gold': os.path.join(self.DATA_FOLDER, "gold_data.csv") if not self.IS_CLOUD else "gold_data.csv",
            'stock_market_actions': os.path.join(self.DATA_FOLDER, "stock_market_actions.csv") if not self.IS_CLOUD else "stock_market_actions.csv",
            'cash_flow': os.path.join(self.DATA_FOLDER, "cash_flow_data.csv") if not self.IS_CLOUD else "cash_flow_data.csv",
            'dividends': os.path.join(self.DATA_FOLDER, "dividends_data.csv") if not self.IS_CLOUD else "dividends_data.csv",
            'currency_transfers': os.path.join(self.DATA_FOLDER, "currency_transfers.csv") if not self.IS_CLOUD else "currency_transfers.csv",
            'future_dividends': os.path.join(self.DATA_FOLDER, "future_dividends.csv") if not self.IS_CLOUD else "future_dividends.csv",
            'capital_gains': os.path.join(self.DATA_FOLDER, "capital_gains.csv") if not self.IS_CLOUD else "capital_gains.csv",
            'daily_snapshots': os.path.join(self.DATA_FOLDER, "daily_snapshots.csv") if not self.IS_CLOUD else "daily_snapshots.csv"
        }

        self.DEFAULTS = {
            'portfolio': {
                'data': {
                    'Ticker': ['VOO', 'QQQ', 'AMZN'],
                    'Shares': [13, 12, 40],
                    'Bought At': [14, 460.21, 186.3],
                    'Stock Price': [0, 0, 0],
                    'Current Value (Local)': [0, 0, 0],
                    'Current Value in $': [0, 0, 0],
                    'Total Cost ($)': [0, 0, 0],
                    'Total Gain ($)': [0, 0, 0],
                    'Total Return (%)': [0, 0, 0],
                    'Weight (%)': [0, 0, 0],
                    'Sector': ['ETF', 'ETF', 'Technology'],
                    'Sub Sector': ['Unknown'] * 3,
                    'Stop Loss': [''] * 3,
                    'Exit Strategy': [''] * 3,
                    'Currency': ['USD', 'USD', 'USD']
                },
                'dtypes': {
                    "Shares": "int", "Bought At": "float", "Stock Price": "float",
                    "Current Value (Local)": "float", "Current Value in $": "float", "Total Cost ($)": "float",
                    "Total Gain ($)": "float", "Total Return (%)": "float", "Weight (%)": "float", 'Stop Loss': 'str',
                }
            },

            'cash': {
                'data': {"Currency": ["USD", "ILS"], "Balance": [0, 0], "Value in USD": [0, 0]},
                'dtypes': {"Balance": "float", "Value in USD": "float"}
            },
            'gold': {
                'data': {"Type": ["Gold (grams)"], "Amount": [0], "Value": [0]},
                'dtypes': {"Amount": "float", "Value": "int"}
            },
            'stock_market_actions': {
                'data': {
                    'Note': [], 'Action': [], 'Currency': [], 'Ticker': [], 'Price': [],
                    'Quantity': [], 'Total Price of Action': [], 'Total Price of Action in $': [],
                    'Date': [], 'Commission': [], 'Executed': []
                },
                'dtypes': {
                    'Price': 'float', 'Quantity': 'float', 'Total Price of Action': 'float',
                    'Total Price of Action in $': 'float', 'Commission': 'float', 'Executed': 'bool'
                }
            },
            'cash_flow': {
                'data': {
                    'Note': [], 'Category': [], 'Currency': [], 'Amount': [],
                    'Amount in USD': [], 'Type': [], 'Date': [], 'Executed': []
                },
                'dtypes': {'Amount': 'float', 'Amount in USD': 'float', 'Executed': 'bool'}
            },
            'dividends': {
                'data': {
                    'Date': [], 'Ticker': [], 'Currency': [],
                    'Amount (original currency)': [], 'Amount in USD': [], 'Net amount in USD':[],'Note': []
                },
                'dtypes': {
                    'Amount (original currency)': 'float', 'Amount in USD': 'float', 'Net amount in USD': 'float'
                }
            },
            'currency_transfers': {
                'data': {
                    'Date': [], 'From Currency': [], 'To Currency': [], 'Amount': [],
                    'Rate': [], 'Amount in To Currency': [], 'Conversion Fee': [],
                    'Net Amount Received': [], 'Note': [], 'Executed': []
                },
                'dtypes': {
                    'Amount': 'float', 'Rate': 'float', 'Amount in To Currency': 'float',
                    'Conversion Fee': 'float', 'Net Amount Received': 'float', 'Executed': 'bool'
                }
            },
            'future_dividends': {
                'data': {
                    'Ex-Date': [], 'Payment Date': [], 'Ticker': [], 'Currency': [],
                    'Amount per Share (Local Currency)': [], 'Shares Held': [],
                    'Amount per Share (USD)': [], 'Expected Total (USD)': [], 'Note': [], 'Expected Net (USD)': []
                },
                'dtypes': {
                    'Amount per Share (Local Currency)': 'float', 'Shares Held': 'int',
                    'Amount per Share (USD)': 'float', 'Expected Total (USD)': 'float', 'Expected Net (USD)': 'float'
                }
            },

            'capital_gains': {
                'data': {
                    'Date': [],'Ticker': [], 'Quantity': [],
                    'Gross': [], 'Cost Basis': [], 'Gain': [], 'Tax Paid': [],
                    'Net Received': [], 'Currency': [], 'Net Received in ₪': [], 'Net Received in $': []
                },
                'dtypes': {
                    'Quantity': 'float', 'Gross': 'float', 'Cost Basis': 'float', 'Gain': 'float',
                    'Tax Paid': 'float', 'Net Received': 'float', 'Net Received in ₪': 'float', 'Net Received in $': 'float'
                },
            },
            'daily_snapshots': {
                'data': {
                    'Date': [], 'Portfolio (USD)': [], 'Cash (USD)': [], 'Gold (USD)': [],
                    'Total (USD)': [], 'Total (₪)': [], 'Dividends_usd': [], 'capital_gains_tax_usd': [],
                    'deposits_usd': [], 'withdrawals_usd': [], 'stock_net_flow_usd': [],'number_of_actions': []
                },
                'dtypes': {
                    'Portfolio (USD)': 'float', 'Cash (USD)': 'float', 'Gold (USD)': 'float', 'Total (USD)': 'float',
                    'Total (₪)': 'float', 'Dividends_usd': 'float', 'capital_gains_tax_usd': 'float',
                    'deposits_usd': 'float', 'withdrawals_usd': 'float', 'stock_net_flow_usd': 'float', 'number_of_actions': 'int'
                }
            }
        }

    def load_data(self, name):
        file_path = self.FILE_PATHS[name]
        default_data = self.DEFAULTS[name]['data']
        dtype_mapping = self.DEFAULTS[name]['dtypes']

        df = None

        if self.IS_CLOUD:
            try:
                client = storage.Client()
                bucket = client.bucket(self.BUCKET_NAME)
                blob = bucket.blob(file_path)

                if blob.exists():
                    df = pd.read_csv(StringIO(blob.download_as_text()))
                else:
                    print(f"⚠️ {file_path} not found in GCS, creating default.")
            except Exception as e:
                print(f"❌ Error loading {file_path} from GCS: {e}")
        else:
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                try:
                    df = pd.read_csv(file_path)
                except Exception as e:
                    raise Exception(f"❌ File {file_path} is unreadable.\n{e}")

        if df is None or df.empty:
            df = pd.DataFrame(self.DEFAULTS[name]['data'])

        for col, dtype in dtype_mapping.items():
            if col in df.columns:
                try:
                    if dtype in ["float", "float64", "int", "int64"]:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    elif dtype in ["str", "string"]:
                        df[col] = df[col].astype(str)
                    elif dtype == "bool":
                        df[col] = df[col].astype(bool)
                    elif dtype in ["datetime64[ns]", "datetime"]:
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                    else:
                        df[col] = df[col].astype(dtype)
                except Exception as e:
                    print(f"❌ Error casting column {col} to {dtype} in {name}: {e}")
                    raise

            

        df = df.astype(dtype_mapping)
        self.save_data(df, name)


        return df

    def save_data(self, df, name):
        file_path = self.FILE_PATHS[name]
        try:
            if self.IS_CLOUD:
                client = storage.Client()
                bucket = client.bucket(self.BUCKET_NAME)
                blob = bucket.blob(file_path)
                blob.upload_from_string(df.to_csv(index=False), content_type='text/csv')
            else:
                df.to_csv(file_path, index=False, mode='w')
        except Exception as e:
            raise Exception(f"❌ Error saving file {file_path}:\n{e}")


    def get_profile(self, portfolio_df=None, cash_df=None, gold_df=None):
        from services.managers.financial_profile import FinancialProfile
        if portfolio_df is None:
            portfolio_df = self.load_data("portfolio")
        if cash_df is None:
            cash_df = self.load_data("cash")
        if gold_df is None:
            gold_df = self.load_data("gold")
        return FinancialProfile(portfolio_df, cash_df, gold_df)
