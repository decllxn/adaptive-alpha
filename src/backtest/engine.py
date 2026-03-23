import numpy as np


class Backtester:
    def __init__(self, df, strategy, initial_capital=10000, risk_per_trade=0.01, fee=0.0004):
        self.df = df
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.risk_per_trade = risk_per_trade
        self.fee = fee

    def run(self):
        equity = self.initial_capital
        equity_curve = []

        position = None
        trades = []

        for i in range(1, len(self.df)):
            row = self.df.iloc[i]

            # ---------------- ENTRY ----------------
            if position is None:
                signal = self.strategy.generate(row)

                if signal != 0 and row["atr"] > 0:
                    entry_price = row["close"]

                    stop_distance = row["atr"]
                    risk_amount = equity * self.risk_per_trade
                    size = risk_amount / stop_distance

                    stop_loss = (
                        entry_price - stop_distance if signal == 1
                        else entry_price + stop_distance
                    )

                    position = {
                        "type": signal,
                        "entry_price": entry_price,
                        "size": size,
                        "stop_loss": stop_loss,
                        "bars_held": 0
                    }

                    equity *= (1 - self.fee)

            # ---------------- MANAGEMENT ----------------
            else:
                price = row["close"]
                position["bars_held"] += 1

                # stop loss
                if position["type"] == 1 and price <= position["stop_loss"]:
                    pnl = (price - position["entry_price"]) * position["size"]
                    equity += pnl
                    equity *= (1 - self.fee)

                    trades.append(pnl)
                    position = None

                elif position["type"] == -1 and price >= position["stop_loss"]:
                    pnl = (position["entry_price"] - price) * position["size"]
                    equity += pnl
                    equity *= (1 - self.fee)

                    trades.append(pnl)
                    position = None

                # exit on trend flip (after minimum hold)
                elif position["bars_held"] > 5:
                    signal = self.strategy.generate(row)

                    if signal == -position["type"]:
                        pnl = (
                            (price - position["entry_price"]) * position["size"]
                            if position["type"] == 1
                            else (position["entry_price"] - price) * position["size"]
                        )

                        equity += pnl
                        equity *= (1 - self.fee)

                        trades.append(pnl)
                        position = None

            equity_curve.append(equity)

        return equity_curve, np.array(trades)