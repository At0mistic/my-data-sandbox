#!/bin/bash

# Script to initialize Vercel PostgreSQL database
# Creates necessary tables for weather ingestion pipeline

set -e

echo "=== Initializing Vercel PostgreSQL Database ==="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Extract connection info from DATABASE_URL
export PGPASSWORD='sk_d1H68Oz5sFZ-rMRwNXeuW'

DB_HOST='db.prisma.io'
DB_PORT='5432'
DB_USER='b79097f3425a8eed5df2b289c22013533277baec7851441d7c8cefcaeab87567'
DB_NAME='postgres'

echo -e "${YELLOW}Connecting to Vercel PostgreSQL...${NC}"
echo "Host: $DB_HOST"
echo "Database: $DB_NAME"
echo ""

# Create stg_raw_weather table
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" <<EOF
-- Create raw weather table
CREATE TABLE IF NOT EXISTS stg_raw_weather (
    id SERIAL PRIMARY KEY,
    city VARCHAR(50),
    fetched_at TIMESTAMP,
    raw_payload JSONB
);

-- Create index for performance
CREATE INDEX IF NOT EXISTS idx_stg_raw_weather_city_fetched ON stg_raw_weather(city, fetched_at DESC);

-- Display table info
\d stg_raw_weather
EOF

echo ""
echo -e "${GREEN}✓ Database initialization complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Start Airflow: cd docker && docker compose up -d"
echo "2. Trigger DAG in Airflow UI: http://localhost:8080"
echo "3. Run dbt: dbt run --profiles-dir . --target prod (from dbt_project/)"
echo "4. Deploy Next.js: cd vercel-app && npm install && npm run build"
