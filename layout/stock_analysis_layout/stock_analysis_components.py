from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

from layout.shared_components import get_common_table_args, create_button, create_toast, generate_future_date_options

def build_toasts():
    return [create_toast("future-dividend-save-or-add-row-toast", top=20),
            create_toast("stock-holding-save-toast", top=100)]

def build_stock_holding_analysis_table(df):
    editable_cols = ['Sector', 'Stop Loss', 'Exit Strategy', 'Sub Sector']

    columns = [
        {'name': col, 'id': col, 'editable': col in editable_cols}
        for col in df.columns
    ]

    args = get_common_table_args(
        table_id='stock-holding-table',
        columns=columns,
        data=df.to_dict('records'),
        editable=True,
        row_deletable=False,
        page_size=6
    )

    return dash_table.DataTable(**args)

def build_future_dividends_table(df):
    # אם הנתונים ריקים, טוענים אותם עם ערכים ברירת מחדל
    if df.empty:
        df = pd.DataFrame({
            'Ex-Date': [''],
            'Payment Date': [''],
            'Ticker': [''],
            'Currency': ['USD'],
            'Amount per Share (Local Currency)': [0.0],
            'Shares Held': [0.0],
            'Amount per Share (USD)': [0.0],
            'Expected Total (USD)': [0.0],
            'Expected Net (USD)': [0.0],
            'Note': [''],
        })

    # הגדרת העמודות לטבלה
    columns = [
        {'name': 'Ex-Date', 'id': 'Ex-Date', 'editable': True, 'presentation': 'dropdown'},  # דרופדאון לתאריך
        {'name': 'Payment Date', 'id': 'Payment Date', 'editable': True, 'presentation': 'dropdown'},  # דרופדאון לתאריך
        {'name': 'Ticker', 'id': 'Ticker', 'editable': True},
        {'name': 'Currency', 'id': 'Currency', 'editable': True, 'presentation': 'dropdown'},  # דרופדאון למטבע
        {'name': 'Amount per Share (Local Currency)', 'id': 'Amount per Share (Local Currency)', 'editable': True},
        {'name': 'Shares Held', 'id': 'Shares Held', 'editable': False},
        {'name': 'Amount per Share (USD)', 'id': 'Amount per Share (USD)', 'editable': True},
        {'name': 'Expected Total (USD)', 'id': 'Expected Total (USD)', 'editable': False},
        {'name': 'Expected Net (USD)', 'id': 'Expected Net (USD)', 'editable': False},
        {'name': 'Note', 'id': 'Note', 'editable': True},
    ]
    
    # יצירת אפשרויות תאריכים לעתיד
    future_date_options = generate_future_date_options(62)
    
    # הגדרת dropdowns למטבעות ולתאריכים
    dropdown = {
        'Currency': {
            'options': [
                {'label': 'USD', 'value': 'USD'},
                {'label': 'ILS', 'value': 'ILS'},
                {'label': 'EUR', 'value': 'EUR'},
                {'label': 'GBP', 'value': 'GBP'}
            ]
        },
        'Ex-Date': {
            'options': future_date_options
        },
        'Payment Date': {
            'options': future_date_options
        }
    }

    # הגדרת הארגומנטים השונים לטבלה
    args = get_common_table_args(
        table_id='future-dividends-table',
        columns=columns,
        data=df.to_dict('records'),
        editable=True,
        row_deletable=True,
        dropdown=dropdown,
        page_size=6
    )
    
    # מחזירים את הטבלה המוגדרת
    return dash_table.DataTable(**args)


def get_future_dividends_buttons_cols():
    return [
        dbc.Col(
            create_button("save-future-dividends-button", "Save Table", width="200px"),
            xs="auto"
        ),
        dbc.Col(
            create_button("add-future-dividend-button", "Add Future Dividend", width="200px"),
            xs="auto"
        )
    ]

def get_stock_holding_buttons_cols():
    return [
        dbc.Col(
            create_button("save-stock-holding-button", "Save Table", width="200px"),
            xs="auto"
        ),
    ]


def build_weight_pie_chart_analysis():
    return dcc.Loading(
        id="loading-pie-chart-analysis",
        type="default",
        children=dcc.Graph(
            id='weight-pie-chart-analysis',
            config={'displayModeBar': True, 'responsive': True},
            style={'height': '650px', 'width': '100%', 'margin': 'auto'}
        ),
        style={'height': '650px'}
    )

def build_sector_weight_pie_chart_analysis():
    return dcc.Loading(
        id="loading-sector-pie-chart-analysis",
        type="default",
        children=dcc.Graph(
            id='sector-weight-pie-chart-analysis',
            config={'displayModeBar': True, 'responsive': True},
            style={'height': '650px', 'width': '100%', 'margin': 'auto'}
        ),
        style={'height': '650px'}
    )

def build_sub_sector_weight_pie_chart_analysis():
    return dcc.Loading(
        id="loading-sub-sector-pie-chart-analysis",
        type="default",
        children=dcc.Graph(
            id='sub-sector-weight-pie-chart-analysis',
            config={'displayModeBar': True, 'responsive': True},
            style={'height': '650px', 'width': '100%', 'margin': 'auto'}
        ),
        style={'height': '650px'}
    )

def build_currency_weight_pie_chart_analysis():
    return dcc.Loading(
        id="loading-currency-pie-chart-analysis",
        type="default",
        children=dcc.Graph(
            id='currency-weight-pie-chart-analysis',
            config={'displayModeBar': True, 'responsive': True},
            style={'height': '650px', 'width': '100%', 'margin': 'auto'}
        ),
        style={'height': '650px'}
    )
    
def build_stock_weight_excl_index_etfs_chart_analysis():
    return dcc.Loading(
        id="loading-stock-weight-excl-etfs-chart-analysis",
        type="default",
        children=dcc.Graph(
            id='stock-weight-excl-etfs-chart-analysis',
            config={'displayModeBar': True, 'responsive': True},
            style={'height': '650px', 'width': '100%', 'margin': 'auto'}
        ),
        style={'height': '650px'}
    )


def get_download_buttons_cols():
    return [
        dbc.Col([
            create_button("download-stock-holdings-csv-button", "Download Portfolio", width="200px"),
            dcc.Download(id="download-stock-holdings-csv")
        ], xs=12, sm="auto"),

        dbc.Col([
            create_button("download-future-dividend-csv-button", "Download Future Dividend", width="200px"),
            dcc.Download(id="download-future-dividend-csv")
        ], xs=12, sm="auto"),
    ]


