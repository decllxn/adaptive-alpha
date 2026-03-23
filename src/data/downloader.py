import ccxt  # type: ignore
import pandas as pd  # type: ignore
import time
from datetime import datetime, timedelta


class BinanceDownloader:
    def __init__(self, symbol="ETH/USDT", timeframe="1h"):
        self.exchange = ccxt.binance()
        self.symbol = symbol
        self.timeframe = timeframe

    def fetch_last_n_years(self, years=5, limit=1000):
        all_data = []

        # N years ago
        since_dt = datetime.utcnow() - timedelta(days=365 * years)
        since = int(since_dt.timestamp() * 1000)

        start_time = time.time()

        print(f"🚀 Downloading {years} years of {self.symbol} ({self.timeframe}) data...")
        print(f"📅 Starting from: {since_dt}")

        while True:
            data = self.exchange.fetch_ohlcv(
                self.symbol,
                timeframe=self.timeframe,
                since=since,
                limit=limit
            )

            if not data:
                break

            all_data.extend(data)

            # Move forward
            since = data[-1][0] + 1

            # Progress info
            current_dt = datetime.utcfromtimestamp(data[-1][0] / 1000)
            elapsed = time.time() - start_time

            print(
                f"⏱️ {elapsed:.1f}s | "
                f"📈 Candles: {len(all_data)} | "
                f"🕒 Up to: {current_dt}"
            )

            time.sleep(self.exchange.rateLimit / 1000)

            # Stop if finished
            if len(data) < limit:
                break

        # DataFrame
        df = pd.DataFrame(all_data, columns=[
            "timestamp", "open", "high", "low", "close", "volume"
        ])

        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

        # Remove duplicates
        df = df.drop_duplicates(subset="timestamp").reset_index(drop=True)

        total_time = time.time() - start_time

        print(f"\n✅ Download complete in {total_time:.2f} seconds")
        print(f"📊 Total candles: {len(df)} (~{years} years)")

        return df

    def save_to_csv(self, df, path="data/raw/ETH_5Y.csv"):
        df.to_csv(path, index=False)
        print(f"💾 Saved to {path}")