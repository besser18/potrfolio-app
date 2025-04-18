import pandas as pd
from data.data_manager import DataManager
from external_data.currency_manager import CurrencyManager
from services.managers.cash_manager import CashManager

class DividendsManager:
    """
    אחראי לעיבוד דיבידנדים עתידיים שהגיע זמנם:
    - חישוב סכום נטו לאחר מס (25%)
    - עדכון טבלת מזומן בהתאם
    - העברת השורות ל-dividends_data.csv כולל חישוב נטו
    - הסרת השורות מ-future_dividends.csv
    """

    def __init__(self, data_manager: DataManager, currency_manager: CurrencyManager):
        self.data_manager = data_manager
        self.currency_manager = currency_manager

    def process_due_dividends(self, date):
        future_df = self.data_manager.load_data("future_dividends")
        past_df = self.data_manager.load_data("dividends")
        cash_df = self.data_manager.load_data("cash")
        cash_manager = CashManager(cash_df)

        future_df["Payment Date"] = pd.to_datetime(future_df["Payment Date"], errors="coerce")
        due_df = future_df[future_df["Payment Date"].dt.date == date]

        processed = []
        for _, row in due_df.iterrows():
            cash_manager.add_cash(row["Currency"], row["Amount per Share (Local Currency)"] * row["Shares Held"] * 0.75)
            # הכנת שורת עבר
            past_row = {
                "Date": pd.to_datetime(row["Payment Date"]).date(),
                "Ticker": row["Ticker"],
                "Currency": row["Currency"],
                "Amount (original currency)": row["Amount per Share (Local Currency)"],
                "Amount in USD": row["Expected Total (USD)"],
                "Net amount in USD": row["Expected Net (USD)"],
                "Note": row.get("Note", "")
            }

            past_df = pd.concat([past_df, pd.DataFrame([past_row])], ignore_index=True)
            processed.append(row.name)

        # הסרת השורות שעובדו מהעתידיים
        future_df = future_df.drop(index=processed).reset_index(drop=True)


        # שמירה
        self.data_manager.save_data(future_df, "future_dividends")
        self.data_manager.save_data(past_df, "dividends")
        cash_manager.save()

    def get_today_dividend_amount_usd(self, date):
        df = self.data_manager.load_data("dividends")
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df[df["Date"].dt.date == date]
        df["Net amount in USD"] = pd.to_numeric(df["Net amount in USD"], errors="coerce").fillna(0)
        return df["Net amount in USD"].sum().round(2)
