import pandas as pd


def compute_returns(df: pd.DataFrame):
    df["returns"] = df["close"].pct_change().fillna(0)
    return df


def compute_atr(df: pd.DataFrame, period: int = 14):
    high_low = df["high"] - df["low"]
    high_close = (df["high"] - df["close"].shift()).abs()
    low_close = (df["low"] - df["close"].shift()).abs()

    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df["atr"] = tr.rolling(period).mean()

    return df


def compute_moving_averages(df: pd.DataFrame):
    df["ma_fast"] = df["close"].rolling(20).mean()
    df["ma_slow"] = df["close"].rolling(50).mean()
    return df

def compute_regime(df):
    df["trend_strength"] = abs(df["ma_fast"] - df["ma_slow"]) / df["close"]

    # trending vs ranging
    df["is_trending"] = df["trend_strength"] > 0.003

    return df