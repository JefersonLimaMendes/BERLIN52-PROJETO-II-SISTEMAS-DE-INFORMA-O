# Berlin52 - Projeto II

Projeto acadêmico de otimização de rotas para o problema do caixeiro-viajante (TSP), utilizando a instância Berlin52. O repositório reúne uma implementação de algoritmo genético, os dados das cidades e os resultados obtidos durante os testes.

## Sobre

O objetivo do projeto é encontrar uma rota de menor distância que visite todas as 52 cidades exatamente uma vez e retorne à cidade de origem. Para isso, o algoritmo representa cada rota como um cromossomo e aplica seleção, cruzamento e mutação para evoluir uma população de soluções ao longo das gerações.

A execução principal utiliza sementes aleatórias de 1 a 30, uma população inicial de 5.000 rotas e registra a melhor solução encontrada durante a evolução em `resultado_genetico.txt`.

## Funcionamento

O algoritmo genético realiza as seguintes etapas:

1. Leitura das coordenadas das 52 cidades em `berlin52.txt`.
2. Geração de uma população inicial com rotas aleatórias.
3. Cálculo da distância euclidiana de cada rota, incluindo o retorno à cidade inicial.
4. Seleção das rotas mais aptas por torneio.
5. Cruzamento entre pares de rotas para gerar novos indivíduos.
6. Aplicação de mutação nas soluções geradas.
7. Repetição do processo até que a população deixe de apresentar melhora por cinco ciclos.
8. Registro das rotas e distâncias encontradas em `resultado_genetico.txt`.

## Arquivos

- `berlin52.py`: implementação principal do algoritmo genético.
- `berlin52.txt`: coordenadas da instância Berlin52.
- `forca_bruta.py`: implementação de referência para busca exaustiva de uma rota TSP.
- `resultado_genetico.txt`: resultados registrados nos testes do algoritmo genético.

## Como executar

É necessário ter Python 3 instalado. Na pasta do projeto, execute:

```bash
python berlin52.py
```

Os novos resultados serão acrescentados ao arquivo `resultado_genetico.txt`.

> A execução da força bruta exige um arquivo no formato `.tsp` compatível com o código e, por ser uma busca exaustiva, pode apresentar custo computacional muito alto para instâncias grandes como Berlin52.

## Tecnologias

- Python 3
- Algoritmos genéticos
- Problema do caixeiro-viajante (TSP)
- Distância euclidiana
