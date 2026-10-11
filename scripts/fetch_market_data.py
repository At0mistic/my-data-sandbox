"""Download daily MSCI World market data from Yahoo Finance."""

from datetime import date, datetime, timezone
import math
from typing import Any
import warnings

import yfinance as yf

YEARS_OF_HISTORY = 15
MARKET_TICKERS = ("^990100-USD-STRD", "URTH")
PRICE_COLUMNS = {
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Close": "close",
    "Adj Close": "adj_close",
    "Volume": "volume",
    "Dividends": "dividends",
    "Stock Splits": "stock_splits",
}


def _history_start(today: date) -> date:
    year = today.year - YEARS_OF_HISTORY
    day = min(today.day, 28 if today.month == 2 else today.day)
    return date(year, today.month, day)


def _number_or_none(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def fetch_market_data() -> tuple[str, list[dict[str, Any]]]:
    """Fetch up to 15 years of daily prices, preferring the MSCI World index."""
    today = datetime.now(timezone.utc).date()
    start_date = _history_start(today)
    rows: list[dict[str, Any]] = []

    for ticker in MARKET_TICKERS:
        history = yf.download(
            ticker,
            start=start_date.isoformat(),
            end=today.isoformat(),
            interval="1d",
            auto_adjust=False,
            actions=True,
            progress=False,
            threads=False,
            multi_level_index=False,
        )
        if history.empty:
            continue

        rows = []
        for timestamp, quote in history.iterrows():
            row: dict[str, Any] = {
                "ticker": ticker,
                "trade_date": timestamp.date(),
            }
            for source_column, target_column in PRICE_COLUMNS.items():
                value = _number_or_none(quote.get(source_column))
                row[target_column] = (
                    int(value)
                    if target_column == "volume" and value is not None
                    else value
                )
            rows.append(row)

        if ticker != MARKET_TICKERS[0]:
            warnings.warn(
                f"No history was returned for {MARKET_TICKERS[0]}; using {ticker}.",
                RuntimeWarning,
                stacklevel=2,
            )
        return ticker, rows

    raise RuntimeError(
        "Yahoo Finance returned no daily history for the MSCI World index "
        "or the URTH ETF."
    )
