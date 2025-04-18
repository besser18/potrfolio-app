#from .data_sync_callbacks import register_data_sync_callbacks
from .render_table_callbacks import register_render_table_callbacks
from .first_tab_callbacks import register_first_tab_callbacks
from .second_tab_callbacks import register_second_tab_callbacks
from .download_callbacks import register_download_callbacks
from .third_tab_callbacks import register_third_tab_callbacks

def register_all_callbacks(app):
    #register_data_sync_callbacks(app)
    register_render_table_callbacks(app)
    register_first_tab_callbacks(app)
    register_second_tab_callbacks(app)
    register_download_callbacks(app)
    register_third_tab_callbacks(app)
