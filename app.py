# app.py
from dash import Dash
import dash_bootstrap_components as dbc

from layout.layout_main import build_main_layout
from callbacks import register_all_callbacks
from data.data_manager import DataManager

from services.managers.cash_manager import CashManager
from services.managers.gold_manager import GoldManager
from services.managers.stock_manager import StockManager

# יצירת האפליקציה
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Portfolio Tracker 📈"
server = app.server  # נדרש ל־Cloud Run

def serve_layout():
    data_manager = DataManager()

    # טען את כל הנתונים
    portfolio_df = data_manager.load_data("portfolio")
    cash_df = data_manager.load_data("cash")
    gold_df = data_manager.load_data("gold")
    stock_market_actions_data = data_manager.load_data("stock_market_actions")
    cash_flow_data = data_manager.load_data("cash_flow")
    dividends_data = data_manager.load_data("dividends")
    currency_transfer_data = data_manager.load_data("currency_transfers")
    future_dividends_data = data_manager.load_data("future_dividends")
    capital_gain_data = data_manager.load_data("capital_gains")

    # יצירת אובייקטים של מנהלים
    portfolio_manager = StockManager(portfolio_df)
    cash_manager = CashManager(cash_df)
    gold_manager = GoldManager(gold_df)

    return build_main_layout(
        portfolio_manager.get_df(),
        cash_manager.get_df(),
        gold_manager.get_df(),
        stock_market_actions_data,
        cash_flow_data,
        dividends_data,
        currency_transfer_data,
        future_dividends_data,
        capital_gain_data
    )

# קביעת layout
app.layout = serve_layout

# רישום הקולבקים
register_all_callbacks(app)

# הרצת האפליקציה
if __name__ == "__main__":
    app.run(debug=True)

