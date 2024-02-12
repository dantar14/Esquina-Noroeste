import numpy as np
from tabulate import tabulate
num_fabricas = int(input("Ingrese número de fábricas: "))
num_destinos = int(input("Ingrese número de destinos: "))
oferta = []
for i in range(num_fabricas):
    oferta_i = int(input(f"Ingrese oferta de la fábrica {i}: "))
    oferta.append(oferta_i)
demanda = []
for j in range(num_destinos):
    demanda_j = int(input(f"Ingrese demanda del destino {j}: "))
    demanda.append(demanda_j)
celdas_basicas = np.zeros((num_fabricas, num_destinos))
i = 0
j = 0
while i < num_fabricas and j < num_destinos:
    cantidad = min(oferta[i], demanda[j])
    celdas_basicas[i][j] = cantidad
    oferta[i] -= cantidad
    demanda[j] -= cantidad
    if oferta[i] == 0:
        i += 1
    if demanda[j] == 0:
        j += 1
u = np.zeros(num_fabricas)
v = np.zeros(num_destinos)
while True:
    c = np.zeros((num_fabricas, num_destinos))
    for i in range(num_fabricas):
        for j in range(num_destinos):
            if celdas_basicas[i][j] == 0:
                c[i][j] = -u[i] - v[j]
    fila, columna = np.unravel_index(c.argmax(), c.shape)
    if c[fila][columna] <= 0:
        break
    celdas_visibles = np.zeros((num_fabricas, num_destinos), dtype=bool)
    celdas_visibles[fila][columna] = True
    celdas_visitadas = np.zeros((num_fabricas, num_destinos), dtype=bool)
    celdas_visitadas[fila][columna] = True
    while True:
        celdas_no_visitadas = np.logical_and(celdas_visibles, np.logical_not(celdas_visitadas))
        indices_no_visitados = np.where(celdas_no_visitadas)
        i, j = indices_no_visitados[0][0], indices_no_visitados[1][0]
        celdas_visitadas[i][j] = True
        filas_visitadas = np.any(celdas_visitadas, axis=1)
        columnas_visitadas = np.any(celdas_visitadas, axis=0)
        u[filas_visitadas] = u[filas_visitadas] + c[i][columnas_visitadas] - v[columnas_visitadas]
        v[columnas_visitadas] = v[columnas_visitadas] - c[filas_visitadas][j] + u[filas_visitadas]
        celdas_visibles[i][j] = True
        if not np.any(np.logical_and(celdas_no_visitadas, np.logical_not(celdas_visibles))):
            break
    delta = min(oferta[i], demanda[j])
    celdas_basicas[i][j] += delta
    oferta[i] -= delta
    demanda[j] -= delta
tabla_resultados = []
for i in range(num_fabricas):
    fila = []
    for j in range(num_destinos):
        fila.append(celdas_basicas[i][j])
    tabla_resultados.append(fila + [oferta[i]])
tabla_resultados.append(demanda + [sum(oferta)])
headers = [f"Destino {j}" for j in range(num_destinos)] + ["Oferta"]
tabla_resultados.insert(0, headers)
print(tabulate(tabla_resultados, headers="firstrow", tablefmt="grid"))
costo_total = 0
for i in range(num_fabricas):
    for j in range(num_destinos):
        costo_total += celdas_basicas[i][j] * int(input(f"Ingrese costo de transporte de unidad desde la fábrica {i} al destino {j}: "))
print(f"El costo total es: {costo_total}")