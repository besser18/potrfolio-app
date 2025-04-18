from dash import Input, Output, dcc
from data.data_manager import DataManager
from services.managers.cash_manager import CashManager
from services.managers.gold_manager import GoldManager
from services.managers.stock_manager import StockManager

data_manager = DataManager()

def register_download_callbacks(app):

    # ===================================================
    # 🔹 טאב ראשון: Portfolio / Cash / Gold
    # ===================================================

    @app.callback(
        Output("download-portfolio-csv", "data"),
        Input("download-portfolio-cvs-button", "n_clicks"),
        prevent_initial_call=True
    )
    def download_portfolio(n_clicks):
        df = data_manager.load_data("portfolio")
        stock_manager = StockManager(df)
        return dcc.send_data_frame(stock_manager.get_df().to_csv, "portfolio_data.csv")

    @app.callback(
        Output("download-cash-csv", "data"),
        Input("download-cash-cvs-button", "n_clicks"),
        prevent_initial_call=True
    )
    def download_cash(n_clicks):
        df = data_manager.load_data("cash")
        cash_manager = CashManager(df)
        return dcc.send_data_frame(cash_manager.get_df().to_csv, "cash_data.csv")

    @app.callback(
        Output("download-gold-csv", "data"),
        Input("download-gold-cvs-button", "n_clicks"),
        prevent_initial_call=True
    )
    def download_gold(n_clicks):
        df = data_manager.load_data("gold")
        gold_manager = GoldManager(df)
        return dcc.send_data_frame(gold_manager.get_df().to_csv, "gold_data.csv")

    # ===================================================
    # 🔹 טאב שני: Actions / Cash Flow / Dividends / Currency Transfers
    # ===================================================

    @app.callback(
        Output("download-stock-market-actions-csv", "data"),
        Input("download-stock-market-actions-csv-button", "n_clicks"),
        prevent_initial_call=True
    )
    def download_actions(n_clicks):
        df = data_manager.load_data("stock_market_actions")
        return dcc.send_data_frame(df.to_csv, "stock_market_actions.csv")

    @app.callback(
        Output("download-cash-flow-csv", "data"),
        Input("download-cash-flow-csv-button", "n_clicks"),
        prevent_initial_call=True
    )
    def download_cash_flow(n_clicks):
        df = data_manager.load_data("cash_flow")
        return dcc.send_data_frame(df.to_csv, "cash_flow_data.csv")

    @app.callback(
        Output("download-dividends-csv", "data"),
        Input("download-dividends-csv-button", "n_clicks"),
        prevent_initial_call=True
    )
    def download_dividends(n_clicks):
        df = data_manager.load_data("dividends")
        return dcc.send_data_frame(df.to_csv, "dividends_data.csv")

    @app.callback(
        Output("download-currency-transfers-csv", "data"),
        Input("download-currency-transfers-csv-button", "n_clicks"),
        prevent_initial_call=True
    )
    def download_currency(n_clicks):
        df = data_manager.load_data("currency_transfers")
        return dcc.send_data_frame(df.to_csv, "currency_transfers.csv")

    # ===================================================
    # 🔹 טאב שלישי: Holdings / Future Dividends
    # ===================================================

    @app.callback(
        Output("download-stock-holdings-csv", "data"),
        Input("download-stock-holdings-csv-button", "n_clicks"),
        prevent_initial_call=True
    )
    def download_holdings(n_clicks):
        df = data_manager.load_data("portfolio")
        stock_manager = StockManager(df)
        return dcc.send_data_frame(stock_manager.get_df().to_csv, "portfolio_data.csv")

    @app.callback(
        Output("download-future-dividend-csv", "data"),
        Input("download-future-dividend-csv-button", "n_clicks"),
        prevent_initial_call=True
    )
    def download_future_dividends(n_clicks):
        df = data_manager.load_data("future_dividends")
        return dcc.send_data_frame(df.to_csv, "future_dividends.csv")

