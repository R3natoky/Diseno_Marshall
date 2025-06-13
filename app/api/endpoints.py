# app/api/endpoints.py

from fastapi import APIRouter, HTTPException, status
from app.models.marshall_models import MarshallInput, MarshallOutput
from app.services.marshall_calculator import analyze_marshall_data

router = APIRouter()

@router.post(
    "/analyze",
    response_model=MarshallOutput,
    summary="Analiza datos de Ensayo Marshall",
    description="Recibe los datos de un ensayo Marshall, calcula las curvas de "
                "regresión y determina el contenido óptimo de asfalto.",
    tags=["Marshall Analysis"]
)
def analyze_marshall_endpoint(data: MarshallInput):
    """
    Endpoint para realizar el análisis completo del diseño Marshall.
    """
    try:
        # Llama a la función de servicio con los datos validados por Pydantic
        results = analyze_marshall_data(
            asphalt_content=data.asphalt_content,
            unit_weight=data.unit_weight,
            voids_percentage=data.voids_percentage,
            vma_percentage=data.vma_percentage,
            vfa_percentage=data.vfa_percentage,
            stability=data.stability,
            flow=data.flow,
            target_voids=data.target_voids
        )
        return results
    except ValueError as e:
        # Si el servicio lanza un error (ej: no se encuentra raíz),
        # lo capturamos y devolvemos un error HTTP 400.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Captura de cualquier otro error inesperado.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ha ocurrido un error inesperado: {e}"
        )