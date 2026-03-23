# 📈 Adaptive Alpha: Modular Quantitative Trading System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Framework: PyTorch](https://img.shields.io/badge/Framework-PyTorch-ee4c2c.svg)](https://pytorch.org/)

A research-driven quantitative trading framework for **Crypto Perpetual Futures**, specifically architected for the 2026 market regime. This system integrates **Hybrid ML Signal Generation** with **Reinforcement Learning (RL) Execution** and **Volatility-Adjusted Risk Management**.

---

## 🧠 Core Philosophy

Modern crypto markets are non-stationary. **Adaptive Alpha** rejects static "if-then" logic in favor of a decoupled, three-pillar architecture designed to navigate shifting regimes:

* **📈 Trending:** Momentum-driven expansion phases.
* **🔄 Ranging:** Mean-reverting liquidity clusters.
* **⚡ High-Volatility:** Tail-risk events and liquidity shocks.

> **Key Innovation:** We separate **Intent** (Directional Prediction) from **Action** (Execution Optimization) to ensure the system remains interpretable and robust.

---

## 🏗️ System Architecture



### 1. Signal Engine (LSTM-GRU Hybrid)
The engine predicts the short-term directional probability ($P_t$) using a multivariate feature set $X_t$.

$$P_t = \mathbb{P}(\Delta P_{t+1} > 0 \mid X_t)$$

**Feature Vector ($X_t$):**
* **Microstructure:** Order Book Imbalance (OBI) & Cumulative Volume Delta (CVD).
* **Costs:** Real-time Funding Rates & Spreads.
* **Momentum:** Adaptive ATR-normalized returns.

**Signal Mapping:**
$$S_t = \begin{cases} +1 & \text{if } P_t > \theta_{long} \\ -1 & \text{if } P_t < \theta_{short} \\ 0 & \text{otherwise} \end{cases}$$

---

### 2. Execution Agent (PPO Reinforcement Learning)
The RL agent optimizes entry/exit to minimize slippage and maximize capture of the predicted move.

* **State Space ($s_t$):** $(S_t, \text{OBI}, \text{spread}, \text{inventory}, \sigma_t)$
* **Reward Function ($R_t$):** Focuses on risk-adjusted returns minus execution friction.
  
$$R_t = \Delta \text{PnL}_t - (\lambda_1 \cdot \text{slippage}) - (\lambda_2 \cdot \text{drawdown})$$

---

### 3. Risk Engine (Volatility-Adjusted Kelly)
Position sizing is dynamically scaled based on the **Kelly Criterion**, adjusted for the current volatility regime to prevent ruin.

**Standard Kelly:**
$$f^* = \frac{\mu}{\sigma^2}$$

**Volatility-Adjusted Exposure:**
$$f_t = \left( \frac{\mu_t}{\sigma_t^2} \right) \cdot \left( \frac{\sigma_{target}}{\sigma_t} \right)$$

---

## 🚀 Strategy Selection & Justification

| Approach | Selection | Justification |
| :--- | :---: | :--- |
| **Adaptive Trend + RL** | **SELECTED** | **High robustness; decouples alpha from execution.** |
| Transformer Stat-Arb | Rejected | High compute overhead; prone to overfit on noise. |
| Full MARL | Rejected | Unstable training dynamics in non-stationary markets. |

---

## 🗂️ Project Structure

```bash
adaptive-alpha/
├── configs/           # YAML hyperparameter & API configurations
├── data/              # Parquet-formatted market & on-chain data
├── src/
│   ├── features/      # OBI, CVD, and Z-score transformations
│   ├── models/        # PyTorch LSTM-GRU & PPO Architectures
│   ├── strategy/      # Signal logic & Regime filtering
│   └── backtest/      # Vectorized & Event-driven backtesting
├── tests/             # Unit tests for order execution & math
└── main.py            # System entry point