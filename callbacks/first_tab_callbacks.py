from dash import Input, Output, State, callback_context
import dash.exceptions
import pandas as pd
from utils.main_data_update import get_updated_data, UpdatedDataDict
import plotly.graph_objs as go
from plotly.graph_objs import Figure
import numpy as np
from datetime import datetime
from data.data_manager import DataManager

data_manager = DataManager()


EMPTY_PORTFOLIO_CALLBACK_OUTPUT = (
    "",            # Toast message
    "",            # Toast header
    "",            # Toast icon
    False,         # Toast open
    Figure(),      # total-allocation-pie-chart
    Figure(),      # weight-pie-chart
    Figure(),      # sector-weight-pie-chart
    [],            # portfolio-store data
    [],            # cash-store data
    [],            # gold-store data
    Figure(),      # weight-pie-chart-analysis (Tab 3)
    Figure(),      # sector-weight-pie-chart-analysis (Tab 3)
    Figure(),      # sub-sector-weight-pie-chart-analysis (Tab 3)
    Figure(),      # currency-weight-pie-chart-analysis
    Figure(),      # stock-weight-excl-etfs-chart-analysis (Tab 3)

)

start_date = f"{datetime.today().year}-01-01"
end_date = datetime.today().strftime('%Y-%m-%d')

def register_first_tab_callbacks(app):

    @app.callback(
        [
            Output('update-save-toast', 'children'),
            Output('update-save-toast', 'header'),
            Output('update-save-toast', 'icon'),
            Output('update-save-toast', 'is_open'),
            Output('total-allocation-pie-chart', 'figure'),
            Output('weight-pie-chart', 'figure'),
            Output('sector-weight-pie-chart', 'figure'),
            Output('portfolio-store', 'data'),
            Output('cash-store', 'data'),
            Output('gold-store', 'data'),
            Output('weight-pie-chart-analysis', 'figure'),  #Tab 3
            Output('sector-weight-pie-chart-analysis', 'figure'),   #Tab 3
            Output('sub-sector-weight-pie-chart-analysis', 'figure'),   #Tab 3
            Output('currency-weight-pie-chart-analysis', 'figure'), #Tab 3
            Output('stock-weight-excl-etfs-chart-analysis', 'figure'),  # Tab 3

         ],
        Input('update-save-button', 'n_clicks'),
        State('gold-table', 'data'),
        prevent_initial_call=False
    )
    def update_table(_update_clicks, gold_data):
        try:
            data: UpdatedDataDict = get_updated_data(data_manager, gold_data)
            charts = data["charts"]


            return (
                "Prices updated & saved successfully! ✅", "Success", "success", True,
                charts.create_total_allocation_pie_chart(),
                charts.create_stock_weight_pie_chart(),
                charts.create_sector_weight_pie_chart(),
                data["portfolio"].to_dict("records"),
                data["cash"].to_dict("records"),
                data["gold"].to_dict("records"),
                charts.create_stock_weight_pie_chart(), #Tab 3
                charts.create_sector_weight_pie_chart(), #Tab 3
                charts.create_sub_sector_weight_pie_chart(), #Tab 3
                charts.create_currency_weight_pie_chart(),  #Tab 3
                charts.create_stock_weight_excluding_index_etfs_chart()  # Tab 3
            )

        except Exception as e:
            return (
                f"Error updating prices & saving: {str(e)} ❌", "Error", "danger", True,
                *EMPTY_PORTFOLIO_CALLBACK_OUTPUT[4:]
            )

    @app.callback(
        Output('stock-dropdown', 'options'),
        Input('portfolio-store', 'data'),
        prevent_initial_call=True
    )
    def update_dropdown(data):
        tickers = [row['Ticker'] for row in data if row['Ticker']]
        return [{'label': x, 'value': x} for x in set(tickers)]

    @app.callback(
        [Output('stock-chart-figure', 'figure'),
         Output('error-toast', 'children'),
         Output('error-toast', 'is_open')],
        [Input('stock-dropdown', 'value'),
         Input('stock-chart-type', 'value')]
    )
    def update_graph(stock_slctd, chart_type):
        try:
            from utils.finance_utils import get_stock_candles
            stock_slctd_df = get_stock_candles(stock_slctd)
            if stock_slctd_df.empty or stock_slctd_df is None:
                return go.Figure(), f"No available info for {stock_slctd}", True

            trading_days = np.array(stock_slctd_df['Date'])
            all_days = np.array(pd.date_range(start=start_date, end=end_date).date)
            non_trading_days = np.setdiff1d(all_days, trading_days)

            if chart_type == 'line':
                figure = go.Figure(data=[go.Scatter(
                    x=stock_slctd_df['Date'],
                    y=stock_slctd_df['Close'],
                    mode='lines',
                    name=stock_slctd,
                    line=dict(color='blue')
                )])
            elif chart_type == 'candlestick':
                figure = go.Figure(data=[go.Candlestick(
                    x=stock_slctd_df['Date'],
                    open=stock_slctd_df['Open'],
                    high=stock_slctd_df['High'],
                    low=stock_slctd_df['Low'],
                    close=stock_slctd_df['Close'],
                    name=stock_slctd
                )])

            figure.update_layout(
                title=f'{stock_slctd} Price History YTD',
                xaxis_title='Date',
                yaxis_title='Price ($)',
                template='plotly_dark',
                xaxis=dict(
                    type='date',
                    tickmode='auto',
                    tickangle=-45,
                    rangebreaks=[dict(values=non_trading_days)]
                )
            )
            return figure, "", False

        except Exception as e:
            return go.Figure(), f"Error loading {stock_slctd}: {str(e)}", True
