from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = REPO_ROOT / "data" / "AAPL.txt"
CHART_PATH = Path(__file__).resolve().with_name("strategy_daily_pnl.html")


def read_aapl() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, na_values=["null"])
    print("Missing values before preprocessing:")
    print(df.isna().sum().to_string())
    print()

    df["Date"] = pd.to_datetime(df["Date"], errors="raise")
    df = df.set_index("Date").sort_index()
    return df


def print_first_look(df: pd.DataFrame) -> None:
    buffer = StringIO()
    df.info(buf=buffer)
    print("DataFrame info:")
    print(buffer.getvalue())
    print("DataFrame describe:")
    print(df.describe().to_string())
    print()


def total_return(pnl: pd.Series, signal: pd.Series) -> float:
    signal_sum = signal.sum()
    if signal_sum == 0:
        return float("nan")
    return pnl.sum() / signal_sum


def save_pnl_chart(random_pnl: pd.Series, always_buy_pnl: pd.Series) -> None:
    fig = go.Figure()
    fig.add_scatter(
        x=random_pnl.index,
        y=random_pnl,
        mode="lines",
        name="random strategy daily PnL",
    )
    fig.add_scatter(
        x=always_buy_pnl.index,
        y=always_buy_pnl,
        mode="lines",
        name="always-buy daily PnL",
    )
    fig.update_layout(
        title="AAPL strategy daily PnL",
        xaxis_title="Date",
        yaxis_title="Daily PnL",
    )
    fig.write_html(CHART_PATH, include_plotlyjs="cdn")
    print(f"Strategy PnL chart saved to: {CHART_PATH}")
    print()


def main() -> None:
    print(f"Reading data from: {DATA_PATH}")
    df = read_aapl()
    print_first_look(df)
    print(f"Rows before dropna: {len(df)}")
    df = df.dropna().sort_index()
    print(f"Rows after dropna: {len(df)}")
    print("Missing values after dropna:")
    print(df.isna().sum().to_string())
    print()

    price = df["Adj Close"]
    Daily_futur_returns = ((price.shift(-1) - price) / price).rename("Daily_futur_returns")

    np.random.seed(2712)
    long_only_signal = pd.Series(
        np.random.randint(0, 2, size=len(df)),
        index=df.index,
        name="long_only_signal",
    )
    print(f"long_only_signal index equals df index: {long_only_signal.index.equals(df.index)}")
    print("long_only_signal head:")
    print(long_only_signal.head(10).to_string())
    print()
    print("long_only_signal tail:")
    print(long_only_signal.tail(10).to_string())
    print()

    random_pnl = (long_only_signal * Daily_futur_returns).rename("PnL")
    random_total_return = total_return(random_pnl, long_only_signal)

    always_buy_signal = pd.Series(1, index=df.index, name="always_buy_signal")
    always_buy_pnl = (always_buy_signal * Daily_futur_returns).rename("always_buy_PnL")
    always_buy_total_return = total_return(always_buy_pnl, always_buy_signal)

    print("Daily_futur_returns head:")
    print(Daily_futur_returns.head(10).to_string())
    print()
    print("Daily_futur_returns tail:")
    print(Daily_futur_returns.tail(10).to_string())
    print()
    print("Random strategy PnL head:")
    print(random_pnl.head(10).to_string())
    print()
    print("Random strategy PnL tail:")
    print(random_pnl.tail(10).to_string())
    print()
    print("Always-buy strategy PnL head:")
    print(always_buy_pnl.head(10).to_string())
    print()
    print("Always-buy strategy PnL tail:")
    print(always_buy_pnl.tail(10).to_string())
    print()

    save_pnl_chart(random_pnl, always_buy_pnl)

    print(f"Random strategy invested days: {long_only_signal.sum()}")
    print(f"Random strategy total return: {random_total_return}")
    print(f"Always-buy strategy invested days: {always_buy_signal.sum()}")
    print(f"Always-buy strategy total return: {always_buy_total_return}")


if __name__ == "__main__":
    main()
