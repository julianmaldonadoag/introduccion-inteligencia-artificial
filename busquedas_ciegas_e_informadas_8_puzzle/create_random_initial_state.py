import random

n = 3

# Posiciones que permitiran realizar los 4 movimientos posibles para la celda vacia:
# arriba, derecha, abajo e izquierda.
row = [ -1, 0, 1, 0 ]
col = [ 0, 1, 0, -1 ]

# Imprime la matriz de nxn celdas.
def printMatrix(matrix):
    for i in range(n):
        for j in range(n):
            print((matrix[i][j]), end = ' ')
        print()

# Revisa si la posicion no supera los limites de la matriz.
def isValidPos(x, y):
    return x >= 0 and x < n and y >= 0 and y < n

# Matriz objetivo a partir de la cual se creará la matriz inicial realizando
# movimientos en la celda vacia (0).
initial_state = [[1, 2, 3 ], 
                [ 4, 5, 6 ], 
                [ 7, 8, 0 ] ]

empty_pos = [2, 2]
n_empty_pos = []

# La celda vacia (0) es movida 40 posiciones aleatorias validas.
for i in range(40):
    invalid_pos = True
    while invalid_pos:
        mov = random.randint(0, 3)
        n_empty_pos = [empty_pos[0] + row[mov], empty_pos[1] + col[mov]]
        if isValidPos(n_empty_pos[0], n_empty_pos[1]):
            invalid_pos = False

    x1 = empty_pos[0]
    y1 = empty_pos[1]
    x2 = n_empty_pos[0]
    y2 = n_empty_pos[1]

    initial_state[x1][y1], initial_state[x2][y2] = initial_state[x2][y2], initial_state[x1][y1]

    empty_pos[0] = x2
    empty_pos[1] = y2

print('Matriz inicial aleatoria:')
printMatrix(initial_state)
print(initial_state)