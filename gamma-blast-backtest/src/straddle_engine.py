import pandas as pd

def build_straddle_series(call_df, put_df):
    # Merge on timestamp
    merged = pd.merge(call_df, put_df, on="timestamp", suffixes=("_call", "_put"))
    merged["straddle_price"] = merged["close_call"] + merged["close_put"]
    return merged[["timestamp", "straddle_price"]]