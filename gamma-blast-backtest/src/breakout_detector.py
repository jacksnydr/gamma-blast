
def detect_descending_breakout(straddle_df, lookback=15):
    straddle_df = straddle_df.copy()
    straddle_df["prev_highs"] = straddle_df["straddle_price"].rolling(window=lookback).max()
    straddle_df["breakout"] = straddle_df["straddle_price"] > straddle_df["prev_highs"]

    breakout_points = straddle_df[straddle_df["breakout"]]
    if not breakout_points.empty:
        breakout_time = breakout_points.iloc[0]["timestamp"]
        breakout_price = breakout_points.iloc[0]["straddle_price"]
        return breakout_time, breakout_price
    return None, None