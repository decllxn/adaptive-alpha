def liquidity_sweep(df):
    df["prev_high"] = df["high"].shift(1)
    df["prev_low"] = df["low"].shift(1)

    # sweep high then close below → bearish
    df["sweep_high"] = (df["high"] > df["prev_high"]) & (df["close"] < df["prev_high"])

    # sweep low then close above → bullish
    df["sweep_low"] = (df["low"] < df["prev_low"]) & (df["close"] > df["prev_low"])

    return df

def fair_value_gaps(df):
    # FVG definition (3-candle imbalance)

    df["fvg_bullish"] = (
        (df["low"].shift(1) > df["high"].shift(2))  # gap up
    )

    df["fvg_bearish"] = (
        (df["high"].shift(1) < df["low"].shift(2))  # gap down
    )

    # Inverse FVG (failed gap continuation)
    df["ifvg_bullish"] = (
        df["fvg_bearish"] & (df["close"] > df["high"].shift(1))
    )

    df["ifvg_bearish"] = (
        df["fvg_bullish"] & (df["close"] < df["low"].shift(1))
    )

    return df