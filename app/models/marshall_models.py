# app/models/marshall_models.py

from pydantic import BaseModel, Field
from typing import List, Dict, Any

# --- Modelos para la Entrada de la API ---

class MarshallInput(BaseModel):
    """
    Modelo para los datos de entrada del ensayo Marshall.
    El cliente de la API debe enviar un JSON con esta estructura.
    """
    asphalt_content: List[float] = Field(
        ..., 
        example=[4.5, 5.0, 5.5, 6.0], 
        description="Lista de contenidos de asfalto (%)"
    )
    unit_weight: List[float] = Field(
        ..., 
        example=[2.459, 2.476, 2.496, 2.520],
        description="Lista de pesos unitarios (g/cm³)"
    )
    voids_percentage: List[float] = Field(
        ...,
        example=[7.1, 5.8, 4.1, 2.3],
        description="Lista de porcentajes de vacíos (%)"
    )
    vma_percentage: List[float] = Field(
        ...,
        example=[16.61, 16.47, 16.26, 15.90],
        description="Lista de Vacíos en el Agregado Mineral (%)"
    )
    vfa_percentage: List[float] = Field(
        ...,
        example=[57.17, 64.84, 75.55, 85.46],
        description="Lista de Vacíos Llenos con Asfalto (%)"
    )
    stability: List[float] = Field(
        ...,
        example=[1110, 1157, 1159, 1128],
        description="Lista de valores de estabilidad (kg)"
    )
    flow: List[float] = Field(
        ...,
        example=[2.85, 3.12, 3.35, 3.42],
        description="Lista de valores de flujo (mm)"
    )
    target_voids: float = Field(
        default=4.0, 
        gt=0, 
        lt=10, 
        description="Porcentaje de vacíos objetivo para el diseño"
    )

    class Config:
        """Configuración para que Pydantic genere un ejemplo en la UI de Swagger."""
        json_schema_extra = {
            "example": {
                "asphalt_content": [4.5, 5.0, 5.5, 6.0],
                "unit_weight": [2.459, 2.476, 2.496, 2.520],
                "voids_percentage": [7.1, 5.8, 4.1, 2.3],
                "vma_percentage": [16.61, 16.47, 16.26, 15.90],
                "vfa_percentage": [57.17, 64.84, 75.55, 85.46],
                "stability": [1110, 1157, 1159, 1128],
                "flow": [2.85, 3.12, 3.35, 3.42],
                "target_voids": 4.0
            }
        }

# --- Modelos para la Salida de la API ---
# (Estos no son estrictamente necesarios para que funcione,
# pero mejoran la documentación y la predicibilidad de la respuesta)

class OptimizationResults(BaseModel):
    target_air_voids: float
    optimum_asphalt_content: float
    final_properties: Dict[str, float]

class Points(BaseModel):
    x: List[float]
    y: List[float]

class RegressionCurve(BaseModel):
    equation: str
    r2_score: float
    original_points: Points
    curve_points: Points

class MarshallOutput(BaseModel):
    """
    Modelo para la respuesta de la API.
    """
    regression_curves: Dict[str, RegressionCurve]
    optimization_results: OptimizationResults