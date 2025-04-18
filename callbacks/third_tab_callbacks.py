
from dash import Input, Output, State, ctx, callback, callback_context
import pandas as pd
from dash.exceptions import PreventUpdate
from data.data_manager import DataManager
import numpy as np
from external_data.currency_manager import CurrencyManager
from services.tables.future_dividends_table import FutureDividendsTable
from utils.graph_utils import PortfolioCharts
from plotly.graph_objs import Figure

DEFAULT_FORMATTERS = {
    'Sector': lambda val: 'Unknown' if pd.isna(val) or str(val).strip() == '' else str(val),
    'Sub Sector': lambda val: 'Unknown' if pd.isna(val) or str(val).strip() == '' else str(val),
    'Stop Loss': lambda val: '' if pd.isna(val) or str(val).strip() == '' else str(val),
    'Exit Strategy': lambda val: '' if pd.isna(val) or str(val).strip() == '' else str(val)
}

currency_manager = CurrencyManager()
data_manager = DataManager()
def register_third_tab_callbacks(app):

    @app.callback(
        [Output("future-dividends-table", "data"),
        Output("future-dividend-save-or-add-row-toast", "children"),
        Output("future-dividend-save-or-add-row-toast", 'header'),
        Output("future-dividend-save-or-add-row-toast", 'icon'),
        Output("future-dividend-save-or-add-row-toast", 'is_open')],
        [Input("save-future-dividends-button", "n_clicks"),
        Input("add-future-dividend-button", "n_clicks")],
        State("future-dividends-table", "data"),
        prevent_initial_call=False#רוצה שזה יתעדכן באופן תדיר
    )
    def update_currency_transfer(_update_clicks, _add_clicks, existing_data):
        ctx = callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

        try:
            if not existing_data:
                if triggered_id == 'save-future-dividends-button':
                    return [], "No data to update or save", "Warning", "warning", True
                elif triggered_id == 'add-future-dividend-button':
                    existing_data = []

            table = FutureDividendsTable(data_manager, pd.DataFrame(existing_data))

            if triggered_id == 'save-future-dividends-button':
                if not table.validate_required_fields():
                    return existing_data, "❌ Please fill all required fields before saving.", "Missing Data", "danger", True

                table.calculate_expected_total(currency_manager)
                table.save()
                return table.to_dict(), "✅ Future Dividend table saved successfully!", "Success", "success", True

            elif triggered_id == 'add-future-dividend-button':
                table.add_empty_row()
                return table.to_dict(), "✅ Row added! Press save to commit", "Success", "success", True
            else:
                table.calculate_expected_total(currency_manager)
                table.save()
                return table.to_dict(), "", "", "info", False
        except ValueError as ve:
            return existing_data, f"{str(ve)} ❌", "Error", "danger", True
        except Exception as e:
            return existing_data, f"Error adding or updating row: {str(e)} ❌", "Error", "danger", True
        
    @app.callback(
        [Output("stock-holding-save-toast", "children"),
        Output("stock-holding-save-toast", 'header'),
        Output("stock-holding-save-toast", 'icon'),
        Output("stock-holding-save-toast", 'is_open')],
        Input("save-stock-holding-button", "n_clicks"),
        State("stock-holding-table", "data"),
        prevent_initial_call=True
    )
    def update_stock_holding_table(_save_clicks, existing_data):
        try:
            if not existing_data:
                return "No data to save", "Warning", "warning", True
            portfolio_df = data_manager.load_data("portfolio")
            updated_df = pd.DataFrame(existing_data)

            editable_columns = list(DEFAULT_FORMATTERS.keys())
            changed_rows = []

            for _, row in updated_df.iterrows():
                ticker = row['Ticker']
                original_row = portfolio_df.loc[portfolio_df['Ticker'] == ticker]

                for col in editable_columns:
                    orig_val_raw = original_row[col].values[0]
                    new_val_raw = row[col]

                    formatter = DEFAULT_FORMATTERS[col]
                    orig_val = formatter(orig_val_raw)
                    new_val = formatter(new_val_raw)

                    if orig_val == new_val:
                        continue

                    portfolio_df.loc[portfolio_df['Ticker'] == ticker, col] = new_val
                    changed_rows.append(ticker)
                        
            if not changed_rows:
                return "No changes detected", "No Update", "info", True

            data_manager.save_data(portfolio_df, "portfolio")
            return (
                f"✅ Updated tickers: {', '.join(set(changed_rows))}\n"
                "Please press the 'Save & Update' button on the Overview tab to save and apply the changes.",
                "Success",
                "success",
                True
            )
        except Exception as e:
            return f"❌ Error: {str(e)}", "Error", "danger", True