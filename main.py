from src.data.loader import load_csv
from src.features.technicals import (
    compute_returns,
    compute_atr,
    compute_moving_averages,
    compute_regime
)
from src.features.microstructure import fair_value_gaps
from src.strategy.signal_engine import SignalEngine
from src.backtest.engine import Backtester
from src.backtest.metrics import win_rate, total_return


def main():
    # -----------------------------
    # Load Data (5-Year ETH)
    # -----------------------------
    df = load_csv("data/raw/ETH_5Y.csv")

    print(f"Loaded dataset: {len(df)} rows")

    # -----------------------------
    # Feature Engineering
    # -----------------------------
    df = compute_returns(df)
    df = compute_atr(df)
    df = compute_moving_averages(df)

    # 🔥 NEW: Regime detection
    df = compute_regime(df)

    # 🔥 NEW: FVG + IFVG logic
    df = fair_value_gaps(df)

    # Clean NaNs AFTER all features
    df = df.dropna()

    print(f"After feature engineering: {len(df)} rows")

    # -----------------------------
    # Strategy
    # -----------------------------
    strategy = SignalEngine()

    # -----------------------------
    # Backtest
    # -----------------------------
    bt = Backtester(
        df,
        strategy,
        initial_capital=10000,
        risk_per_trade=0.01,
        fee=0.0004
    )

    equity_curve, trades = bt.run()

    # -----------------------------
    # Metrics
    # -----------------------------
    final_equity = equity_curve[-1]
    total_ret = total_return(equity_curve)
    num_trades = len(trades)
    winrate = win_rate(trades)

    # -----------------------------
    # Output
    # -----------------------------
    print("\n📊 RESULTS (Regime + FVG Strategy | 5Y ETH)")
    print(f"Final Equity: ${final_equity:.2f}")
    print(f"Total Return: {total_ret:.2f}%")
    print(f"Number of Trades: {num_trades}")
    print(f"Win Rate: {winrate * 100:.2f}%")

    if num_trades > 0:
        print(f"Avg Trade PnL: {trades.mean():.2f}")

    print("-" * 40)


if __name__ == "__main__":
    main()