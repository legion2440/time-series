from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = REPO_ROOT / "data" / "AAPL.txt"
CHART_PATH = Path(__file__).resolve().with_name("aapl_candlestick.html")
MONTHLY_AGGREGATION = {
    "Open": "mean",
    "Close": "mean",
    "Volume": "sum",
    "High": "max",
    "Low": "min",
    "Adj Close": "mean",
}


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


def business_month_end_frequency() -> str:
    # Pandas 3 renamed the BusinessMonthEnd alias from BM to BME.
    try:
        pd.tseries.frequencies.to_offset("BM")
    except ValueError:
        return "BME"
    return "BM"


def save_candlestick_chart(df: pd.DataFrame) -> None:
    chart_df = df.dropna(subset=["Open", "High", "Low", "Close"])
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=chart_df.index,
                open=chart_df["Open"],
                high=chart_df["High"],
                low=chart_df["Low"],
                close=chart_df["Close"],
                name="AAPL OHLC",
            )
        ]
    )
    fig.update_layout(
        title="AAPL candlestick chart",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
    )
    fig.write_html(CHART_PATH, include_plotlyjs="cdn")
    print(f"Candlestick chart saved to: {CHART_PATH}")
    print(f"Rows used for candlestick chart: {len(chart_df)}")
    print()


def main() -> None:
    print(f"Reading data from: {DATA_PATH}")
    df = read_aapl()
    print_first_look(df)
    clean_df = df.dropna().sort_index()
    print(f"Rows before dropna: {len(df)}")
    print(f"Rows after dropna: {len(clean_df)}")
    print("Missing values after dropna:")
    print(clean_df.isna().sum().to_string())
    print()
    save_candlestick_chart(clean_df)

    month_end_frequency = business_month_end_frequency()
    print("Business month-end target alias from subject/audit: BM")
    print(f"Business month-end frequency used for resample: {month_end_frequency}")
    transformed_df = clean_df.resample(month_end_frequency).agg(MONTHLY_AGGREGATION)
    print("transformed_df.head().to_markdown():")
    print(transformed_df.head().to_markdown())
    print()
    print("Audit view without Adj Close:")
    print(transformed_df[["Open", "Close", "Volume", "High", "Low"]].head().to_markdown())
    print()
    print(f"Number of business month-end rows: {len(transformed_df)}")
    print()

    open_prices = clean_df["Open"]
    daily_returns_pct_change = open_prices.pct_change()
    daily_returns_shift = (open_prices - open_prices.shift(1)) / open_prices.shift(1)
    returns_match = np.allclose(
        daily_returns_pct_change.to_numpy(),
        daily_returns_shift.to_numpy(),
        equal_nan=True,
    )

    print("Daily returns by pct_change() head:")
    print(daily_returns_pct_change.head(10).to_string())
    print()
    print("Daily returns by pct_change() tail:")
    print(daily_returns_pct_change.tail(10).to_string())
    print()
    print(f"Daily returns length: {len(daily_returns_pct_change)}")
    print()
    print("Daily returns by shift formula head:")
    print(daily_returns_shift.head(10).to_string())
    print()
    print("Daily returns by shift formula tail:")
    print(daily_returns_shift.tail(10).to_string())
    print()
    print(f"pct_change() and shift formula results match: {returns_match}")


if __name__ == "__main__":
    main()
