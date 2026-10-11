SELECT
    ticker,
    trade_date,
    open::numeric AS open,
    high::numeric AS high,
    low::numeric AS low,
    close::numeric AS close,
    adj_close::numeric AS adj_close,
    volume::bigint AS volume,
    dividends::numeric AS dividends,
    stock_splits::numeric AS stock_splits,
    fetched_at
FROM {{ source('raw_data', 'stg_raw_market_data') }}
