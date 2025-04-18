from dash import Input, Output

def register_render_table_callbacks(app):

    # ✅ מציג את טבלת תיק ההשקעות
    @app.callback(
        Output("portfolio-table", "data"),
        Input("portfolio-store", "data")
    )
    def render_portfolio_table(data):
        return data

    # ✅ מציג את טבלת הניתוח (עם Stop Loss וכו')
    @app.callback(
        Output("stock-holding-table", "data"),
        Input("portfolio-store", "data")
    )
    def render_stock_holding_table(data):
        return data

    # ✅ מציג את טבלת המזומן
    @app.callback(
        Output("cash-table", "data"),
        Input("cash-store", "data")
    )
    def render_cash_table(data):
        return data

    # ✅ מציג את טבלת הזהב
    @app.callback(
        Output("gold-table", "data"),
        Input("gold-store", "data")
    )
    def render_gold_table(data):
        return data
