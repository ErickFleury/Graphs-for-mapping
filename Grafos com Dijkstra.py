import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Função que cria um grafo direcionado a partir de um arquivo .csv
def criar_grafo(csv):
    # Lê um arquivo .csv
    df = pd.read_csv(csv)

    # Verifica se o arquivo .csv contém as colunas necessárias
    colunas = ['Source', 'Target', 'Weight']
    if not all(col in df.columns for col in colunas):
        raise KeyError(f"Error: CSV file must contain columns: {colunas}")

    # Cria um grafo direcionado a partir do arquivo csv
    grafo = nx.DiGraph()
    for _, row in df.iterrows():
        source = row['Source']
        target = row['Target']
        weight = float(row['Weight'])
        grafo.add_edge(source, target, weight=weight)
    return grafo, df

# Função para visualizar um grafo direcionado
def visualisar_grafo(grafo, df, start_node=None, end_node=None):
    # Define a posição dos nós no gráfico (k é a constante de separação dos nós e a seed é para evitar que a posição dos nós mude a cada execução)
    pos = nx.spring_layout(grafo, k=0.3, seed=42)

    # Define o tamanho da figura
    plt.figure(figsize=(12, 8))

    # Desenha os nós
    nx.draw_networkx_nodes(grafo, pos, node_size=500, node_color="skyblue")

    # Desenha as arestas com os pesos
    edge_labels = nx.get_edge_attributes(grafo, 'weight')
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels)

    # Desenha as arestas
    nx.draw_networkx_edges(grafo, pos, alpha = 0.5)

    # Se os nós de início e fim forem fornecidos, encontra o caminho mais curto e destaca as arestas
    if start_node is not None and end_node is not None:
            shortest_path = nx.dijkstra_path(grafo, source=start_node, target=end_node, weight='weight')
            path_edges = list(zip(shortest_path, shortest_path[1:]))
            nx.draw_networkx_edges(grafo, pos, edgelist=path_edges, edge_color='red', width=3)

    nx.draw_networkx_labels(grafo, pos, font_size=12)
    plt.axis('off')
    plt.show()

# Caminho do arquivo .csv
csv = "graph_structure2.csv" 
grafo, df = criar_grafo(csv)
# Nós de início e fim para encontrar o caminho mais curto
start_node = 'Rotatoria 9'
end_node = 'Rotatoria 4'
# Visualiza o grafo com o caminho mais curto
visualisar_grafo(grafo, df, start_node, end_node)
# Visualiza o grafo sem o caminho mais curto
visualisar_grafo(grafo, df)