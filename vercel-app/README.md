# Weather Dashboard with Vercel PostgreSQL

Next.js dashboard for visualizing weather data from dbt models.

## Setup

1. Create `.env.local` with your Vercel PostgreSQL credentials:
```env
DATABASE_URL=postgresql://user:password@host:5432/database?sslmode=require
```

2. Install dependencies:
```bash
npm install
```

3. Run development server:
```bash
npm run dev
```

4. Open http://localhost:3000

## Build for production:
```bash
npm run build
npm start
```

## Deployment to Vercel

1. Push to GitHub
2. Import project in Vercel dashboard
3. Add `DATABASE_URL` environment variable
4. Deploy!
