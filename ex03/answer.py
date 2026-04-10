import numpy as np
import pandas as pd


def build_multiindex_dataframe() -> pd.DataFrame:
    business_dates = pd.bdate_range("2021-01-01", "2021-12-31")
    tickers = ["AAPL", "FB", "GE", "AMZN", "DAI"]
    index = pd.MultiIndex.from_product([business_dates, tickers], names=["Date", "Ticker"])

    np.random.seed(2712)
    return pd.DataFrame(
        index=index,
        data=np.random.randn(len(index), 1),
        columns=["Price"],
    )


def main() -> None:
    market_data = build_multiindex_dataframe()
    daily_returns = market_data.pivot_table(
        values="Price",
        index="Date",
        columns="Ticker",
    ).pct_change()

    print("MultiIndex DataFrame head:")
    print(market_data.head(10).to_string())
    print()
    print(f"Daily returns shape: {daily_returns.shape}")
    print()
    print("Daily returns head:")
    print(daily_returns.head().to_string())


if __name__ == "__main__":
    main()
