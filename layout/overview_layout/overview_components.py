#overview_components
import dash_bootstrap_components as dbc
from dash import dcc, dash_table
from layout.shared_components import create_button, create_toast, get_common_table_args


def build_portfolio_table(df):
    # הסתרת העמודות Stop Loss ו-Exit Strategy מהתצוגה בלבד
    visible_columns = [col for col in df.columns if col not in ['Stop Loss', 'Exit Strategy']]

    columns = [{'name': col, 'id': col, 'editable': False} for col in visible_columns]

    args = get_common_table_args(
        table_id='portfolio-table',
        columns=columns,
        data=df.to_dict('records'),
        editable=True,
        row_deletable=False,
        page_size=10
    )

    return dash_table.DataTable(**args)

def get_portfolio_action_buttons_cols():
    return [
        dbc.Col(
            create_button("update-save-button", "Update & Save", width="180px"),
            xs="auto"
        ),
    ]


def build_total_allocation_chart():
    return dcc.Loading(
        id='loading-total-allocation-chart',
        type="default",
        children=dcc.Graph(id='total-allocation-pie-chart', style={'height': '600px', 'width': '100%'}),
        style={'height': '600px'}
    )

def build_cash_table(cash_data):
    columns = [
        {'name': 'Currency', 'id': 'Currency', 'editable': False},
        {'name': 'Balance', 'id': 'Balance', 'editable': False},
        {'name': 'Value in USD', 'id': 'Value in USD', 'editable': False}
    ]

    args = get_common_table_args(
        table_id='cash-table',
        columns=columns,
        data=cash_data.to_dict('records'),
        editable=False,
        row_deletable=False,
        page_size=5 
    )

    return dash_table.DataTable(**args)

def build_gold_table(gold_data):
    columns = [
        {'name': 'Type', 'id': 'Type', 'editable': False},
        {'name': 'Amount', 'id': 'Amount', 'editable': True},
        {'name': 'Value', 'id': 'Value', 'editable': False}
    ]

    args = get_common_table_args(
        table_id='gold-table',
        columns=columns,
        data=gold_data.to_dict('records'),
        editable=True,
        row_deletable=False,
        page_size=5
    )

    return dash_table.DataTable(**args)

def build_stock_dropdown(stock_list, default_stock):
    return dcc.Dropdown(
        id='stock-dropdown',
        options=[{'label': x, 'value': x} for x in stock_list],
        value=default_stock,
        clearable=False
    )

def build_chart_type_dropdown():
    return dcc.Dropdown(
        id='stock-chart-type',
        options=[
            {'label': 'Line Chart', 'value': 'line'},
            {'label': 'Candlestick Chart', 'value': 'candlestick'}
        ],
        value='line',
        clearable=False
    )


def build_weight_pie_chart():
    return dcc.Loading(
        id="loading-pie-chart",
        type="default",
        children=dcc.Graph(id='weight-pie-chart', style={'height': '600px', 'width': '100%'}),
        style={'height': '600px'}
    )

def build_sector_weight_pie_chart():
    return dcc.Loading(
        id="loading-pie-sector-weight-chart",
        type="default",
        children=dcc.Graph(id='sector-weight-pie-chart', style={'height': '600px', 'width': '100%'}),
        style={'height': '600px'}
    )


def get_download_buttons_cols():
    return [
        dbc.Col([
            create_button("download-portfolio-cvs-button", "Download Portfolio", width="200px"),
            dcc.Download(id="download-portfolio-csv")
        ], xs=12, sm="auto"),

        dbc.Col([
            create_button("download-cash-cvs-button", "Download Cash Holdings", width="200px"),
            dcc.Download(id="download-cash-csv")
        ], xs=12, sm="auto"),

        dbc.Col([
            create_button("download-gold-cvs-button", "Download Gold Holdings", width="200px"),
            dcc.Download(id="download-gold-csv")
        ], xs=12, sm="auto")
    ]


def build_toasts():
    return [
        create_toast("error-toast", "Error ⚠️", "Something went wrong!", "danger", top=20),
        create_toast("update-save-toast", "Update Successful ✅", "Saved successfully!", "success", top=100),
        create_toast("update-save-cash-gold-toast", "Cash & Gold Updated ✅", "Updated successfully!", "success", top=180)
    ]