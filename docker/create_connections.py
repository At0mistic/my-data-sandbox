#!/usr/bin/env python3
"""
Create Airflow connections programmatically
This script runs during docker-compose initialization
"""

import os
from airflow.models import Connection
from airflow.utils.db import merge_conn

# Get credentials from environment variables
vercel_host = os.getenv('VERCEL_POSTGRES_HOST', 'db.prisma.io')
vercel_port = os.getenv('VERCEL_POSTGRES_PORT', '5432')
vercel_user = os.getenv('VERCEL_POSTGRES_USER', '')
vercel_password = os.getenv('VERCEL_POSTGRES_PASSWORD', '')
vercel_db = os.getenv('VERCEL_POSTGRES_DB', 'postgres')

print(f"Creating Airflow connection: postgres_vercel")
print(f"  Host: {vercel_host}")
print(f"  User: {vercel_user[:10]}...")  # Hide sensitive info
print(f"  Database: {vercel_db}")

# Create the connection to vercel DB
conn = Connection(
    conn_id='postgres_vercel',
    conn_type='postgres',
    host=vercel_host,
    port=int(vercel_port),
    login=vercel_user,
    password=vercel_password,
    schema=vercel_db,
    extra='{"sslmode": "require"}'
)

conn_local = Connection(
    conn_id='postgres_local',
    conn_type='postgres',
    host='postgres',
    port=5432,
    login=os.getenv('POSTGRES_USER', 'postgres'),
    password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
    schema=os.getenv('POSTGRES_DB', 'data_warehouse'),
    extra='{"sslmode": "disable"}'
)

# Save connection
merge_conn(conn)
merge_conn(conn_local)
print("✓ Connection created successfully!")
