// pages/index.tsx - Main dashboard page

import { useEffect, useState } from 'react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface WeatherData {
  city: string;
  temperature_celsius: number;
  windspeed_kmh: number;
  weather_description: string;
  fetched_at: string;
}

export default function Home() {
  const [weatherData, setWeatherData] = useState<WeatherData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('/api/weather')
      .then((res) => res.json())
      .then((result) => {
        if (result.success) {
          setWeatherData(result.data);
        } else {
          setError(result.error);
        }
      })
      .catch((err) => {
        console.error('Error fetching weather:', err);
        setError('Failed to load weather data');
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8 text-center">Loading...</div>;
  if (error) return <div className="p-8 text-center text-red-500">Error: {error}</div>;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-blue-100 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Weather Dashboard</h1>
          <p className="text-gray-600">Real-time weather data from Nantes & Paris</p>
        </div>

        {/* Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          {weatherData.map((data) => (
            <div key={data.city} className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-bold text-gray-800 mb-4">{data.city}</h2>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-gray-600 text-sm">Temperature</p>
                  <p className="text-3xl font-bold text-blue-600">{data.temperature_celsius}°C</p>
                </div>
                <div>
                  <p className="text-gray-600 text-sm">Wind Speed</p>
                  <p className="text-3xl font-bold text-green-600">{data.windspeed_kmh} km/h</p>
                </div>
              </div>
              <div className="mt-4">
                <p className="text-gray-600 text-sm">Condition</p>
                <p className="text-lg text-gray-800">{data.weather_description}</p>
              </div>
              <p className="text-xs text-gray-500 mt-4">Last updated: {new Date(data.fetched_at).toLocaleString()}</p>
            </div>
          ))}
        </div>

        {/* Simple Chart */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">Temperature Comparison</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={weatherData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="city" />
              <YAxis label={{ value: 'Temperature (°C)', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Bar dataKey="temperature_celsius" fill="#3b82f6" name="Temperature" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
