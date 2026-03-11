

# def get_data(ticker, startdate, enddate, interval="1d"):
#     import yfinance as yf
    
#     df = yf.Ticker(ticker).history(start=startdate, end=enddate, interval=interval)
#     df["Ticker"] = ticker

def get_history(ticker, period_start, period_end, granularity="1d"):
    import yfinance
    df = yfinance.Ticker(ticker).history(
        start=period_start,
        end=period_end,
        interval=granularity,
        auto_adjust=True
    ).reset_index()
    df = df.rename(columns={
        "Date": "datetime", 
        "Open": "open", 
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    })
    df = df.drop(columns=["Dividends", "Stock Splits"])
    # input(df)
    return df

from datetime import datetime

import pytz

period_start = datetime(2010, 1, 1, tzinfo=pytz.utc)   
period_end = datetime(2025, 12, 31, tzinfo=pytz.utc)

ticker = "AAPL"

df = get_history(ticker, period_start, period_end)

df["rolling30avg"] = df["close"].rolling(30).mean()
df["rolling30min"] = df["close"].rolling(30).min()
df["rolling30max"] = df["close"].rolling(30).max()

df["ticker"] = ticker

df = df.dropna()

from sqlalchemy import create_engine, text
engine = create_engine("sqlite:///databases/ticker_data.db")

with engine.begin() as connection:
    df.to_sql(name="LoadedData", con=connection, if_exists="append", index=False)

with engine.connect() as conn:
    conn.execute(text("SELECT * FROM LoadedData")).fetchall()