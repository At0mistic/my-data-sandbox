# Weather Dashboard: Airflow + dbt + Next.js

Complete data pipeline with development/production separation.

**Stack:** Apache Airflow | PostgreSQL | dbt | Next.js | Vercel

---

## 🚀 Quick Start (5 Minutes)

### 1. Fix Docker Permission (First Time Only)
```bash
sudo usermod -aG docker $USER
# Log out and log back in
```

### 2. Start Services
```bash
cd docker
docker compose up -d
sleep 30
docker compose ps  # Verify all running
```

### 3. Trigger Data Ingestion
- Open http://localhost:8080 (Airflow)
- Login: `airflow` / `airflow`
- Find `weather_ingestion_etl` DAG
- Click ▶️ trigger button
- Wait for completion (~1-2 min)

### 4. Test Locally
```bash
cd vercel-app
npm install
npm run dev
# Open http://localhost:3000
```

### 5. Deploy to Vercel
```bash
# Push code
git add -A && git commit -m "Weather dashboard" && git push

# Deploy (choose one)
# Option A: CLI
npm install -g vercel && cd vercel-app && vercel

# Option B: Dashboard
# Go to https://vercel.com/new → Select repo → Deploy
```

**Set environment variable in Vercel dashboard:**
- Settings → Environment Variables
- Add: `DATABASE_URL=postgres://b79...@db.prisma.io:5432/postgres?sslmode=require`
- Click Save

✅ **Done!** Dashboard live at: `https://YOUR_PROJECT.vercel.app`

---

## 🏗️ Architecture

```
Open-Meteo API (Weather Data)
    ↓
Airflow (Orchestration - Docker)
    ↓
PostgreSQL (Storage)
    ├─ LOCAL:  localhost:5432 (via .env.local)
    └─ PROD:   db.prisma.io (via .env.production.local)
    ↓
dbt (Transformation)
    ├─ dev:   localhost → fct_weather
    └─ prod:  Vercel DB → fct_weather
    ↓
Next.js API
    ├─ /api/weather         (all cities)
    └─ /api/weather/[city]  (specific city)
    ↓
Dashboard UI
    ├─ LOCAL:  localhost:3000
    └─ PROD:   vercel.app
```

**Key Principle:** Single source of truth = Vercel PostgreSQL (same DB for dev & prod)

---

## 📁 Project Structure

```
.
├── docker/                      # Docker & Airflow
│   ├── docker-compose.yml       # Services: postgres, airflow
│   ├── .env                     # Vercel credentials (gitignored)
│   └── create_connections.py    # Setup postgres_vercel connection
│
├── dags/                        # Airflow DAGs
│   └── weather_ingestion_dag.py # Fetch weather hourly
│
├── scripts/                     # Python utilities
│   └── fetch_weather.py         # Open-Meteo API client
│
├── dbt_project/                 # dbt transformations
│   ├── profiles.yml             # dev & prod targets
│   ├── models/stg/              # Staging layer
│   └── models/marts/            # Final models (fct_weather)
│
├── vercel-app/                  # Next.js dashboard
│   ├── .env.local               # LOCAL: localhost:5432
│   ├── .env.production.local    # PROD: db.prisma.io
│   ├── lib/db.ts                # Connection pool
│   ├── pages/api/weather.ts     # API endpoints
│   └── pages/index.tsx          # Dashboard UI
│
└── README.md                    # This file
```

---

## ⚙️ Configuration

### .env Files
```bash
# vercel-app/.env.local (Development)
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/data_warehouse"

# vercel-app/.env.production.local (Production)
DATABASE_URL="postgres://b79...@db.prisma.io:5432/postgres?sslmode=require"
```

### dbt Targets
```bash
dbt run --target dev    # Uses localhost
dbt run --target prod   # Uses Vercel DB
```

---

## 📊 Data Flow

**Development:** Airflow → Vercel DB ← npm run dev → localhost:3000

**Production:** Airflow → Vercel DB ← Vercel deployment → vercel.app

---

## 🔧 Common Commands

```bash
# Start services
cd docker && docker compose up -d

# View logs
docker compose logs -f [service]

# Run dbt
cd dbt_project && dbt run --target dev

# Start dashboard
cd vercel-app && npm run dev

# Stop services
docker compose down
```

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Docker permission denied | `sudo usermod -aG docker $USER` → logout/in |
| Airflow won't start | `docker compose logs airflow-init` |
| DAG not visible | Wait 30s, refresh page |
| dbt connection fails | `dbt debug --target dev` |
| No data in dashboard | 1) Trigger DAG 2) Run dbt 3) Refresh app |
| Vercel deploy fails | Check `DATABASE_URL` in dashboard env vars |

---

## 🔐 Security

- ✅ `.env*` files in `.gitignore` (never committed)
- ✅ No credentials in source code
- ✅ Uses `process.env.DATABASE_URL` only
- ✅ Vercel env vars set in dashboard

---

## 📚 Key Concepts

- **Single Source of Truth:** Same Vercel DB for dev & prod (no duplication)
- **Environment Switching:** Automatic via `.env.local` vs `.env.production.local`
- **dbt Targets:** `dev` (localhost) and `prod` (Vercel)
- **Airflow Connection:** `postgres_vercel` feeds Vercel PostgreSQL

---

## ✅ Deployment Checklist

- [ ] Local dashboard works (http://localhost:3000)
- [ ] All files committed to GitHub
- [ ] `.env*` files protected in `.gitignore`
- [ ] Code pushed to GitHub
- [ ] Vercel deployment complete
- [ ] `DATABASE_URL` set in Vercel dashboard
- [ ] Live dashboard accessible

---

**Ready?** Follow Quick Start above! 🚀