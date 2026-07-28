// pages/api/weather.ts - API endpoint to fetch latest weather data

import { query } from '@/lib/db';
import { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Query the fct_weather dbt model (marts table)
    const result = await query(
      `SELECT city, temperature_celsius, windspeed_kmh, weather_description, fetched_at 
       FROM public.fct_weather 
       ORDER BY city ASC`
    );

    res.status(200).json({
      success: true,
      data: result.rows,
      count: result.rowCount,
    });
  } catch (error) {
    console.error('API error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch weather data',
    });
  }
}
