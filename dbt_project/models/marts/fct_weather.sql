-- Modèle d'exposition: Dernières relevés météo avec calculs

WITH weather_staged AS (
    SELECT 
        id,
        city,
        fetched_at,
        temperature_celsius,
        windspeed_kmh,
        weather_code
    FROM {{ ref('stg_weather') }}
),

latest_by_city AS (
    SELECT 
        city,
        temperature_celsius,
        windspeed_kmh,
        weather_code,
        fetched_at,
        ROW_NUMBER() OVER (PARTITION BY city ORDER BY fetched_at DESC) as rn
    FROM weather_staged
),

final AS (
    SELECT 
        city,
        temperature_celsius,
        windspeed_kmh,
        weather_code,
        fetched_at,
        CASE 
            WHEN weather_code = 0 THEN 'Clear sky'
            WHEN weather_code = 1 THEN 'Mainly clear'
            WHEN weather_code = 2 THEN 'Partly cloudy'
            WHEN weather_code = 3 THEN 'Overcast'
            WHEN weather_code IN (45, 48) THEN 'Foggy'
            WHEN weather_code IN (51, 53, 55) THEN 'Light to moderate drizzle'
            WHEN weather_code IN (61, 63, 65) THEN 'Slight to moderate rain'
            WHEN weather_code IN (71, 73, 75) THEN 'Slight to heavy snow'
            WHEN weather_code = 77 THEN 'Snow grains'
            WHEN weather_code IN (80, 81, 82) THEN 'Rain showers'
            WHEN weather_code IN (85, 86) THEN 'Snow showers'
            WHEN weather_code = 95 THEN 'Thunderstorm'
            WHEN weather_code IN (96, 99) THEN 'Thunderstorm with hail'
            ELSE 'Unknown'
        END as weather_description
    FROM latest_by_city
    WHERE rn = 1
)

SELECT * FROM final
