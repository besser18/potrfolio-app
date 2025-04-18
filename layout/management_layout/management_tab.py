from dash import html
import dash_bootstrap_components as dbc
from layout.management_layout.management_components import (
    build_stock_market_action_table,
    get_stock_market_actions_buttons_cols,
    build_toasts,
    build_modals,
    build_cash_flow_table,
    get_cash_flow_buttons_cols,
    get_download_buttons_cols,
    build_dividend_table,
    build_currency_transfer_table,
    get_currency_transfer_buttons_cols
)


def build_management_tab(stock_market_actions_data, cash_flow_data, dividends_data, currency_transfer_data):
    action_update_save_or_add_row_toast, cash_flow_update_toast, currency_transfer_toast= build_toasts()
    confirm_save_modal, cash_flow_save_modal, currency_transfer_modal = build_modals()

    return dbc.Container([
        html.Div([
            action_update_save_or_add_row_toast,
            confirm_save_modal,
            cash_flow_update_toast,
            cash_flow_save_modal,
            currency_transfer_toast,
            currency_transfer_modal
        ]),

        dbc.Row([
            dbc.Col(html.H1("Stock Market Actions", className='text-center text-info font-weight-bolder'), width=12)
        ]),

        dbc.Row([
            dbc.Col(build_stock_market_action_table(stock_market_actions_data), xl=10, lg=10, md=12, sm=12, xs=12)
        ], justify='center'),

        dbc.Row(get_stock_market_actions_buttons_cols(), className="d-flex justify-content-end gap-2 mt-2"),

        html.Hr(),

        dbc.Row([
            dbc.Col(html.H1("Cash Flow", className='text-center text-info font-weight-bolder'), width=12)
        ]),

        dbc.Row([
            dbc.Col(build_cash_flow_table(cash_flow_data), xl=10, lg=10, md=12, sm=12, xs=12)
        ], justify='center'),

        dbc.Row(get_cash_flow_buttons_cols(), className="d-flex justify-content-end gap-2 mt-2"),

        html.Hr(),

        dbc.Row([
            dbc.Col(html.H1("All Past Dividend", className='text-center text-info font-weight-bolder'), width=12)
        ]),

        dbc.Row([
            dbc.Col(build_dividend_table(dividends_data), xl=10, lg=10, md=12, sm=12, xs=12)
        ], justify='center'),

        html.Hr(),

        dbc.Row([
            dbc.Col(html.H1("Currency Transfer", className='text-center text-info font-weight-bolder'), width=12)
        ]),

        dbc.Row([
            dbc.Col(build_currency_transfer_table(currency_transfer_data), xl=10, lg=10, md=12, sm=12, xs=12)
        ], justify='center'),

        dbc.Row(get_currency_transfer_buttons_cols(), className="d-flex justify-content-end gap-2 mt-2"),

        html.Hr(),

        dbc.Row([
            dbc.Col(html.H3("Download files:"))
        ]),
        dbc.Row(get_download_buttons_cols(), justify="start", className="gap-2 mt-3")

    ], fluid=True, style={'padding': '20px'})