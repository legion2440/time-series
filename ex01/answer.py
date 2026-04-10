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
    print()
    print("integer_series:")
    print(integer_series)
    print()
    print(f"7-day moving average length: {len(moving_average_7d)}")
    print()
    print("7-day moving average:")
    print(moving_average_7d)


if __name__ == "__main__":
    main()
