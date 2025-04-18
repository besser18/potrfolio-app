# utils/main_data_update.py

from typing import Optional, Dict, TypedDict
import pandas as pd
from data.data_manager import DataManager
from services.managers.financial_profile import FinancialProfile
from utils.graph_utils import PortfolioCharts

class UpdatedDataDict(TypedDict):
    portfolio: pd.DataFrame
    cash: pd.DataFrame
    gold: pd.DataFrame
    charts: PortfolioCharts

def get_updated_data(data_manager: DataManager, gold_data: Optional[list] = None) -> UpdatedDataDict:
    """
    מחזיר את כל הנתונים והגרפים המעודכנים עבור כפתור 'Save & Update'.
    """
    profile = data_manager.get_profile()

    if gold_data is not None:
        profile.gold_manager.set_data(gold_data)

    profile.update_all()
    profile.save_all()

    summary = profile.get_summary()
    charts = PortfolioCharts(
        summary["portfolio"],
        summary["cash"],
        summary["gold"]
    )

    return {
        "portfolio": summary["portfolio"],
        "cash": summary["cash"],
        "gold": summary["gold"],
        "charts": charts
    }
