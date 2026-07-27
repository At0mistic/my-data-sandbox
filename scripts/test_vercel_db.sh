#!/bin/bash

# Test script to validate Vercel PostgreSQL integration

set -e

echo "=== Testing Vercel PostgreSQL Integration ==="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Credentials
export PGPASSWORD='sk_d1H68Oz5sFZ-rMRwNXeuW'
DB_HOST='db.prisma.io'
DB_PORT='5432'
DB_USER='b79097f3425a8eed5df2b289c22013533277baec7851441d7c8cefcaeab87567'
DB_NAME='postgres'

echo -e "${YELLOW}Test 1: Connection to Vercel PostgreSQL${NC}"
if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Connection successful${NC}"
else
    echo -e "${RED}✗ Connection failed${NC}"
    exit 1
fi
echo ""

echo -e "${YELLOW}Test 2: Check if stg_raw_weather table exists${NC}"
if psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "\d stg_raw_weather" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Table stg_raw_weather exists${NC}"
else
    echo -e "${YELLOW}⚠ Table stg_raw_weather not found (will be created by Airflow)${NC}"
fi
echo ""

echo -e "${YELLOW}Test 3: Check database size${NC}"
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "
SELECT 
  pg_size_pretty(pg_database_size('$DB_NAME')) as database_size;
"
echo ""

echo -e "${YELLOW}Test 4: List all tables${NC}"
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "
SELECT 
  schemaname,
  tablename 
FROM pg_tables 
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY schemaname, tablename;
"
echo ""

echo -e "${GREEN}=== All tests passed! ===${NC}"
echo ""
echo "Next steps:"
echo "1. Start Airflow: cd docker && docker compose up -d"
echo "2. Trigger DAG to ingest data"
echo "3. Run dbt: cd dbt_project && dbt run --target prod"
echo "4. Test API: curl http://localhost:3000/api/weather (when running vercel-app)"
