import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import r2_score
from IPython.display import display, HTML

contenido_asfalto = np.array([4.5, 5.0, 5.5, 6.0])
peso_unitario = np.array([2.459, 2.476, 2.496, 2.520])
porcentaje_vacios = np.array([7.1, 5.8, 4.1, 2.3])
porcentaje_vacios_agregado_mineral = np.array([16.61, 16.47, 16.26, 15.90])
vacios_llenos_asfalto = np.array([57.17, 64.84, 74.55, 85.46])
flujo = np.array([2.85, 3.12, 3.35, 3.42])
estabilidad = np.array([1110, 1157, 1159, 1128])

# Función para ajustar y graficar regresión polinomial en una subtrama
# ax es el objeto que representa un conjunto de ejes en los que se va a dibujar un gráfico con matplotlib.
def ajustar_y_graficar(ax, x, y, titulo, grado=2):
    # Ajuste de regresión polinomial, La función np.polyfit(x, y, grado) se utiliza para encontrar los coeficientes de un polinomio que mejor se ajusta a los datos (x, y) usando el método de mínimos cuadrados.
    # np.polyfit devuelve los coeficientes en orden decreciente de los grados del polinomio.
    # La función np.poly1d(coeficientes) crea un objeto polinómico a partir de los coeficientes obtenidos anteriormente.
    coeficientes = np.polyfit(x, y, grado)
    polinomio = np.poly1d(coeficientes)

    # Generar valores para la curva ajustada, la funcion linspace nos va permitir crear 100 valores equidistantes entre el valor maximo y minimo de x
    # polinomio(x_vals) evalúa el polinomio en cada uno de los 100 valores contenidos en x_vals.
    x_vals = np.linspace(min(x), max(x), 100)
    y_ajustado = polinomio(x_vals)

    # Calcular el valor de R^2, evaluamos los valores x en el polinomio, r2_score es una función que normalmente se importa desde la biblioteca sklearn.metrics.
    #r2_score(y, y_pred) calcula el coeficiente de determinación R cuadrado entre los valores reales y y los valores predichos y_pred.
    y_pred = polinomio(x)
    r2 = r2_score(y, y_pred)

    # Creamos un string con cadena de formato texto f, El símbolo $ indica que el texto entre los dos símbolos $ será interpretado como una ecuación matematica
    # {"+" if coeficientes[1] >= 0 else ""}: Añade un signo + si el coeficiente es positivo, para mantener la notación correcta de la ecuación.
    ecuacion_texto = f'$y = {coeficientes[0]:.4f}x^2 {"+" if coeficientes[1] >= 0 else ""}{coeficientes[1]:.4f}x {"+" if coeficientes[2] >= 0 else ""}{coeficientes[2]:.4f}$\n$R^2 = {r2:.5f}$'

    # Graficar los puntos de dispersion y la curva de regresión polinomial
    ax.scatter(x, y, color='brown')
    ax.plot(x_vals, y_ajustado, color='green')

    # Mostrar la ecuación de regresión y R^2 en el gráfico usando la funcion text
    ax.text(min(x), max(y) - (max(y) - min(y)) * 0.6, ecuacion_texto, color='blue', fontsize=10)

    # Colocar el título dentro del gráfico
    ax.set_title(titulo)
    ax.grid()

# plt.subplots() es una función de matplotlib que crea una figura (fig) y una cuadrícula de subtramas (axs).
#fig es el objeto de la figura que contiene todos los subgráficos.
#axs es una matriz de objetos de los ejes (axes), cada uno representando una subtrama en la figura.
# 3,2 significa que tendremos los 6 graficos en 3 filas y 2 columnas y figsize=(15, 15) significa que nuetros figura que contendra los 6 graficos sera de 15 x 15 pulgadas
fig, axs = plt.subplots(3, 2, figsize=(15, 15))

# Llamadas a la función para cada relación, axs es una matriz de objetos de los ejes (axes), que contiene todos los subgráficos creados con plt.subplots(3, 2, ...)
# axs[0, 0] se refiere al subgráfico en la primera fila y primera columna de esa matriz (recordando que los índices empiezan desde 0).
ajustar_y_graficar(axs[0, 0], contenido_asfalto, peso_unitario, 'PESO UNITARIO')
ajustar_y_graficar(axs[0, 1], contenido_asfalto, porcentaje_vacios, 'PORCENTAJE VACIOS')
ajustar_y_graficar(axs[1, 0], contenido_asfalto, porcentaje_vacios_agregado_mineral, 'VMA')
ajustar_y_graficar(axs[1, 1], contenido_asfalto, vacios_llenos_asfalto, 'V.LL.A')
ajustar_y_graficar(axs[2, 0], contenido_asfalto, flujo, 'FLUJO')
ajustar_y_graficar(axs[2, 1], contenido_asfalto, estabilidad, 'ESTABILIDAD')

plt.show()

# Resolver la ecuación de regresión para "PORCENTAJE VACIOS" cuando y = 4
# Calcular coeficientes del polinomio y ajustar el término independiente
coeficientes = np.polyfit(contenido_asfalto, porcentaje_vacios, 2)
coeficientes[-1] = coeficientes[-1] - 4  # Ajustar el término independiente para igualar a y = 4

# Encontrar las raices usando la funcion root de numpy
raices = np.roots(coeficientes)

print(f"Las raices para x cuando y = 4 son: {raices}")

#Trabajaremos para un valor x = 5.5 que sera nuestro optimo C.A
optimo_contenido_asfalto = 5.5

# Lista de datos y nombres
datos = [
    (contenido_asfalto, peso_unitario, 'Peso Unitario'),
    (contenido_asfalto, porcentaje_vacios, 'Porcentaje Vacíos'),
    (contenido_asfalto, porcentaje_vacios_agregado_mineral, 'VMA'),
    (contenido_asfalto, vacios_llenos_asfalto, 'V. LL. A.'),
    (contenido_asfalto, flujo, 'Flujo'),
    (contenido_asfalto, estabilidad, 'Estabilidad')
]

# Crear un diccionario para almacenar los resultados
resultados = {'Contenido Asfalto (%)': [optimo_contenido_asfalto]}

# Calcular y almacenar los valores de y para x = 5.5 usando regresión polinomial
for x, y, nombre in datos:
    coeficientes = np.polyfit(x, y, 2)  # Ajuste polinomial de grado 2
    polinomio = np.poly1d(coeficientes)
    y_nuevo = polinomio(optimo_contenido_asfalto)
    resultados[nombre] = [round(y_nuevo, 4)]  # Redondear a 4 decimales

# Crear el DataFrame
df_resultados = pd.DataFrame(resultados)

# Agregar estilos CSS para centrar los valores y establecer el fondo verde claro
estilos_html = f'''
<div style="border: 2px solid black; padding: 10px; border-radius: 5px; width: fit-content;">
    <style>
        table {{
            border-collapse: collapse;
            width: 100%;


        }}
        th {{

            background-color: lightgreen;  /* Fondo verde claro solo para encabezados */
            padding: 8px;  /* Espaciado interno */
            border: 1px solid black;  /* Bordes de las celdas */
            text-align: center;
        }}
        td {{

            padding: 8px;  /* Espaciado interno */
            border: 1px solid black;  /* Bordes de las celdas */
        }}
    </style>
    {html_table}
</div>
'''

# Mostrar la tabla estilizada
display(HTML(estilos_html))