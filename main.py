import numpy as np
import matplotlib.pyplot as plt

# Definimos los estados
estados = ["Soleado", "Nublado", "Lluvioso"]

# Función para generar una matriz de transición aleatoria
def generar_matriz_transicion_aleatoria(estados):
    num_estados = len(estados)
    matriz_transicion = np.zeros((num_estados, num_estados))
    for i in range(num_estados):
        random_probs = np.random.rand(num_estados)
        matriz_transicion[i] = random_probs / random_probs.sum()  # Normalizar para que sumen a 1
    return matriz_transicion

# Función para realizar una simulación del modelo de Markov
def simulacion_markov(estado_inicial, matriz_transicion, estados, num_dias):
    estado_actual = estado_inicial
    historial_estados = [estado_actual]
    
    for _ in range(num_dias - 1):
        estado_actual = np.random.choice(estados, p=matriz_transicion[estados.index(estado_actual)])
        historial_estados.append(estado_actual)
    
    return historial_estados

# Función para realizar múltiples simulaciones
def multiples_simulaciones(num_simulaciones, estados, num_dias, distribucion_inicial=None):
    resultados = []
    for _ in range(num_simulaciones):
        # Selección de estado inicial basado en una distribución inicial si está definida
        if distribucion_inicial:
            estado_inicial = np.random.choice(estados, p=distribucion_inicial)
        else:
            estado_inicial = np.random.choice(estados)  # Estado inicial aleatorio
        matriz_transicion = generar_matriz_transicion_aleatoria(estados)  # Matriz de transición aleatoria
        resultados.append(simulacion_markov(estado_inicial, matriz_transicion, estados, num_dias))
    return resultados

# Configuración de la distribución inicial (opcional)
distribucion_inicial = [0.5, 0.3, 0.2]  # 50% Soleado, 30% Nublado, 20% Lluvioso

# Ejecutamos múltiples simulaciones
num_simulaciones = 100000
num_dias = 30
resultados_simulaciones = multiples_simulaciones(num_simulaciones, estados, num_dias, distribucion_inicial)

# Contamos la frecuencia de cada estado en todos los días simulados
frecuencia_estados = {estado: 0 for estado in estados}

for simulacion in resultados_simulaciones:
    for estado in simulacion:
        frecuencia_estados[estado] += 1

# Convertimos frecuencias a porcentajes
total_estados = sum(frecuencia_estados.values())
porcentaje_estados = {estado: (frecuencia / total_estados) * 100 for estado, frecuencia in frecuencia_estados.items()}

# Generamos el histograma
plt.figure(figsize=(10, 6))
plt.bar(porcentaje_estados.keys(), porcentaje_estados.values())
plt.xlabel('Estados')
plt.ylabel('Porcentaje (%)')
plt.title('Porcentaje de Estados en Simulaciones de Modelo de Markov')
plt.show()

# Gráfico de líneas de una simulación específica
simulacion_especifica = resultados_simulaciones[0]

plt.figure(figsize=(10, 6))
plt.plot(range(num_dias), simulacion_especifica, marker='o')
plt.xlabel('Día')
plt.ylabel('Estado')
plt.title('Evolución del Estado en una Simulación Específica')
plt.yticks(ticks=range(len(estados)), labels=estados)
plt.grid(True)
plt.show()

# Gráfico de barras acumulativas para cada día a lo largo de todas las simulaciones
conteo_diario = {estado: np.zeros(num_dias) for estado in estados}

for simulacion in resultados_simulaciones:
    for dia, estado in enumerate(simulacion):
        conteo_diario[estado][dia] += 1

# Convertimos conteo diario a porcentajes
porcentaje_diario = {estado: (conteo / num_simulaciones) * 100 for estado, conteo in conteo_diario.items()}

# Generar gráfico de barras acumulativas
fig, ax = plt.subplots(figsize=(10, 6))
bottom = np.zeros(num_dias)
for estado in estados:
    ax.bar(range(num_dias), porcentaje_diario[estado], bottom=bottom, label=estado)
    bottom += porcentaje_diario[estado]

ax.set_xlabel('Día')
ax.set_ylabel('Porcentaje (%)')
ax.set_title('Distribución de Estados por Día a lo Largo de Todas las Simulaciones')
ax.legend()
plt.show()
