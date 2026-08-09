import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(
    title="Weather Datamart API",
    description="API exposant les données nettoyées du Data Mart dbt",
    version="1.0.0"
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for local development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Récupération des paramètres de connexion (variables d'environnement)
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_NAME = os.getenv("POSTGRES_DB", "data_warehouse")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")


def get_db_connection():
    """Établit la connexion à PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            cursor_factory=RealDictCursor  # Renvoie les résultats sous forme de dictionnaire Python
        )
        return conn
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de connexion à la BDD: {str(e)}")


@app.get("/")
def read_root():
    """Serve the weather dashboard HTML page"""
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    return FileResponse(html_path, media_type="text/html")


@app.get("/api/v1/weather/latest")
def get_latest_weather(city: str = None):
    """
    Récupère le dernier relevé météo enregistré dans le Datamart (fct_weather_readings).
    Possibilité de filtrer par ville (ex: /api/v1/weather/latest?city=Nantes).
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if city:
            query = """
                SELECT * 
                FROM fct_weather
                WHERE LOWER(city) = LOWER(%s)
                ORDER BY fetched_at DESC 
                LIMIT 1;
            """
            cursor.execute(query, (city,))
        else:
            query = """
                SELECT * 
                FROM fct_weather 
                ORDER BY fetched_at DESC 
                LIMIT 1;
            """
            cursor.execute(query)

        latest_reading = cursor.fetchone()

        if not latest_reading:
            raise HTTPException(status_code=404, detail="Aucun relevé trouvé dans le datamart.")

        return {
            "status": "success",
            "data": latest_reading
        }

    finally:
        cursor.close()
        conn.close()