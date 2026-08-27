""""berlin52_code"""
import random
import copy
import time

def achando_posiçoes():
    """ Cria um dicionário de listas com as coordenadas de cada ponto
    Exemplo: 1:[0,10] """
    
   # Linhas abaixo abrem o arquivo transfomando cada linha em um elemento de uma lista,
   # excluindo o cabeçalho.

    arq = open('berlin52.txt',"r+")
    lista_arq = arq.readlines()
    lista_arq = lista_arq[6:]
    posiçoes = {}

    # laço responsável por limpar as linhas r preencher o dicionário 'posiçoes',
    # com exceção do último, que não tem '\n'.

    for i in range( len(lista_arq) - 1):

        lista = lista_arq[i].split(" ")

        lista[2] = lista[2][0:len(lista[2]) - 1]

        lista = [float(i) for i in lista]

        chave = lista[0]

        lista = lista[1:]

        posiçoes[chave] = lista
    
    # inserem o último elemento no dicionário

    lista = [float(i) for i in lista_arq[len(lista_arq)-1].split(" ")]
    chave = lista[0]
    lista = lista[1:]
    posiçoes[float(chave)] = lista
    
    #função retorna o arquivo e o número de pontos

    arq.close
    n_pontos = len(lista_arq)

    return posiçoes, n_pontos

def caminho_entre(pos_1, pos_2):

    """Função que descobre a distância entre dois pontos"""

    x_1, y_1 = pos_1[0], pos_1[1]
    x_2, y_2 = pos_2[0], pos_2[1]

    diferença_x = abs(x_1 - x_2)
    diferença_y = abs(y_1 - y_2)

    distancia = (diferença_x**2) + (diferença_y**2)
    distancia = distancia**(1/2)
    
    return distancia

def pop_inicial(n_populaçao, n_pontos):

    index = [i for i in range(1, n_pontos + 1)]
    lista = [None] * len(index)
    embaralhado = [None] * (n_populaçao)
    n = len(index) - 1
    count = 0

    while embaralhado[len(embaralhado) - 1] == None:
        a = 0
        while n != -1:
            x =  random.randint(0,n)
            lista[a] = index[x]
            index[x], index[n] = index[n], index[x]
            a+=1
            n-= 1
        embaralhado[count] = lista.copy()
        n = len(index) - 1
        count +=1
    
    return embaralhado

def soma_caminho(caminho,coordenadas):
    soma = 0
    for i in range( len(caminho) - 1):
       soma+= caminho_entre(coordenadas[caminho[i]], coordenadas[caminho[i + 1]])

    soma+= caminho_entre(coordenadas[caminho[len(caminho) - 1]], coordenadas[caminho[0]])
    return caminho, soma

def selecionando(coordenadas,populaçao):

    n = len(populaçao)
    most_fit = [None] * n
    for i in range(n):
        x = random.randint(0,len(populaçao) -2)
        
        caminho_1, distancia_1 = soma_caminho(populaçao[x], coordenadas)
        caminho_2, distancia_2 = soma_caminho(populaçao[x+1], coordenadas)
        
        if distancia_1 < distancia_2:
            most_fit[i] =  caminho_1
        else:
            most_fit[i] = caminho_2
    
    return most_fit

def escolher_pontos_de_corte(tamanho):
    ponto_corte_1 = random.randint(1, tamanho // 2)
    ponto_corte_2 = random.randint(tamanho // 2 + 1, tamanho - 1)
    
    if ponto_corte_1 > ponto_corte_2:
        ponto_corte_1, ponto_corte_2 = ponto_corte_2, ponto_corte_1
    
    return ponto_corte_1, ponto_corte_2

def copiar_subsecoes(pai, ponto_corte_1, ponto_corte_2):
    filho = [None] * int(len(pai))
    filho[ponto_corte_1:ponto_corte_2] = pai[ponto_corte_1:ponto_corte_2]
    return filho

def preencher_filho(filho, pai, ponto_corte_2):
    tamanho = len(filho)
    pos = ponto_corte_2
    for gene in pai:
        if gene not in filho:
            if pos >= tamanho:
                pos = 0
            filho[pos] = gene
            pos += 1
    return filho

def cruzamento(pai_1, pai_2):
    tamanho = int(len(pai_1))
    
    # Escolher pontos de corte
    ponto_corte_1, ponto_corte_2 = escolher_pontos_de_corte(tamanho)
    
    # Criar filhos com as subseções copiadas
    filho_1 = copiar_subsecoes(pai_1, ponto_corte_1, ponto_corte_2)
    filho_2 = copiar_subsecoes(pai_2, ponto_corte_1, ponto_corte_2)
    
    # Preencher o restante dos filhos
    filho_1 = preencher_filho(filho_1, pai_2, ponto_corte_2)
    filho_2 = preencher_filho(filho_2, pai_1, ponto_corte_2)

    #filho_1[1] = filho_1[len(filho_1) - 1]
    #filho_2[1] = filho_2[len(filho_2) - 1]

    return filho_1, filho_2

def mutaçao(filho_1, filho_2):

    filhos = [filho_1, filho_2]

    for i in range(len(filhos)):
       chance = random.randint(1,100)
       if chance < 1:
           ponto_mutacao = random.randint(0, len(filhos[i]) - 1)
           primeira_parte = filhos[i][:ponto_mutacao]
           filhos[i][:len(filhos[i]) - ponto_mutacao] = filhos[i][ponto_mutacao:]
           filhos[i][len(filhos[i]) - ponto_mutacao:] = primeira_parte

    return filhos[0], filhos[1]
    
def crossover(pais):
    
    nova_populaçao = [None] * (len(pais))

    k = 0

    for i in range(1, len(pais), 2):
        
        #filho_1, filho_2 = cruzamento(pais[i][:len(pais[i]) -1],pais[i-1][:len(pais[i-1]) -1])
        
        filho_1, filho_2 = cruzamento(pais[i],pais[i-1])
        
        filho_1, filho_2 = mutaçao(filho_1, filho_2)

        nova_populaçao[i], nova_populaçao[i-1] = filho_1, filho_2

    return nova_populaçao

def melhor_caminho(coordenadas,populaçao):
    
    menor_caminho, d_menor = soma_caminho(populaçao[0], coordenadas)

    for novo_caminho in populaçao[1:]:
        caminho, distancia = soma_caminho(novo_caminho, coordenadas)
        if distancia < d_menor:
            menor_caminho = caminho
            d_menor = distancia
    
    menor_caminho.append(menor_caminho[0])

    return menor_caminho, d_menor

def guardando_resultado(caminho, distancia, n_geraçao):

    with open("resultado_genetico.txt", "a") as arq:

        arq.write("\n")
        arq.write("Geracao numero: " + str(n_geraçao) )
        arq.write("\n")
        for i in range(len(caminho)):
            arq.write(str(caminho[i]))
            if i < len(caminho) - 1:
                arq.write("/")
        
        arq.write("\n")
        
        arq.write(str(distancia))
        arq.write("\n")

def verificar(continuar,novo_menor, menor_anterior, coordenadas):

    menor_anterior, distancia = soma_caminho(menor_anterior, coordenadas)

    if distancia <= novo_menor:
        return continuar+1
    
    return 0

def evoluçao(distancias,populaçao, n_geraçoes = 10000):
    
    continuar = 0

    while continuar < 5: #n_geraçoes < 50:

        lista_pais = selecionando(distancias, populaçao)
        filhos = crossover(lista_pais)

        if n_geraçoes%5 == 0:

            mais_curto, menor_d = melhor_caminho(distancias, populaçao)
            guardando_resultado(mais_curto, menor_d, n_geraçoes)
            continuar = verificar(continuar, menor_d, populaçao[0],distancias)
        
        populaçao = filhos
        populaçao[1000] = mais_curto[:len(mais_curto)-1]
        n_geraçoes+=1
        
    else:
        #mais_curto, menor_d = melhor_caminho(distancias, populaçao)
        #mais_curto.append(mais_curto[0])
        return mais_curto, menor_d
    

def mais_proximo():

    with open("resultado_guloso.txt","r+") as arq:

        lista_arq = arq.readlines()
        populaçao = [None] * (len(lista_arq)//2)
        j = 0

        for i in range(0,len(lista_arq),2):
            caminho = lista_arq[i].split("/")
            caminho = caminho[0:len(caminho)-1]
            caminho = [float(i) for i in caminho]
            populaçao[j] = caminho
            j+=1
        
    return populaçao

def main_genetico(teste):
    
    inicio = time.time()

    random.seed(teste)
    coordenadas, n_pontos = achando_posiçoes()
    n_populaçao = 5000
    populaçao = pop_inicial(n_populaçao, n_pontos)
    #pop_prox = mais_proximo()
    #populaçao += pop_prox

    with open("resultado_genetico.txt", "a") as arq:
        arq.write("numero do teste: " + str(teste))
        arq.write("\n")
        arq.write("numero da seed: " + str(teste))
        arq.write("\n")
    
    evoluçao(coordenadas, populaçao)
    fim = time.time()

    total = fim - inicio
    with open("resultado_genetico.txt", "a") as arq:
        arq.write("Tempo de execucao do teste: " + str(total))
        arq.write("\n")
        arq.write("===========================================")
        arq.write('\n')

if __name__ == "__main__":

    with open("resultado_genetico.txt", "w") as arq:
        arq.write("Resultados do algoritmo genetico aplicado ao TSP Berlin52: ")
        arq.write("\n")

    for i in range(1,31):
        main_genetico(i)
#main_genetico()

# pesquisar três trabalhos, artigos, no caps, sobre o TSP(caixeiro-viajante)