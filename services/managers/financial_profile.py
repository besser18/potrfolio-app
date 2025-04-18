import pandas as pd
from services.managers.cash_manager import CashManager
from services.managers.gold_manager import GoldManager
from services.managers.stock_manager import StockManager
from services.tables.capital_gains_table import CapitalGainsTable
from data.data_manager import DataManager


class FinancialProfile:
    def __init__(self, portfolio_df: pd.DataFrame, cash_df: pd.DataFrame, gold_df: pd.DataFrame):
        self.data_manager = DataManager()

        self.stock_manager = StockManager(portfolio_df)
        self.cash_manager = CashManager(cash_df)
        self.gold_manager = GoldManager(gold_df)
        capital_gains_df = self.data_manager.load_data(CapitalGainsTable.FILE_PATH)
        self.capital_gains_table = CapitalGainsTable(data_manager=self.data_manager, df=capital_gains_df)


    def update_all(self) -> None:
        self.stock_manager.update()
        self.cash_manager.update()
        self.gold_manager.update()

    def save_all(self) -> None:
        self.stock_manager.save()
        self.cash_manager.save()
        self.gold_manager.save()
        self.capital_gains_table.save()

    def process_all_actions(self, actions_table) -> tuple[list[str], list[str]]:
        """
        מריץ את כל הפעולות מהטבלה ומעדכן את המנהלים הרלוונטיים בהתאם.
        """
        results, errors = actions_table.process_actions(
            stock_manager=self.stock_manager,
            cash_manager=self.cash_manager,
            capital_gains_table=self.capital_gains_table
        )
        return results, errors

    def get_summary(self) -> dict[str, pd.DataFrame]:
        """
        מחזיר את כל הנתונים המרכזיים בצורה פשוטה.
        """
        return {
            "portfolio": self.stock_manager.get_df(),
            "cash": self.cash_manager.get_df(),
            "gold": self.gold_manager.get_df(),
            "capital_gains": self.capital_gains_table.get_df()
        }

    def get_full_report(self) -> dict[str, dict]:
        """
        מיועד לגרפים, ניתוחים או ייצוא – מחזיר את כל המידע בפורמט dict.
        """
        summary = self.get_summary()
        return {key: df.to_dict("records") for key, df in summary.items()}

    def get_profile_values_report(self):

        summary = self.get_summary()
        portfolio_value = round(summary["portfolio"]['Current Value in $'].sum(), 2)
        cash_value = round(summary["cash"]['Value in USD'].sum(), 2)
        gold_value = round(summary["gold"]['Value'].sum(), 2)
        total_value = portfolio_value + cash_value + gold_value

        return {
            "portfolio_value": portfolio_value,
            "cash_value": cash_value,
            "gold_value": gold_value,
            "total_value": total_value
        }

