import numpy as np


def win_rate(trades):
    if len(trades) == 0:
        return 0
    return (trades > 0).mean()


def total_return(equity_curve, initial=10000):
    return (equity_curve[-1] / initial - 1) * 100