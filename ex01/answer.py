import pandas as pd


def build_integer_series() -> pd.Series:
    date_index = pd.date_range("2010-01-01", "2020-12-31", freq="D")
    return pd.Series(
        range(date_index.size),
        index=date_index,
        name="integer_series",
    )


def main() -> None:
    integer_series = build_integer_series()
    moving_average_7d = integer_series.rolling(window=7).mean()

    print(f"integer_series length: {len(integer_series)}")
    print(f"7-day moving average length: {len(moving_average_7d)}")
    print()
    print("integer_series head:")
    print(integer_series.head(10).to_string())
    print()
    print("integer_series tail:")
    print(integer_series.tail(10).to_string())
    print()
    print("7-day moving average head:")
    print(moving_average_7d.head(10).to_string())
    print()
    print("7-day moving average tail:")
    print(moving_average_7d.tail(10).to_string())


if __name__ == "__main__":
    main()
