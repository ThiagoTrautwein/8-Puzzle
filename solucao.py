from typing import Iterable, Set, Tuple
from queue import PriorityQueue, Queue, LifoQueue

class Nodo:
    """
    Implemente a classe Nodo com os atributos descritos na funcao init
    """
    def __init__(self, estado:str, pai:'Nodo', acao:str, custo:int):
        """
        Inicializa o nodo com os atributos recebidos
        :param estado:str, representacao do estado do 8-puzzle
        :param pai:Nodo, referencia ao nodo pai, (None no caso do nó raiz)
        :param acao:str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param custo:int, custo do caminho da raiz até este nó
        """
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo
    
    def __lt__(self, other):
        return self.custo < other.custo
    
    def __eq__(self, other):
        if (isinstance(other, Nodo)):
            return self.estado == other.estado and self.acao == other.acao
        return False
    def __hash__(self):
        return hash((self.estado, self.acao))
    
def sucessor(estado:str)->Set[Tuple[str,str]]:
    """
    Recebe um estado (string) e retorna um conjunto de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """
    index_void = estado.find('_')
    acoes_possiveis = []
    if (index_void + 3 < len(estado)):
        acoes_possiveis.append("abaixo")

    if (index_void - 3 >= 0):
        acoes_possiveis.append("acima")

    if (index_void % 3 == 0): #coluna da esquerda
        acoes_possiveis.append("direita")

    elif (index_void % 3 == 1): #coluna do meio
        acoes_possiveis.append("direita")
        acoes_possiveis.append("esquerda")

    else: #coluna da direita
        acoes_possiveis.append("esquerda")

    resultado = set()
    for acao in acoes_possiveis:
        estado_atingido = list(estado)
        match (acao):
            case "esquerda":
                aux = estado_atingido[index_void-1]
                estado_atingido[index_void-1] = "_"

            case "direita":
                aux = estado_atingido[index_void+1]
                estado_atingido[index_void+1] = "_"
            
            case "abaixo":
                aux = estado_atingido[index_void+3]
                estado_atingido[index_void+3] = "_"

            case "acima":
                aux = estado_atingido[index_void-3]
                estado_atingido[index_void-3] = "_"

        estado_atingido[index_void] = aux
        resultado.add((acao, ''.join(estado_atingido)))

    return resultado
                
def expande(nodo:Nodo)->Set[Nodo]:
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um conjunto de nodos.
    Cada nodo do conjunto é contém um estado sucessor do nó recebido.
    :param nodo: objeto da classe Nodo
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    nodos_expandidos = []
    for succ in sucessor(nodo.estado):
        acao, estado_atingido = succ
        filho = Nodo(estado_atingido, nodo, acao, nodo.custo+1)
        nodos_expandidos.append(filho)

    return nodos_expandidos

def calcula_hamming(estado:str):
    count = 0
    for i, num in enumerate(list(estado)):
        if (num != '_'):
            if (i + 1 != int(num)):
                count +=1 
        else:
            if (i != len(estado) - 1):
                count += 1
    
    return count

def calcula_manhattan(estado: str) -> int:
    """
    Calcula a distância de Manhattan para um estado do 8-puzzle.
    :param estado: str, representacao do estado do 8-puzzle
    :return: int, distância de Manhattan
    """
    objetivo = '12345678_'
    distancia_total = 0

    for i, valor in enumerate(estado):
        if valor != '_':
            pos_objetivo = objetivo.index(valor)
            distancia_total += abs(i // 3 - pos_objetivo // 3) + abs(i % 3 - pos_objetivo % 3)

    return distancia_total

def astar_hamming(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    objetivo = "12345678_"

    fronteira = PriorityQueue()
    nodo = Nodo(estado, None, None, 0)
    custo = calcula_hamming(estado)

    fronteira.put((custo, nodo))

    explorados = set()
    custo_total = 0
    nodos_expandidos = 0
    while not fronteira.empty():
        custo, v = fronteira.get()
        if (v.estado == objetivo):
            caminho = []
            while v.pai is not None:
                caminho.append(v.acao)
                custo_total += v.custo
                v = v.pai
            caminho.reverse()
            #print(f'Nodos Expandidos:{nodos_expandidos} - Custo Total:{custo_total}')
            return caminho
        
        if (v.estado not in explorados):
            explorados.add(v.estado)
            sucessores = expande(v)
            nodos_expandidos += 1
            for succ in sucessores:
                if (succ.estado not in explorados):
                    novo_custo = succ.custo + calcula_hamming(succ.estado)
                    fronteira.put((novo_custo, succ))
    #print(f'Solução Não Encontrada - Nodos Expandidos:{nodos_expandidos}')
    return None

def astar_manhattan(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    objetivo = "12345678_"

    if not eh_soluvel(estado):
        return None

    fronteira = PriorityQueue()
    nodo = Nodo(estado, None, None, 0)
    custo = calcula_manhattan(estado)

    fronteira.put((custo, nodo))

    explorados = []
    custo_total = 0
    nodos_expandidos = 0
    while not fronteira.empty():
        custo, v = fronteira.get()
        if (v.estado == objetivo):
            caminho = []
            while v.pai is not None:
                caminho.append(v.acao)
                custo_total += v.custo
                v = v.pai
            caminho.reverse()
            #print(f'Nodos Expandidos:{nodos_expandidos} - Custo Total:{custo_total}')
            return caminho
        
        if (v.estado not in explorados):
            explorados.append(v.estado)
            sucessores = expande(v)
            nodos_expandidos += 1
            for succ in sucessores:
                if (succ.estado not in explorados):
                    novo_custo = succ.custo + calcula_manhattan(succ.estado)
                    fronteira.put((novo_custo, succ))
    #print(f'Solução Não Encontrada - Nodos Expandidos:{nodos_expandidos}')
    return None

#opcional,extra
def bfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em LARGURA e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    objetivo = "12345678_"

    fronteira = Queue()
    nodo = Nodo(estado, None, None, 0)

    fronteira.put(nodo)

    explorados = set()
    nodos_expandidos = 0
    while not fronteira.empty():
        v = fronteira.get()
        if (v.estado == objetivo):
            caminho = []
            while v.pai is not None:
                caminho.append(v.acao)
                v = v.pai
            caminho.reverse()
            #print(f'Nodos Expandidos:{nodos_expandidos}')
            return caminho
        
        if (v.estado not in explorados):
            explorados.add(v.estado)
            sucessores = expande(v)
            nodos_expandidos += 1
            for succ in sucessores:
                if (succ.estado not in explorados):
                    fronteira.put(succ)
    #print(f'Solução Não Encontrada - Nodos Expandidos:{nodos_expandidos}')
    return None

#opcional,extra
def dfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    objetivo = "12345678_"

    fronteira = LifoQueue()
    nodo = Nodo(estado, None, None, 0)

    fronteira.put(nodo)

    explorados = set()
    nodos_expandidos = 0
    while not fronteira.empty():
        v = fronteira.get()
        if (v.estado == objetivo):
            caminho = []
            while v.pai is not None:
                caminho.append(v.acao)
                v = v.pai
            caminho.reverse()
            #print(f'Nodos Expandidos:{nodos_expandidos}')
            return caminho
        
        if (v.estado not in explorados):
            explorados.add(v.estado)
            sucessores = expande(v)
            nodos_expandidos += 1
            for succ in sucessores:
                if (succ.estado not in explorados):
                    fronteira.put(succ)
    #print(f'Solução Não Encontrada - Nodos Expandidos:{nodos_expandidos}')
    return None

#opcional,extra
def astar_new_heuristic(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = sua nova heurística e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError

def conta_inversoes(estado):
    # Função para contar o número de inversões no estado
    inversoes = 0
    elementos = [e for e in estado if e != '_']
    for i in range(len(elementos)):
        for j in range(i + 1, len(elementos)):
            if elementos[i] > elementos[j]:
                inversoes += 1
    return inversoes

def eh_soluvel(estado):
    # Um estado é solúvel se o número de inversões for par
    return conta_inversoes(estado) % 2 == 0

if __name__ == "__main__":
    estado = "185423_67"
    astar_hamming(estado)
