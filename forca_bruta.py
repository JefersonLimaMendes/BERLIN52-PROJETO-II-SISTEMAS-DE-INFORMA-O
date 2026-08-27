import itertools
import math

def ler_arquivo_tsp(arquivo):
    with open("berlin8.tsp", 'r') as file:
        linhas = file.readlines()
        
    nodes = {}
    ler = False
    for linha in linhas:
        if linha.startswith("NODE_COORD_SECTION"):
            ler = True
            continue
        if ler:
            if linha.strip() == "EOF":
                break
            partes = linha.split()
            node_id = int(partes[0])
            x = float(partes[1])
            y = float(partes[2])
            nodes[node_id] = (x, y)
    
    return nodes

def dist_euclideana(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

def dist_total(route, nodes):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += dist_euclideana(nodes[route[i]], nodes[route[i+1]])
    total_distance += dist_euclideana(nodes[route[-1]], nodes[route[0]])
    return total_distance

def forca_bruta_tsp(nodes):
    cities = list(nodes.keys())
    melhor_rota = None
    min_distancia = float('inf')
    
    for permutation in itertools.permutations(cities[1:]):
        rota_atual = [cities[0]] + list(permutation)
        dist_atual = dist_total(rota_atual, nodes)
        
        if dist_atual < min_distancia:
            min_distancia = dist_atual
            melhor_rota = rota_atual
    
    return melhor_rota, min_distancia

arquivo = 'berlin52.tsp'
nodes = ler_arquivo_tsp(arquivo)
melhor_rota, min_distancia = forca_bruta_tsp(nodes)

print("Melhor rota encontrada:", melhor_rota)
print("Menor distância:", min_distancia)
