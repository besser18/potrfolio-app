import requests
import pandas as pd
from datetime import datetime

API_KEY_EODHD = '67fd49795d5873.83367399'
URL_EODHD = 'https://eodhd.com/api/eod/'

def get_stock_candles(symbol, start_date='2025-01-01', end_date=datetime.today().date()):
    try:
        params = {
            'api_token': API_KEY_EODHD,
            'from': start_date,
            'to': end_date,
            'fmt': 'json',
            'period': 'd'  # daily data
        }

        response = requests.get(f"{URL_EODHD}{symbol}", params=params)
        data = response.json()

        if not isinstance(data, list):
            print(f"Error fetching data: {data.get('message', 'Unknown error')}")
            return None

        df = pd.DataFrame(data)
        df = df.rename(columns={
            'date': 'Date',
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume'
        })

        df['Date'] = pd.to_datetime(df['Date']).dt.date
        float_cols = ['Open', 'High', 'Low', 'Close']
        df[float_cols] = df[float_cols].astype(float).round(2)
        df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce').fillna(0).astype(int)
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        df = df.sort_values(by='Date').reset_index(drop=True)

        return df

    except Exception as e:
        print(f"Error in get_stock_candles function: {e}")
        return None
