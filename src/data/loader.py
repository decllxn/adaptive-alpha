import pandas as pd


def load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    # Ensure proper datetime index
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")
    df = df.set_index("timestamp")

    return df