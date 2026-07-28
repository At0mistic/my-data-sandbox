// pages/api/weather/[city].ts - API endpoint for specific city

import { query } from '@/lib/db';
import { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { city } = req.query;

  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  if (!city || typeof city !== 'string') {
    return res.status(400).json({ error: 'City parameter is required' });
  }

  try {
    const result = await query(
      `SELECT city, temperature_celsius, windspeed_kmh, weather_description, fetched_at 
       FROM public.fct_weather 
       WHERE city = $1`,
      [city]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'City not found' });
    }

    res.status(200).json({
      success: true,
      data: result.rows[0],
    });
  } catch (error) {
    console.error('API error:', error);
    res.status(500).json({
      success: false,
      error: 'Failed to fetch weather data',
    });
  }
}
