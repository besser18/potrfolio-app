from dash import html, dcc
import dash_bootstrap_components as dbc
from layout.overview_layout.overview_components import (
    build_portfolio_table,
    build_cash_table,
    build_gold_table,
    build_total_allocation_chart,
    build_weight_pie_chart,
    build_sector_weight_pie_chart,
    build_stock_dropdown,
    build_chart_type_dropdown,
    get_download_buttons_cols,
    get_portfolio_action_buttons_cols,
    build_toasts,
)

def build_overview_tab(portfolio_data, cash_data, gold_data):
    error_toast, update_save_toast, update_save_cash_gold_toast = build_toasts()
    stock_list = portfolio_data['Ticker'].tolist()
    default_stock = 'VOO' if 'VOO' in stock_list else (stock_list[0] if stock_list else None)
    return dbc.Container([
        html.Div([
        error_toast,
        update_save_toast,
        update_save_cash_gold_toast,
        ]),

        dbc.Row([
            dbc.Col(html.H1("Stock Market Portfolio", className='text-center text-info font-weight-bolder'), width=12)
        ]),

        dbc.Row([
            dbc.Col(build_portfolio_table(portfolio_data), xl=10, lg=10, md=12, sm=12, xs=12)
        ], justify='center'),

        dbc.Row(get_portfolio_action_buttons_cols(), className="d-flex justify-content-end gap-2 mt-2"),

        html.Hr(),

        dbc.Row([
            dbc.Col(html.H2("Cash & Gold Management", className='text-center text-info font-weight-bolder'))
        ]),
        dbc.Row([
            dbc.Col(build_cash_table(cash_data), xl=6, lg=6, md=12, sm=12, xs=12),
            dbc.Col(build_gold_table(gold_data), xl=6, lg=6, md=12, sm=12, xs=12)
        ], justify='center'),

        html.Hr(),

        dbc.Row([
            dbc.Col(build_total_allocation_chart(), xl=6, lg=6, md=8, sm=12, xs=12)
        ], justify='center'),

        html.Br(),

        dbc.Row([
            dbc.Col(build_stock_dropdown(stock_list, default_stock), width=5),
            dbc.Col(build_chart_type_dropdown(), width=5)
        ], justify='center'),

        dbc.Row([
            dbc.Col(dcc.Loading(
                id="loading-chart",
                type="default",
                children=dcc.Graph(id='stock-chart-figure', style={'height': '600px', 'width': '100%'}),
                style={'height': '600px'}
            ), xl=10, lg=10, md=12, sm=12, xs=12)
        ], justify='center'),

        html.Br(),

        dbc.Row([
            dbc.Col(build_weight_pie_chart(), xl=6, lg=6, md=6, sm=12, xs=12),
            dbc.Col(build_sector_weight_pie_chart(), xl=6, lg=6, md=6, sm=12, xs=12)
        ], justify='center'),

        html.Hr(),

        dbc.Row([
            dbc.Col(html.H3("Download files:"))
        ]),
        dbc.Row(get_download_buttons_cols(), justify="start", className="gap-2 mt-3")

    ], fluid=True, style={'padding': '20px'})