import dash_bootstrap_components as dbc
from datetime import datetime, timedelta

TABLE_STYLE = {
    'height': '600px', 'overflowY': 'auto', 'overflowX': 'auto'
}

CELL_STYLE = { 
    'color': 'white', 'backgroundColor': '#222222', 'textAlign': 'center', 'fontSize': '14px', 'minWidth': '120px', 'width': '120px', 'maxWidth': '200px',
}

HEADER_STYLE = {
    'backgroundColor': '#444444', 'fontWeight': 'bold', 'color': 'white', 'textAlign': 'center', 'fontSize': '16px'
}
def create_toast(toast_id, header="", message="", icon="info", duration=4000, is_open=False, top=20):
    return dbc.Toast(
        message,
        id=toast_id,
        header=header,
        is_open=is_open,
        duration=duration,
        icon=icon,
        dismissable=True,
        style={
            "position": "fixed",
            "top": f"{top}px",
            "right": "50px",
            "width": "250px",
            "zIndex": 1000
        }
    )

def create_button(button_id, label, color="secondary", size="lg", width=None, custom_style=None, disabled=False):
    button_style = {}
    if width:
        button_style['width'] = width
    if custom_style:
        button_style.update(custom_style)

    return dbc.Button(
        label,
        id=button_id,
        color=color,
        size=size,
        style=button_style,
        disabled=disabled
    )


def create_confirm_save_modal(modal_id, confirm_button_id, cancel_button_id, header_text="Confirm Save", body_text="Are you sure you want to save these changes? This action cannot be undone."):
    return dbc.Modal([
        dbc.ModalHeader(header_text),
        dbc.ModalBody(body_text),
        dbc.ModalFooter([
            dbc.Button("Cancel", id=cancel_button_id, color="secondary", className="ms-auto"),
            dbc.Button("Yes, Save", id=confirm_button_id, color="primary", className="ms-2")
        ])
    ], id=modal_id, is_open=False)

def generate_date_options(days_back: int = 31):
    return [
        {'label': (datetime.today() - timedelta(days=i)).strftime('%Y-%m-%d'),
         'value': (datetime.today() - timedelta(days=i)).strftime('%Y-%m-%d')}
        for i in range(days_back)
    ]

def generate_future_date_options(days_ahead: int = 31):
    return [
        {'label': (datetime.today() + timedelta(days=i)).strftime('%Y-%m-%d'),
         'value': (datetime.today() + timedelta(days=i)).strftime('%Y-%m-%d')}
        for i in range(days_ahead)
    ]

def get_common_table_args(table_id, columns, data, dropdown=None, editable=True, row_deletable=True, page_size=10):
    return {
        'id': table_id,
        'columns': columns,
        'data': data,
        'editable': editable,
        'filter_action': "native",
        'sort_action': "native",
        'row_deletable': row_deletable,
        'page_current': 0,
        'page_size': page_size,
        'style_table': TABLE_STYLE,
        'style_cell': CELL_STYLE,
        'style_header': HEADER_STYLE,
        'dropdown': dropdown or {}
    }