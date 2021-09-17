import copy # Se importa copy para utilizar la funcion deepcopy.
from collections import deque # Se utilizara para crear la cola.
import time
import tracemalloc # Se utilizara para medir la memoria ocupada.

# --------------- Variables y funciones base para el algoritmo  ---------------

# Numeros de filas y columnas.
n = 3
# Cantidad de nodos explorados tras finalizar el algoritmo (optimalidad).
n_explored_nodes = 0
# Posiciones que permitiran realizar los 4 movimientos posibles para la celda vacia (0):
# arriba, derecha, abajo e izquierda.
row = [ -1, 0, 1, 0 ]
col = [ 0, 1, 0, -1 ]

# Estructura del nodo para los algoritmos BFS y DFS.
class Node:
    def __init__(self, parent, matrix, empty_pos):
        self.parent = parent
        self.matrix = matrix
        self.empty_pos = empty_pos # Posicion de la celda vacia (0) en [fila, columna]

# Se encarga de crear un nuevo nodo. Ademas actualiza la nueva posición de la celda vacia.
def newNode(parent, matrix, empty_pos, new_empty_pos):                
    # Se copian los datos de la matriz padre a la matriz actual, sin referencia.
    new_matrix = copy.deepcopy(matrix)

    # Se obtienen las posiciones donde se encuentra la celda vacia (0)
    # tanto en la matriz padre como en la actual.
    x1 = empty_pos[0]
    y1 = empty_pos[1]
    x2 = new_empty_pos[0]
    y2 = new_empty_pos[1]
    # Se intercambia en la nueva matriz las posiciones de la celda 
    # vacia (0) en la posición correspondiente al movimiento realizado.
    new_matrix[x1][y1], new_matrix[x2][y2] = new_matrix[x2][y2], new_matrix[x1][y1]

    new_node = Node(parent, new_matrix, new_empty_pos)
    return new_node

# Imprime la matriz de nxn celdas.
def printMatrix(matrix):
    for i in range(n):
        for j in range(n):
            print((matrix[i][j]), end = ' ')
        print()

# Revisa si la posicion no supera los limites de la matriz.
def isValidPos(x, y):
    return x >= 0 and x < n and y >= 0 and y < n

# Revisa si algun nodo de la frontera contiene determinada matriz.
def frontierHasMatrix(frontier, matrix):
    for node in frontier:
        if node.matrix == matrix:
            return True
    return False

# -------------------- Algoritmo principal  --------------------

# Solución para el 8-puzzle usando BFS.
def BFS(initial_state, empty_pos, goal_state):
    global n_explored_nodes
    n_explored_nodes = 0
    # Se crea la frontera que contendra cada uno de los nodos proximos a explorar.
    frontier = deque([])

    # Se crea el nodo raiz.
    root = Node(None, initial_state, empty_pos)
    # Se añade el nodo raiz a la frontera.
    frontier.append(root)
    # Lista de matrices exploradas.
    explored = [] 

    # Mientras la frontera no este vacia.
    while frontier:
        state = frontier.popleft() # Sale el primer nodo en entrar.
        explored.append(state.matrix)
        n_explored_nodes += 1

        if (state.matrix == goal_state):
            return True

        # Se generan los posibles descendientes, para este caso el rango 
        # de descendientes es de 2 a 4 por nodo.
        for i in range(4): # 4 posibles movimientos.
            new_empty_pos = [state.empty_pos[0]+row[i], state.empty_pos[1]+col[i]]
                
            if isValidPos(new_empty_pos[0], new_empty_pos[1]):
                # Se crea el nodo hijo.
                child = newNode(state, state.matrix, state.empty_pos, new_empty_pos)
                
                if not frontierHasMatrix(frontier, child.matrix) and child.matrix not in explored:
                    frontier.append(child)

    return False

# ------------------------- 10 casos de pruebas -------------------------

# Caso 1. Ejemplo de las diapositivas.
initial_state = [[1, 0, 2 ],
                [ 4, 5, 3 ],
                [ 7, 8, 6 ] ]
empty_pos = [ 0, 1 ]
# Caso 2.
# initial_state = [[0, 1, 3  ],
#                 [ 4, 2, 8 ],
#                 [ 7, 6, 5 ] ]
# empty_pos = [ 0, 0 ]
# Caso 3.
# initial_state = [[4, 1, 2], 
#                 [ 5, 0, 8], 
#                 [ 7, 6, 3]]
# empty_pos = [ 1, 1]
# Caso 4.
# initial_state = [[2, 4, 0], 
#                 [ 1, 5, 3], 
#                 [ 7, 8, 6]]
# empty_pos = [ 0, 2 ]
# Caso 5.
# initial_state = [[1, 5, 2], 
#                 [ 7, 0, 3], 
#                 [ 8, 4, 6]]
# empty_pos = [ 1, 1 ]
# Caso 6.
# initial_state = [[2, 4, 3], 
#                 [ 1, 0, 5], 
#                 [ 7, 8, 6]]
# empty_pos = [ 1, 1 ]
# Caso 7.
# initial_state = [[4, 1, 3], 
#                 [ 7, 0, 5], 
#                 [ 8, 2, 6]]
# empty_pos = [ 1, 1 ]
# Caso 8.
# initial_state = [[2, 3, 6], 
#                 [ 5, 7, 4], 
#                 [ 0, 1, 8]]
# empty_pos = [ 2, 0 ]
# Caso 9.
# initial_state = [[0, 1, 3], 
#                 [ 4, 2, 5], 
#                 [ 7, 8, 6]]
# empty_pos = [ 0, 0 ]
# Caso 10.
# initial_state = [[1, 2, 3], 
#                 [ 4, 8, 5], 
#                 [ 0, 7, 6]]
# empty_pos = [ 2, 0]

# -------------------- Programa principal --------------------

goal_state = [  [ 1, 2, 3 ],
                [ 4, 5, 6 ],
                [ 7, 8, 0 ] ]

print('Matriz inicial:')
printMatrix(initial_state)

start_time = time.time()
tracemalloc.start()
if (BFS(initial_state, empty_pos, goal_state)):
    end_time = time.time()
    print("Objetivo encontrado aplicando BFS")
    print('Memoria [B]:', tracemalloc.get_traced_memory()[1])
    print('Tiempo [s]:', round(end_time - start_time, 5))
    print('Nodos explorados:', n_explored_nodes)
    tracemalloc.stop()
else:
    print("Objetivo NO encontrado")