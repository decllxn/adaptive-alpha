class SignalEngine:
    def __init__(self):
        pass

    def generate(self, row):
        if row["atr"] == 0:
            return 0

        # -----------------------------
        # REGIME FILTER
        # -----------------------------
        if not row.get("is_trending", False):
            return 0

        # -----------------------------
        # TREND
        # -----------------------------
        trend_up = row["ma_fast"] > row["ma_slow"]
        trend_down = row["ma_fast"] < row["ma_slow"]

        # -----------------------------
        # INVERSE FVG (direction bias)
        # -----------------------------
        bullish_bias = row.get("ifvg_bullish", False)
        bearish_bias = row.get("ifvg_bearish", False)

        # -----------------------------
        # ENTRY (FVG)
        # -----------------------------
        bullish_fvg = row.get("fvg_bullish", False)
        bearish_fvg = row.get("fvg_bearish", False)

        # -----------------------------
        # LONG
        # -----------------------------
        if trend_up and bullish_bias and bullish_fvg:
            return 1

        # -----------------------------
        # SHORT
        # -----------------------------
        if trend_down and bearish_bias and bearish_fvg:
            return -1

        return 0