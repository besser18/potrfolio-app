import pandas as pd
from datetime import datetime
from data.data_manager import DataManager
from external_data.currency_manager import CurrencyManager
from services.managers.dividends_manager import DividendsManager
from services.tables.capital_gains_table import CapitalGainsTable
from services.tables.cashflow_table import CashFlowTable
from services.tables.actions_table import ActionsTable

class DailySnapshotBuilder:
    """
    מחלקה זו אחראית על בניית תמונת מצב יומית מלאה של כל ההון:
    - שווי תיק מניות
    - שווי מזומן
    - שווי זהב
    - תזרים חיצוני כללי (הפקדות, משיכות, דיבידנדים, מס)
    - תזרים השקעות בלבד (דיבידנדים, מס)
    """

    def __init__(self, data_manager: DataManager, currency_manager: CurrencyManager):
        self.data_manager = data_manager
        self.currency_manager = currency_manager
        self.dividends_manager = DividendsManager(data_manager, currency_manager)
        self.capital_gains_table = CapitalGainsTable(data_manager)
        self.cash_flow_table = CashFlowTable(data_manager)
        self.actions_table = ActionsTable(data_manager)

    def build_snapshot(self, date=None) -> dict:
        date = datetime.utcnow().date()
        
        # עדכן דיבידנדים עתידיים שהגיע זמנם
        self.dividends_manager.process_due_dividends(date)

        # טען את הפרופיל הפיננסי הכולל
        profile = self.data_manager.get_profile()
        profile.update_all()

        # קבל ערכים כלליים מהפרופיל
        summary = profile.get_profile_values_report()
        portfolio_value = summary["portfolio_value"]
        cash_value = summary["cash_value"]
        gold_value = summary["gold_value"]
        total_value = summary["total_value"]
        total_ils = self.currency_manager.convert(total_value, "USD", "ILS")

        # טען את הזרימות הכספיות
        devidends_flow = self.dividends_manager.get_today_dividend_amount_usd(date)
        capital_gains_tax_usd_flow = self.capital_gains_table.get_today_capital_gains_tax_usd(date)
        deposits_usd_flow = self.cash_flow_table.get_today_deposits_usd(date)
        withdrawals_usd_flow = self.cash_flow_table.get_today_withdrawals_usd(date)

        #חישוב המניות
        amount_bought_today = self.actions_table.get_total_buy_usd_on_date(date)
        amount_sold_today = self.actions_table.get_total_sell_usd_on_date(date)
        number_of_actions = self.actions_table.get_number_of_actions_on_date(date)

        snapshot = {
            "Date": date,
            "Portfolio (USD)": portfolio_value,
            "Cash (USD)": cash_value,
            "Gold (USD)": gold_value,
            "Total (USD)": total_value,
            "Total (₪)": total_ils,
            "Dividends_usd": devidends_flow,
            "capital_gains_tax_usd": capital_gains_tax_usd_flow,
            "deposits_usd": deposits_usd_flow,
            "withdrawals_usd": withdrawals_usd_flow,
            "stock_net_flow_usd": amount_sold_today - amount_bought_today,
            "number_of_actions": number_of_actions
        }


        # --- מניעת כפילויות ושמירה ---
        df = self.data_manager.load_data("daily_snapshots")
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date
        df = df[df["Date"] != date]  # הסרת שורה קיימת לאותו תאריך
        df = pd.concat([df, pd.DataFrame([snapshot])], ignore_index=True)
        self.data_manager.save_data(df, "daily_snapshots")

        print("✅ Daily snapshot saved successfully.")

        return snapshot
