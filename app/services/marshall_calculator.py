# app/services/marshall_calculator.py

import numpy as np
from sklearn.metrics import r2_score
from typing import List, Dict, Any, Tuple

# Usaremos un grado polinomial de 2, como en el script original.
POLYNOMIAL_DEGREE = 2


def _calculate_regression(
    x_values: np.ndarray, y_values: np.ndarray
) -> Tuple[np.poly1d, float, str]:
    """
    Calcula la regresión polinomial para un conjunto de datos.

    Args:
        x_values: Valores del eje X (contenido de asfalto).
        y_values: Valores del eje Y (propiedad a analizar).

    Returns:
        Una tupla con:
        - El objeto polinomio de numpy.
        - El valor de R^2.
        - La ecuación de la regresión en formato de texto.
    """
    # Ajuste de regresión polinomial.
    coeficientes = np.polyfit(x_values, y_values, POLYNOMIAL_DEGREE)
    polinomio = np.poly1d(coeficientes)

    # Cálculo de R^2.
    y_pred = polinomio(x_values)
    r2 = r2_score(y_values, y_pred)

    # Formateo de la ecuación para visualización.
    # El símbolo $ se usa para renderizado matemático en frontends como LaTeX.
    ecuacion_texto = (
        f"$y = {coeficientes[0]:.4f}x^2 "
        f"{'+' if coeficientes[1] >= 0 else ''}{coeficientes[1]:.4f}x "
        f"{'+' if coeficientes[2] >= 0 else ''}{coeficientes[2]:.4f}$"
    )

    return polinomio, r2, ecuacion_texto


def analyze_marshall_data(
    asphalt_content: List[float],
    unit_weight: List[float],
    voids_percentage: List[float],
    vma_percentage: List[float],
    vfa_percentage: List[float],
    stability: List[float],
    flow: List[float],
    target_voids: float = 4.0,
) -> Dict[str, Any]:
    """
    Analiza los datos de un ensayo Marshall para encontrar el contenido
    óptimo de asfalto.

    Args:
        asphalt_content: Lista de contenidos de asfalto (%).
        unit_weight: Lista de pesos unitarios (kg/m³).
        voids_percentage: Lista de porcentajes de vacíos (%).
        vma_percentage: Lista de vacíos en el agregado mineral (%).
        vfa_percentage: Lista de vacíos llenos con asfalto (%).
        stability: Lista de valores de estabilidad (kg).
        flow: Lista de valores de flujo (mm).
        target_voids: El porcentaje de vacíos objetivo para el diseño.

    Returns:
        Un diccionario con todos los resultados del análisis.
    """
    # Convertimos las listas de entrada a arrays de NumPy para el cálculo.
    ac_np = np.array(asphalt_content)

    data_map = {
        "peso_unitario": np.array(unit_weight),
        "porcentaje_vacios": np.array(voids_percentage),
        "vam": np.array(vma_percentage),
        "vfa": np.array(vfa_percentage),
        "estabilidad": np.array(stability),
        "flujo": np.array(flow),
    }

    results = {"regression_curves": {}}

    # 1. Calcular la regresión para cada propiedad.
    for name, y_values in data_map.items():
        polinomio, r2, ecuacion = _calculate_regression(ac_np, y_values)

        # Generar puntos para la curva de la gráfica.
        x_curve = np.linspace(ac_np.min(), ac_np.max(), 100)
        y_curve = polinomio(x_curve)

        results["regression_curves"][name] = {
            "equation": ecuacion,
            "r2_score": round(r2, 5),
            "original_points": {
                "x": asphalt_content,
                "y": y_values.tolist()
            },
            "curve_points": {
                "x": x_curve.tolist(),
                "y": y_curve.tolist()
            },
        }

    # 2. Calcular el contenido de asfalto para el % de vacíos objetivo.
    # Obtenemos el polinomio específico de la curva de vacíos.
    poly_vacios, _, _ = _calculate_regression(ac_np, data_map["porcentaje_vacios"])
    
    # Resolvemos la ecuación: ax^2 + bx + c = target_voids
    # Lo que es igual a: ax^2 + bx + (c - target_voids) = 0
    coeficientes_opt = poly_vacios.coeffs.copy()
    coeficientes_opt[-1] -= target_voids
    raices = np.roots(coeficientes_opt)

    # Filtramos las raíces para que estén en el rango de los datos originales.
    raiz_valida = [
        r for r in raices if np.isreal(r) and ac_np.min() <= r <= ac_np.max()
    ]
    
    # Si no se encuentra una raíz válida, no podemos continuar la optimización.
    if not raiz_valida:
        raise ValueError(
            "No se pudo encontrar un contenido de asfalto óptimo para el "
            f"porcentaje de vacíos objetivo de {target_voids}% dentro del "
            "rango de datos proporcionado."
        )

    optimum_asphalt_content = float(np.real(raiz_valida[0]))

    # 3. Calcular las propiedades de la mezcla en el contenido óptimo de asfalto.
    final_properties = {}
    for name, y_values in data_map.items():
        polinomio, _, _ = _calculate_regression(ac_np, y_values)
        valor_optimo = polinomio(optimum_asphalt_content)
        final_properties[name] = round(float(valor_optimo), 2)

    results["optimization_results"] = {
        "target_air_voids": target_voids,
        "optimum_asphalt_content": round(optimum_asphalt_content, 2),
        "final_properties": final_properties,
    }

    return results