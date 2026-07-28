// lib/db.ts - PostgreSQL connection pool for Vercel

import { Pool } from 'pg';

// Create a connection pool with proper timeouts for Vercel Hobby plan
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  max: 5, // Hobby plan limit
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 5000,
});

pool.on('error', (err) => {
  console.error('Unexpected error on idle client', err);
});

export async function query(text: string, params?: any[]) {
  const start = Date.now();
  try {
    const result = await pool.query(text, params);
    const duration = Date.now() - start;
    console.log('Executed query', { text, duration, rows: result.rowCount });
    return result;
  } catch (error) {
    console.error('Database query error:', error);
    throw error;
  }
}

export async function getClient() {
  const client = await pool.connect();
  return {
    query: (text: string, params?: any[]) => client.query(text, params),
    release: () => client.release(),
  };
}
