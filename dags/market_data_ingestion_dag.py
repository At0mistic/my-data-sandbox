from datetime import datetime, timedelta
import os
import sys

from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.bash import BashOperator

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from fetch_market_data import fetch_market_data

default_args = {
    "owner": "data_team",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="market_data_ingestion_etl",
    default_args=default_args,
    description="Daily MSCI World market data from Yahoo Finance to PostgreSQL",
    schedule_interval="0 6 * * 1-5",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["ingestion", "market-data", "raw"],
)
def market_data_ingestion_pipeline():
    create_table = PostgresOperator(
        task_id="create_raw_market_data_table",
        postgres_conn_id="postgres_local",
        sql="""
            CREATE TABLE IF NOT EXISTS stg_raw_market_data (
                ticker VARCHAR(32) NOT NULL,
                trade_date DATE NOT NULL,
                open NUMERIC,
                high NUMERIC,
                low NUMERIC,
                close NUMERIC,
                adj_close NUMERIC,
                volume BIGINT,
                dividends NUMERIC,
                stock_splits NUMERIC,
                fetched_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                PRIMARY KEY (ticker, trade_date)
            );
        """,
    )

    @task
    def fetch_and_store_market_data():
        ticker, rows = fetch_market_data()
        pg_hook = PostgresHook(postgres_conn_id="postgres_local")
        conn = pg_hook.get_conn()
        try:
            with conn.cursor() as cursor:
                cursor.executemany(
                    """
                    INSERT INTO stg_raw_market_data (
                        ticker, trade_date, open, high, low, close, adj_close,
                        volume, dividends, stock_splits
                    )
                    VALUES (
                        %(ticker)s, %(trade_date)s, %(open)s, %(high)s, %(low)s,
                        %(close)s, %(adj_close)s, %(volume)s, %(dividends)s,
                        %(stock_splits)s
                    )
                    ON CONFLICT (ticker, trade_date) DO UPDATE SET
                        open = EXCLUDED.open,
                        high = EXCLUDED.high,
                        low = EXCLUDED.low,
                        close = EXCLUDED.close,
                        adj_close = EXCLUDED.adj_close,
                        volume = EXCLUDED.volume,
                        dividends = EXCLUDED.dividends,
                        stock_splits = EXCLUDED.stock_splits,
                        fetched_at = NOW();
                    """,
                    rows,
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

        return {"ticker": ticker, "rows_upserted": len(rows)}

    run_dbt_models = BashOperator(
        task_id="run_dbt_models",
        bash_command="""
            cd /opt/airflow/dbt_project && \
            dbt build --profiles-dir .
        """,
    )

    create_table >> fetch_and_store_market_data() >> run_dbt_models


market_data_ingestion_pipeline()
