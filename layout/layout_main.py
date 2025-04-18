#layout_main.py
from dash import html, dcc
import dash_bootstrap_components as dbc
from layout.overview_layout.overview_tab import build_overview_tab
from layout.management_layout.management_tab import build_management_tab
from layout.stock_analysis_layout.stock_analysis_tab import build_stock_analysis_tab  

def build_main_layout(portfolio_data, cash_data, gold_data, stock_market_actions_data, cash_flow_data, dividends_data, currency_transfer_data, future_dividends_data, capital_gains):
    overview_tab = build_overview_tab(portfolio_data, cash_data, gold_data)
    management_tab = build_management_tab(stock_market_actions_data, cash_flow_data, dividends_data, currency_transfer_data)
    stock_analysis_tab = build_stock_analysis_tab(portfolio_data, future_dividends_data)  

    return dbc.Container([
        dcc.Interval(id="initial-load-trigger", interval=1, n_intervals=0, max_intervals=1),
        dcc.Store(id="portfolio-store"),
        dcc.Store(id="cash-store"),
        dcc.Store(id="gold-store"),

        dbc.Tabs(
            [
                dbc.Tab(overview_tab, label="Overview", tab_id="overview"),
                dbc.Tab(management_tab, label="Management", tab_id="management"),
                dbc.Tab(stock_analysis_tab, label="Stock Holding Analysis", tab_id="stock-analysis")
            ],
            id="main-tabs",
            active_tab="overview",
            className="mb-3"
        )
    ], fluid=True)