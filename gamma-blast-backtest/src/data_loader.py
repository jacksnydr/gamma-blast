
import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
BASE_URL = "https://api.polygon.io"

def get_intraday_data(ticker, date):
    url = f"{BASE_URL}/v2/aggs/ticker/{ticker}/range/1/minute/{date}/{date}?adjusted=true&sort=asc&limit=10000&apiKey={POLYGON_API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    raw = response.json().get("results", [])
    if not raw:
        raise ValueError("No intraday data found.")
    
    df = pd.DataFrame(raw)
    df["timestamp"] = pd.to_datetime(df["t"], unit="ms")
    df = df.rename(columns={"o": "open", "h": "high", "l": "low", "c": "close", "v": "volume"})
    return df[["timestamp", "open", "high", "low", "close", "volume"]]

def get_options_chain(ticker):
    url = f"{BASE_URL}/v3/snapshot/options/{ticker}?apiKey={POLYGON_API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("results", [])

def find_atm_strike(options_chain, current_price, expiry_date):
    closest_call, closest_put = None, None
    min_diff = float("inf")

    for option in options_chain:
        details = option["details"]
        if details["expiration_date"] != expiry_date:
            continue

        strike = details["strike_price"]
        diff = abs(strike - current_price)
        if diff < min_diff:
            min_diff = diff
            if details["contract_type"] == "call":
                closest_call = details["ticker"]
            elif details["contract_type"] == "put":
                closest_put = details["ticker"]
    return closest_call, closest_put

def get_option_price_series(option_ticker):
    url = f"{BASE_URL}/v2/aggs/ticker/{option_ticker}/range/1/minute/2024-06-21/2024-06-21?adjusted=true&sort=asc&limit=10000&apiKey={POLYGON_API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    raw = response.json().get("results", [])
    df = pd.DataFrame(raw)
    df["timestamp"] = pd.to_datetime(df["t"], unit="ms")
    df = df.rename(columns={"c": "close"})
    return df[["timestamp", "close"]]

if __name__ == "__main__":
    date = "2024-06-21"
    ticker = "SPY"
    intraday_df = get_intraday_data(ticker, date)
    current_price = intraday_df[intraday_df["timestamp"].dt.time == datetime.strptime("14:30", "%H:%M").time()]["close"].values[0]

    options_chain = get_options_chain(ticker)
    expiry = date
    call_ticker, put_ticker = find_atm_strike(options_chain, current_price, expiry)

    call_series = get_option_price_series(call_ticker)
    put_series = get_option_price_series(put_ticker)

    print(f"ATM call: {call_ticker}, put: {put_ticker}")
