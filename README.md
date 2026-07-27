# Data Engineering Sandbox

Projet full-stack: Ingestion de données météo → Transformation dbt → Dashboard Next.js sur Vercel.

## 🏗️ Architecture

```
Weather API (Open-Meteo)
         ↓
    Airflow DAG (hourly)
         ↓
  Vercel PostgreSQL
      ↙        ↖
   dbt          Next.js
  (marts)      (Dashboard)
```

## 🛠️ Technologies

- **Orchestration:** Apache Airflow (Docker)
- **Transformation:** dbt Core
- **Database:** PostgreSQL (Vercel managed)
- **Frontend:** Next.js + React + Recharts
- **Deployment:** Vercel
- **Language:** Python, TypeScript

## 📦 Structure du Projet

```
├── dags/                          # Airflow DAGs
│   └── weather_ingestion_dag.py   # Ingestion toutes les heures
├── scripts/
│   ├── fetch_weather.py           # Fonction pour API Open-Meteo
│   └── init_vercel_db.sh          # Initialisation DB Vercel
├── dbt_project/
│   ├── models/
│   │   ├── stg/                   # Staging (raw data)
│   │   └── marts/                 # Marts (transformed data for BI)
│   └── profiles.yml               # Config dbt (dev + prod Vercel)
├── docker/
│   ├── docker-compose.yml         # Airflow + PostgreSQL local
│   └── .env                       # Credentials Vercel
├── vercel-app/                    # Next.js application
│   ├── pages/api/                 # API routes (PostgreSQL queries)
│   ├── pages/index.tsx            # Dashboard UI
│   └── lib/db.ts                  # Connection pooling
└── DEPLOYMENT_GUIDE.md            # Guide complet de déploiement
```

## 🚀 Quick Start

### 1. Initialiser Vercel PostgreSQL
```bash
bash scripts/init_vercel_db.sh
```

### 2. Démarrer Airflow (ingestion)
```bash
cd docker
docker compose up -d
# Accéder à http://localhost:8080
```

### 3. Exécuter dbt (transformations)
```bash
cd dbt_project
dbt run --target prod
```

### 4. Démarrer Next.js (dashboard)
```bash
cd vercel-app
npm install && npm run dev
# Accéder à http://localhost:3000
```

## 📖 Documentation Complète

Voir [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) pour:
- Configuration détaillée de chaque composant
- Instructions de déploiement sur Vercel
- Tests de validation
- Troubleshooting

## 📊 Data Flow

1. **Ingestion (Airflow)** 
   - Fetch données Open-Meteo (Nantes, Paris)
   - Insérer dans `stg_raw_weather` (Vercel DB)
   - Toutes les heures

2. **Transformation (dbt)**
   - Transformation brute → vue `stg_weather`
   - Agrégation et descriptions → table `fct_weather`
   - Source pour le dashboard

3. **Visualisation (Next.js)**
   - API routes interrogent `fct_weather`
   - React composants affichent graphiques
   - Déployé sur Vercel (près de la BD)

## 🔑 Environment Variables

**docker/.env:**
```
VERCEL_POSTGRES_HOST=db.prisma.io
VERCEL_POSTGRES_USER=xxxxx
VERCEL_POSTGRES_PASSWORD=xxxxx
...
```

**vercel-app/.env.local:**
```
DATABASE_URL=postgres://user:pass@host/db?sslmode=require
```

## 📝 Notes

- **Hobby Plan:** 1GB stockage, ~100 connexions, gratuit
- **Refresh:** Données mises à jour toutes les heures par Airflow
- **Security:** Ne pas commiter `.env` (voir .gitignore)