from datetime import datetime, timedelta
import json
from airflow.decorators import dag, task
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.bash import BashOperator

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from fetch_weather import get_weather_data, CITIES

default_args = {
    'owner': 'data_team',
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

@dag(
    dag_id='weather_ingestion_etl',
    default_args=default_args,
    description='Extraction météo Open-Meteo vers PostgreSQL (Raw)',
    schedule_interval='@hourly',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['ingestion', 'weather', 'raw']
)
def weather_ingestion_pipeline():

    # Task 1 : Création de la table 'raw_weather' si elle n'existe pas.
    create_table = PostgresOperator(
        task_id='create_raw_table',
        postgres_conn_id='postgres_local',
        sql="""
            CREATE TABLE IF NOT EXISTS stg_raw_weather (
                id SERIAL PRIMARY KEY,
                city VARCHAR(50),
                fetched_at TIMESTAMP,
                raw_payload JSONB
            );
        """
    )

    # Task 2 : Extraction et insertion pour chaque ville
    @task
    def fetch_and_store_weather():
        # Connexion à Postgres via le hook Airflow
        pg_hook = PostgresHook(postgres_conn_id='postgres_local')
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        for city in CITIES.keys():
            data = get_weather_data(city)
            
            # Requete d'insertion JSONB
            insert_query = """
                INSERT INTO stg_raw_weather (city, fetched_at, raw_payload)
                VALUES (%s, %s, %s);
            """
            cursor.execute(
                insert_query, 
                (data['city'], data['fetched_at'], json.dumps(data))
            )

        conn.commit()
        cursor.close()
        conn.close()

    # 3. Tâche dbt build (Exécute staging, intermediate et marts avec tests)
    run_dbt_models = BashOperator(
        task_id='run_dbt_models',
        bash_command='''
            cd /opt/airflow/dbt_project && \
            dbt build --profiles-dir .
        '''
    )

    # Chaînage des tâches
    create_table >> fetch_and_store_weather() >> run_dbt_models

# Instanciation du DAG
weather_ingestion_pipeline()