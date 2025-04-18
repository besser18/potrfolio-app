#management_components.py
import dash_bootstrap_components as dbc
from dash import dcc, dash_table
from layout.shared_components import (
    create_button, create_toast, create_confirm_save_modal, generate_date_options, get_common_table_args)
from datetime import datetime, timedelta
import pandas as pd


def build_toasts():
    return [create_toast("action-update-save-or-add-row-toast", top=20),
            create_toast("cash-flow-update-save-or-add-row-toast", top=100),
            create_toast("currency-transfer-update-save-or-add-row-toast", top=180)
            ]

def build_modals():
    return[
        create_confirm_save_modal(modal_id="confirm-save-modal",confirm_button_id="confirm-save-modal-confirm-button",cancel_button_id="confirm-save-modal-cancel-button"),
        create_confirm_save_modal(modal_id="confirm-cash-flow-save-modal",confirm_button_id="confirm-cash-flow-save-modal-confirm-button",cancel_button_id="confirm-cash-flow-save-modal-cancel-button"),
        create_confirm_save_modal(modal_id="confirm-currency-transfer-save-modal", confirm_button_id="confirm-currency-transfer-save-modal-confirm-button", cancel_button_id="confirm-currency-transfer-save-modal-cancel-button")
    ]

def build_stock_market_action_table(df):
    if df.empty:
        df = pd.DataFrame({
            'Note': [''],
            'Action': ['Buy'],
            'Currency': ['USD'],
            'Ticker': [''],
            'Price': [0.0],
            'Quantity': [0.0],
            'Total Price of Action': [0.0],
            'Total Price of Action in $': [0.0],
            'Date': [datetime.today().strftime('%Y-%m-%d')],
            'Commission': [0.0],
            'Executed': [False],
        })

    columns = [
        {'name': 'Note', 'id': 'Note', 'editable': True},
        {'name': 'Action', 'id': 'Action', 'editable': True, 'presentation': 'dropdown'},
        {'name': 'Currency', 'id': 'Currency', 'editable': True, 'presentation': 'dropdown'},
        {'name': 'Ticker', 'id': 'Ticker', 'editable': True},
        {'name': 'Price', 'id': 'Price', 'type': 'numeric', 'editable': True},
        {'name': 'Quantity', 'id': 'Quantity', 'type': 'numeric', 'editable': True},
        {'name': 'Total Price of Action', 'id': 'Total Price of Action', 'type': 'numeric', 'editable': False},
        {'name': 'Total Price of Action in $', 'id': 'Total Price of Action in $', 'type': 'numeric', 'editable': False},
        {'name': 'Date', 'id': 'Date', 'editable': True, 'presentation': 'dropdown'},
        {'name': 'Commission', 'id': 'Commission', 'type': 'numeric', 'editable': True},
        {'name': 'Executed', 'id': 'Executed', 'type': 'text', 'editable': False}
    ]

    dropdown = {
        'Action': {
            'options': [{'label': 'Buy', 'value': 'Buy'}, {'label': 'Sell', 'value': 'Sell'}]
        },
        'Currency': {
            'options': [
                {'label': 'USD', 'value': 'USD'},
                {'label': 'ILS', 'value': 'ILS'},
                {'label': 'EUR', 'value': 'EUR'},
                {'label': 'GBP', 'value': 'GBP'}
            ]
        },
        'Date': {
            'options': generate_date_options(8)
        }
    }

    args = get_common_table_args(table_id='stock-market-action-table', columns=columns, data=df.to_dict('records'), dropdown=dropdown, page_size=10)

    return dash_table.DataTable(**args)


def get_stock_market_actions_buttons_cols():
    return [
        dbc.Col(
            create_button("open-confirm-save-modal-button", "Save Actions", width="180px"),
            xs="auto"
        ),
        dbc.Col(
            create_button("add-stock-action-button", "Add a Action", width="180px"),
            xs="auto"
        )
    ]



def build_cash_flow_table(df: pd.DataFrame):
    if df.empty:
        df = pd.DataFrame({
            'Note': [''],
            'Category': ['Investment'],
            'Currency': ['ILS'],
            'Amount': [0.0],
            'Amount in USD': [0.0],
            'Type': ['Deposit'],
            'Date': [datetime.today().strftime('%Y-%m-%d')],
            'Executed': [False],
        })
    df["Amount"] = df["Amount"].astype("float")
    df["Amount in USD"] = df["Amount in USD"].astype("float")

    columns = [
        {'name': 'Note', 'id': 'Note', 'editable': True},
        {'name': 'Category', 'id': 'Category', 'editable': True, 'presentation': 'dropdown'},
        {'name': 'Currency', 'id': 'Currency', 'editable': True, 'presentation': 'dropdown'},
        {'name': 'Amount', 'id': 'Amount', 'type': 'numeric', 'editable': True},
        {'name': 'Amount in USD', 'id': 'Amount in USD', 'type': 'numeric', 'editable': False},
        {'name': 'Type', 'id': 'Type', 'editable': True, 'presentation': 'dropdown'},
        {'name': 'Date', 'id': 'Date', 'editable': True, 'presentation': 'dropdown'},
    ]

    dropdown = {
        'Date': {'options': generate_date_options(31)},
        'Type': {'options': [{'label': 'Deposit', 'value': 'Deposit'}, {'label': 'Withdrawal', 'value': 'Withdrawal'}]},
        'Currency': {'options': [{'label': 'USD', 'value': 'USD'}, {'label': 'ILS', 'value': 'ILS'}, {'label': 'EUR', 'value': 'EUR'}, {'label': 'GBP', 'value': 'GBP'}]},
        'Category': {'options': [{'label': cat, 'value': cat} for cat in [
            'Investment', 'Credit', 'Education', 'Housing',
            'Phone & Internet', 'Entertainment', 'Transportation',
            'Shopping', 'Food & Restaurants', 'Health', 'Other'
        ]]}
    }

    args = get_common_table_args(table_id='cash-flow-table', columns=columns, data=df.to_dict('records'), dropdown=dropdown, page_size=10)

    return dash_table.DataTable(**args)

def get_cash_flow_buttons_cols():
    return [
        dbc.Col(
            create_button("open-confirm-cash-flow-save-modal-button", "Save Table", width="200px"),
            xs="auto"
        ),
        dbc.Col(
            create_button("add-cash-flow-button", "Add a cash transaction", width="200x"),
            xs="auto"
        )
    ]

from layout.shared_components import get_common_table_args

def build_dividend_table(df: pd.DataFrame):
    if df.empty:
        df = pd.DataFrame({
            'Date': [],
            'Ticker': [],
            'Currency': [],
            'Amount (original currency)': [],
            'Amount in USD': [],
            'Net amount in USD': [],  
            'Note': []
        })

    columns = [
        {'name': 'Date', 'id': 'Date'},
        {'name': 'Ticker', 'id': 'Ticker'},
        {'name': 'Currency', 'id': 'Currency'},
        {'name': 'Amount (original currency)', 'id': 'Amount (original currency)', 'type': 'numeric'},
        {'name': 'Amount in USD', 'id': 'Amount in USD', 'type': 'numeric'},
        {'name': 'Net amount in USD', 'id': 'Net amount in USD', 'type': 'numeric'}, 
        {'name': 'Note', 'id': 'Note'},
    ]

    args = get_common_table_args(table_id='dividends-table', columns=columns, data=df.to_dict('records'), editable=False, row_deletable=False, page_size=10)

    return dash_table.DataTable(**args)


def build_currency_transfer_table(df):
    if df.empty:
        df = pd.DataFrame({
            'Date': [datetime.today().strftime('%Y-%m-%d')],
            'From Currency': ['USD'],
            'To Currency': ['ILS'],
            'Amount': [0.0],
            'Rate': [1.0],
            'Amount in To Currency': [0.0],
            'Conversion Fee': [0.0],
            'Net Amount Received': [0.0],
            'Note': [''],
            'Executed': [False]
        })

    # חישוב ערכים מחדש
    df['Amount in To Currency'] = df['Amount'] * df['Rate']
    df['Net Amount Received'] = df['Amount in To Currency'] - df['Conversion Fee']

    columns = [
        {'name': 'Date', 'id': 'Date', 'editable': True, 'presentation': 'dropdown'},
        {'name': 'From Currency', 'id': 'From Currency', 'editable': True, 'presentation': 'dropdown'},
        {'name': 'To Currency', 'id': 'To Currency', 'editable': True, 'presentation': 'dropdown'},
        {'name': 'Amount', 'id': 'Amount', 'type': 'numeric', 'editable': True},
        {'name': 'Rate', 'id': 'Rate', 'type': 'numeric', 'editable': True},
        {'name': 'Amount in To Currency', 'id': 'Amount in To Currency', 'type': 'numeric', 'editable': False},
        {'name': 'Conversion Fee', 'id': 'Conversion Fee', 'type': 'numeric', 'editable': True},
        {'name': 'Net Amount Received', 'id': 'Net Amount Received', 'type': 'numeric', 'editable': False},
        {'name': 'Note', 'id': 'Note', 'editable': True},
    ]

    dropdown = {
        'Date': {'options': generate_date_options(31)},
        'From Currency': {'options': [{'label': 'USD', 'value': 'USD'}, {'label': 'ILS', 'value': 'ILS'}, {'label': 'EUR', 'value': 'EUR'}, {'label': 'GBP', 'value': 'GBP'}]},
        'To Currency': {'options': [{'label': 'USD', 'value': 'USD'}, {'label': 'ILS', 'value': 'ILS'}, {'label': 'EUR', 'value': 'EUR'}, {'label': 'GBP', 'value': 'GBP'}]},
    }

    args = get_common_table_args(
        table_id='currency-transfer-table',
        columns=columns,
        data=df.to_dict('records'),
        dropdown=dropdown,
        page_size=6
    )

    return dash_table.DataTable(**args)

def get_currency_transfer_buttons_cols():
    return [
        dbc.Col(
            create_button("open-confirm-currency-transfer-save-modal-button", "Save Table", width="220px"),
            xs="auto"
        ),
        dbc.Col(
            create_button("add-currency-transfer-button", "Add Currency Transfer", width="220px"),
            xs="auto"
        )
    ]


def get_download_buttons_cols():
    return [
        dbc.Col([
            create_button("download-stock-market-actions-csv-button", "Download Stock Actions", width="200px"),
            dcc.Download(id="download-stock-market-actions-csv")
        ], xs=12, sm="auto"),

        dbc.Col([
            create_button("download-cash-flow-csv-button", "Download Cash Flow", width="200px"),
            dcc.Download(id="download-cash-flow-csv")
        ], xs=12, sm="auto"),
    
        dbc.Col([
            create_button("download-dividends-csv-button", "Download Dividends", width="200px"),
            dcc.Download(id="download-dividends-csv")
        ], xs=12, sm="auto"),

        dbc.Col([
            create_button("download-currency-transfers-csv-button", "Download Currency Transfers", width="200px"),
            dcc.Download(id="download-currency-transfers-csv")
        ], xs=12, sm="auto")
    ]