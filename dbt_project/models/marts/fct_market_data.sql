SELECT
    ticker,
    trade_date,
    open,
    high,
    low,
    close,
    adj_close,
    volume,
    dividends,
    stock_splits,
    fetched_at
FROM {{ ref('stg_market_data') }}
