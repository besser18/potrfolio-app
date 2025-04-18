import plotly.graph_objs as go
import pandas as pd

class PortfolioCharts:
    def __init__(self, portfolio_df: pd.DataFrame, cash_df: pd.DataFrame, gold_df: pd.DataFrame):
        self.portfolio_df = portfolio_df.copy()
        self.cash_df = cash_df.copy()
        self.gold_df = gold_df.copy()

    def create_total_allocation_pie_chart(self):
        stock_value = self.portfolio_df['Current Value in $'].sum()
        cash_value = self.cash_df['Value in USD'].sum()
        gold_value = self.gold_df['Value'].sum()
        total_value = round(stock_value + cash_value + gold_value)

        labels = ['Stocks', 'Cash', 'Gold']
        values = pd.Series([stock_value, cash_value, gold_value], index=labels).sort_values(ascending=False)
        colors = ['#D32F2F', 'green', 'gold']

        figure = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hoverinfo='label+percent+value',
            textinfo='label+percent',
            marker=dict(colors=colors),
            hole=0.3
        )])

        figure.update_layout(
            annotations=[
                dict(
                    text=f"<b>Total: ${total_value:,.2f}</b>",
                    x=0.9, y=0.9,
                    font_size=18,
                    showarrow=False,
                    font=dict(color="white")
                )
            ],
            title="Total Portfolio Allocation",
            template="plotly_dark",
            showlegend=True,
            legend=dict(x=1, y=1),
            margin=dict(l=50, r=50, t=50, b=50)
        )
        return figure

    def create_stock_weight_pie_chart(self):
        df = self.portfolio_df.sort_values(by='Weight (%)', ascending=False)
        figure = go.Figure(data=[go.Pie(
            labels=df['Ticker'],
            values=df['Weight (%)'],
            hoverinfo='label+percent',
            textinfo='label+percent',
            hole=0.3
        )])
        figure.update_layout(
            title="Portfolio Allocation",
            template="plotly_dark",
            showlegend=True,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        return figure

    def create_sector_weight_pie_chart(self):
        sector_weights = self.portfolio_df.groupby('Sector')['Weight (%)'].sum().reset_index()
        sector_weights = sector_weights[sector_weights['Weight (%)'] > 0]
        sector_weights = sector_weights.sort_values(by='Weight (%)', ascending=False)

        figure = go.Figure(data=[go.Pie(
            labels=sector_weights['Sector'],
            values=sector_weights['Weight (%)'],
            hoverinfo='label+percent',
            textinfo='label+percent',
            hole=0.3
        )])

        figure.update_layout(
            title="Portfolio Allocation by Sector (Weight %)",
            template="plotly_dark",
            showlegend=True,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        return figure


    def create_sub_sector_weight_pie_chart(self):
        sub_sector_weights = self.portfolio_df.groupby('Sub Sector')['Weight (%)'].sum().reset_index()
        sub_sector_weights = sub_sector_weights[sub_sector_weights['Weight (%)'] > 0]
        sub_sector_weights = sub_sector_weights.sort_values(by='Weight (%)', ascending=False)

        figure = go.Figure(data=[go.Pie(
            labels=sub_sector_weights['Sub Sector'],
            values=sub_sector_weights['Weight (%)'],
            hoverinfo='label+percent',
            textinfo='label+percent',
            hole=0.3
        )])

        figure.update_layout(
            title="Portfolio Allocation by Sub Sector (Weight %)",
            template="plotly_dark",
            showlegend=True,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        return figure

    def create_currency_weight_pie_chart(self):
        currency_weights = self.portfolio_df.groupby('Currency')['Weight (%)'].sum().reset_index()
        currency_weights = currency_weights[currency_weights['Weight (%)'] > 0]
        currency_weights = currency_weights.sort_values(by='Weight (%)', ascending=False)

        figure = go.Figure(data=[go.Pie(
            labels=currency_weights['Currency'],
            values=currency_weights['Weight (%)'],
            hoverinfo='label+percent',
            textinfo='label+percent',
            hole=0.3
        )])

        figure.update_layout(
            title="Portfolio Allocation by Currency (Weight %)",
            template="plotly_dark",
            showlegend=True,
            margin=dict(l=50, r=50, t=50, b=50)
        )

        return figure
        
    def create_stock_weight_excluding_index_etfs_chart(self) -> go.Figure:
        exclude_tickers = {"QQQ", "VOO", "IBIT", "MSTY"}

        filtered_df = self.portfolio_df[
            ~self.portfolio_df["Ticker"].isin(exclude_tickers)
        ]

        filtered_df = filtered_df[filtered_df['Weight (%)'] > 0]

        filtered_df = filtered_df.sort_values(by='Weight (%)', ascending=False)

        figure = go.Figure(data=[go.Pie(
            labels=filtered_df["Ticker"],
            values=filtered_df["Weight (%)"],
            hoverinfo='label+percent',
            textinfo='label+percent',
            hole=0.3
        )])

        figure.update_layout(
            title="Portfolio Allocation (Excluding Index ETFs)",
            template="plotly_dark",
            showlegend=True,
            margin=dict(l=50, r=50, t=50, b=50)
        )

        return figure

    
    @staticmethod
    def empty_figure(message: str = "Waiting for data...") -> go.Figure:
        return go.Figure(
            layout=go.Layout(
                title={
                    'text': message,
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 20}
                },
                template='plotly_dark',
                margin=dict(l=50, r=50, t=50, b=50),
            )
        )


