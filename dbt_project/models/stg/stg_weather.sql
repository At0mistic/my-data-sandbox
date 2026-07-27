WITH raw AS (
    SELECT 
        id,
        city,
        fetched_at,
        (raw_payload->>'temperature')::numeric AS temperature_celsius,
        (raw_payload->>'windspeed')::numeric AS windspeed_kmh,
        (raw_payload->>'weathercode')::integer AS weather_code
    FROM {{ source('raw_data', 'stg_raw_weather') }}
)

SELECT * FROM raw