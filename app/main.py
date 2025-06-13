# app/main.py

from fastapi import FastAPI
from app.api import endpoints

# Crea la instancia de la aplicación FastAPI
app = FastAPI(
    title="API de Diseño de Mezcla Asfáltica Marshall",
    description="Una API para calcular el diseño óptimo de asfalto "
                "basado en el método Marshall, a partir de datos de ensayo.",
    version="1.0.0"
)

# Incluye el router de los endpoints bajo el prefijo /api/v1
app.include_router(endpoints.router, prefix="/api/v1", tags=["Marshall Analysis"])

@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint raíz que devuelve un mensaje de bienvenida.
    """
    return {"message": "Bienvenido a la API de Diseño Marshall. Visita /docs para la documentación interactiva."}