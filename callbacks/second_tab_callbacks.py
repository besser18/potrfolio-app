#transactions_callbacks.py
from dash import Input, Output, State, ctx, callback, callback_context
import pandas as pd
from dash.exceptions import PreventUpdate
from data.data_manager import DataManager
import numpy as np
from external_data.currency_manager import CurrencyManager
from services.tables.actions_table import ActionsTable
from services.tables.cashflow_table import CashFlowTable
from services.tables.currency_transfer_table import CurrencyTransferTable
import traceback

currency_manager = CurrencyManager()
data_manager = DataManager()

def register_second_tab_callbacks(app):

    @app.callback(
        [Output("stock-market-action-table", "data"),
        Output("action-update-save-or-add-row-toast", "children"),
        Output("action-update-save-or-add-row-toast", 'header'),
        Output("action-update-save-or-add-row-toast", 'icon'),
        Output("action-update-save-or-add-row-toast", 'is_open')],
        [Input("confirm-save-modal-confirm-button", "n_clicks"),
         Input("add-stock-action-button", "n_clicks")],
        State("stock-market-action-table", "data"),
        prevent_initial_call=True
    )
    def add_transaction(_update_clicks, _add_clicks, existing_data):
        ctx = callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

        try:
            if not existing_data:
                if triggered_id == 'confirm-save-modal-confirm-button':
                    return [], "No data to update or save", "Warning", "warning", True
                elif triggered_id == 'add-stock-action-button':
                    existing_data = []
                else:
                    return [], "⚠️ Invalid trigger with no data", "Warning", "warning", True


            df = pd.DataFrame(existing_data)
            table = ActionsTable(data_manager, df)

            if triggered_id == 'confirm-save-modal-confirm-button':
                if not table.validate_required_fields():
                    return existing_data, "❌ Please fill all required fields before saving.", "Missing Data", "danger", True

                if not table.needs_calculation():
                    return existing_data, "No action taken ❌", "Info", "info", True

                try:
                    profile = data_manager.get_profile()
                    results, errors = table.process_actions(
                        stock_manager=profile.stock_manager,
                        cash_manager=profile.cash_manager,
                        capital_gains_table=profile.capital_gains_table
                    )

                    profile.save_all()
                    table.save()
                    message = f"✅ {len(results)} actions executed!"
                    return table.to_dict(), message, "Done", "success", True
                except Exception as e:
                    return existing_data, f"Error occurred while processing: {str(e)} ❌", "Error", "danger", True

            elif triggered_id == 'add-stock-action-button':
                table.add_empty_row()
                return table.to_dict(), "✅ Row added! Press save to commit", "Success", "success", True

        except Exception as e:
            return existing_data, f"Error occurred: {str(e)} ❌", "Error", "danger", True


        

    @app.callback(
        Output("confirm-save-modal", "is_open"),
        [Input("open-confirm-save-modal-button", "n_clicks"),
        Input("confirm-save-modal-cancel-button", "n_clicks"),
        Input("confirm-save-modal-confirm-button", "n_clicks")],
        [State("confirm-save-modal", "is_open")],
        prevent_initial_call=True
    )
    def toggle_confirm_save_modal(open_click, cancel_click, confirm_click, is_open):
        ctx = callback_context
        triggered_id = ctx.triggered_id
        if triggered_id in ["open-confirm-save-modal-button", "confirm-save-modal-cancel-button", "confirm-save-modal-confirm-button"]:
            return not is_open
        return is_open

    @app.callback(
        [Output("cash-flow-table", "data"),
        Output("cash-flow-update-save-or-add-row-toast", "children"),
        Output("cash-flow-update-save-or-add-row-toast", 'header'),
        Output("cash-flow-update-save-or-add-row-toast", 'icon'),
        Output("cash-flow-update-save-or-add-row-toast", 'is_open')],
        [Input("confirm-cash-flow-save-modal-confirm-button", "n_clicks"),
        Input("add-cash-flow-button", "n_clicks")],
        State("cash-flow-table", "data"),
        prevent_initial_call=True
    )
    def update_cash_flow(_update_clicks, _add_clicks, existing_data):
        ctx = callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

        try:
            if not existing_data:
                if triggered_id == 'confirm-cash-flow-save-modal-confirm-button':
                    return [], "No data to update or save", "Warning", "warning", True
                elif triggered_id == 'add-cash-flow-button':
                    existing_data = []

            table = CashFlowTable(data_manager, pd.DataFrame(existing_data))

            if triggered_id == 'confirm-cash-flow-save-modal-confirm-button':
                if not table.validate_required_fields():
                    return existing_data, "❌ Please fill all required fields before saving.", "Missing Data", "danger", True

                if not table.needs_calculation():
                    return existing_data, "No action taken ❌", "Info", "info", True
                
                profile = data_manager.get_profile()
                results = table.process_cash_flows(
                    cash_manager=profile.cash_manager,
                    currency_manager=profile.stock_manager.currency_manager
                )

                profile.save_all()

                return table.to_dict(), "✅ Cash Flow table saved successfully!", "Success", "success", True

            elif triggered_id == 'add-cash-flow-button':
                table.add_empty_row()
                return table.to_dict(), "✅ Row added! Press save to commit", "Success", "success", True

        except Exception as e:
            return existing_data, f"Error adding or updating row: {str(e)} ❌", "Error", "danger", True



    @app.callback(
        Output("confirm-cash-flow-save-modal", "is_open"),
        [Input("open-confirm-cash-flow-save-modal-button", "n_clicks"),
        Input("confirm-cash-flow-save-modal-cancel-button", "n_clicks"),
        Input("confirm-cash-flow-save-modal-confirm-button", "n_clicks")],
        [State("confirm-cash-flow-save-modal", "is_open")],
        prevent_initial_call=True
    )
    def toggle_cash_flow_confirm_save_modal(open_click, cancel_click, confirm_click, is_open):
        ctx = callback_context
        triggered_id = ctx.triggered_id
        if triggered_id in ["open-confirm-cash-flow-save-modal-button",
                            "confirm-cash-flow-save-modal-cancel-button",
                            "confirm-cash-flow-save-modal-confirm-button"]:
            return not is_open
        return is_open


    @app.callback(
        [Output("currency-transfer-table", "data"),
        Output("currency-transfer-update-save-or-add-row-toast", "children"),
        Output("currency-transfer-update-save-or-add-row-toast", 'header'),
        Output("currency-transfer-update-save-or-add-row-toast", 'icon'),
        Output("currency-transfer-update-save-or-add-row-toast", 'is_open')],
        [Input("confirm-currency-transfer-save-modal-confirm-button", "n_clicks"),
        Input("add-currency-transfer-button", "n_clicks")],
        State("currency-transfer-table", "data"),
        prevent_initial_call=True
    )
    def update_currency_transfer(_update_clicks, _add_clicks, existing_data):
        ctx = callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None

        try:
            if not existing_data:
                if triggered_id == 'confirm-currency-transfer-save-modal-confirm-button':
                    return [], "No data to update or save", "Warning", "warning", True
                elif triggered_id == 'add-currency-transfer-button':
                    existing_data = []

            table = CurrencyTransferTable(data_manager, pd.DataFrame(existing_data))

            if triggered_id == 'confirm-currency-transfer-save-modal-confirm-button':
                if not table.validate_required_fields():
                    return existing_data, "❌ Please fill all required fields before saving.", "Missing Data", "danger", True

                if not table.needs_calculation():
                    return existing_data, "No action taken ❌", "Info", "info", True

                profile = data_manager.get_profile()
                results = table.process_currency_transfers(
                    cash_manager=profile.cash_manager,
                    currency_manager=profile.stock_manager.currency_manager
                )
                profile.save_all()

                return table.to_dict(), f"✅ Currency Transfer table saved successfully!\n {results}", "Success", "success", True

            elif triggered_id == 'add-currency-transfer-button':
                table.add_empty_row()
                return table.to_dict(), "✅ Row added! Press save to commit", "Success", "success", True

        except ValueError as ve:
            return existing_data, f"{str(ve)} ❌", "Error", "danger", True
        except Exception as e:
            return existing_data, f"Error adding or updating row: {str(e)} ❌", "Error", "danger", True

        

    @app.callback(
        Output("confirm-currency-transfer-save-modal", "is_open"),
        [Input("open-confirm-currency-transfer-save-modal-button", "n_clicks"),
        Input("confirm-currency-transfer-save-modal-cancel-button", "n_clicks"),
        Input("confirm-currency-transfer-save-modal-confirm-button", "n_clicks")],
        [State("confirm-currency-transfer-save-modal", "is_open")],
        prevent_initial_call=True
    )
    def toggle_currency_transfer_confirm_save_modal(open_click, cancel_click, confirm_click, is_open):
        ctx = callback_context
        triggered_id = ctx.triggered_id
        if triggered_id in [
            "open-confirm-currency-transfer-save-modal-button",
            "confirm-currency-transfer-save-modal-cancel-button",
            "confirm-currency-transfer-save-modal-confirm-button"]:
            return not is_open
        return is_open