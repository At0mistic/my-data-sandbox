from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import uvicorn

from weather_client import get_weather_for_city

app = FastAPI(title="Instant Météo Nantes")


@app.get("/")
def read_root():
    return FileResponse("index.html")


@app.get("/api/weather/nantes")
def get_nantes_weather():
    try:
        weather = get_weather_for_city("Nantes")
        return {"status": "success", "data": weather}
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Impossible de récupérer la météo : {exc}",
        ) from exc


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
