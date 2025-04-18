# layout/analysis_layout/stock_analysis_tab.py

from dash import html
import dash_bootstrap_components as dbc
from layout.stock_analysis_layout.stock_analysis_components import (
    build_stock_holding_analysis_table,
    build_future_dividends_table,
    get_future_dividends_buttons_cols,
    get_stock_holding_buttons_cols,
    build_toasts,
    get_download_buttons_cols,
    build_sector_weight_pie_chart_analysis,
    build_weight_pie_chart_analysis,
    build_sub_sector_weight_pie_chart_analysis,
    build_currency_weight_pie_chart_analysis,
    build_stock_weight_excl_index_etfs_chart_analysis,
)

future_dividends_toast, save_stock_holding_toast = build_toasts()

def build_stock_analysis_tab(portfolio_data, future_dividends_data):
    return dbc.Container([
        html.Div([
            future_dividends_toast,
            save_stock_holding_toast
        ]),
        dbc.Row([
            dbc.Col(html.H2("Stock Holdings Analysis", className='text-center text-info'), width=12)
        ]),

        dbc.Row([
            dbc.Col(build_stock_holding_analysis_table(portfolio_data), xl=10, lg=10, md=12, sm=12, xs=12)
        ], justify='center'),

        dbc.Row(get_stock_holding_buttons_cols(), className="d-flex justify-content-end gap-2 mt-2"),

        html.Hr(),
        
        dbc.Row([
            dbc.Col(html.H2("Future Dividents", className='text-center text-info'), width=12)
        ]),

        dbc.Row([
            dbc.Col(build_future_dividends_table(future_dividends_data), xl=10, lg=10, md=12, sm=12, xs=12)
        ], justify='center'),

        dbc.Row(get_future_dividends_buttons_cols(), className="d-flex justify-content-end gap-2 mt-2"),

        html.Hr(),

        dbc.Row([
            dbc.Col(html.H3("Portfolio Charts Analysis", className='text-center text-info'))
        ]),

        html.Hr(),

        dbc.Row([
            dbc.Col(build_weight_pie_chart_analysis(), xl=4, lg=6, md=12, sm=12, xs=12, style={"minWidth": "400px"}),
            dbc.Col(build_sector_weight_pie_chart_analysis(), xl=4, lg=6, md=12, sm=12, xs=12, style={"minWidth": "400px"}),
            dbc.Col(build_sub_sector_weight_pie_chart_analysis(), xl=4, lg=6, md=12, sm=12, xs=12, style={"minWidth": "400px"})
        ], justify='center'),

        html.Br(),

        dbc.Row([
            dbc.Col(build_currency_weight_pie_chart_analysis(), xl=4, lg=6, md=12, sm=12, xs=12, style={"minWidth": "400px"}),
            dbc.Col(build_stock_weight_excl_index_etfs_chart_analysis(), xl=4, lg=6, md=12, sm=12, xs=12, style={"minWidth": "400px"})
        ], justify='center'),


        html.Hr(),

        dbc.Row([
            dbc.Col(html.H3("Download files:"))
        ]),
        dbc.Row(get_download_buttons_cols(), justify="start", className="gap-2 mt-3")


    ], fluid=True, style={"padding": "10px"})

