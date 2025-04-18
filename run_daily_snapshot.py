from data.data_manager import DataManager
from external_data.currency_manager import CurrencyManager
from services.daily.daily_snapshot_builder import DailySnapshotBuilder

def run_snapshot(request=None):
    data_manager = DataManager()
    currency_manager = CurrencyManager()
    builder = DailySnapshotBuilder(data_manager, currency_manager)
    builder.build_snapshot()
    print("✅ Snapshot run completed.")
    return "OK"

if __name__ == "__main__":
    run_snapshot()