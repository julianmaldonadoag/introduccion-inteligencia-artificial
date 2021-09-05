import pygame
import numpy as np
import time

# ---------- Funciones ----------

# Imprime el ambiente dibujando cada una de las celdas en base a su estado.
def printEnviroment(screen):
    screen.fill(BG_COLOR)

    for x in range(nX):
        for y in range(nY):
            # Se crea el cuadrado de cada celda a dibujar.
            square = [(x * xSize,   y * ySize),
                    ((x+1) * xSize, y * ySize),
                    ((x+1) * xSize, (y+1) * ySize),
                    (x * xSize,     (y+1) * ySize)]
            if envState[x, y] == 0:
                pygame.draw.polygon(screen, FREE_CELL_COLOR, square, 1)
            elif envState[x, y] == 1:
                pygame.draw.polygon(screen, OCCUPIED_CELL_COLOR, square, 0)
            elif envState[x, y] == 2:
                pygame.draw.polygon(screen, AGENT_COLOR, square, 0)
    pygame.display.flip() # Muestra la cuadricula

# Calcula el valor del TLU (Threshold Logic Units).
def TLU(S, w, threshold):
    sum = np.sum(S * w)
    print('Sum: ', sum)
    return 1 if (sum >= threshold) else 0

# Actualiza la posición del agente en 'x' o 'y' y actualiza
# el estado de su posicion actual asi como de la nueva posición.
def moveAgent(envState, direction):
    global xAgentPos
    global yAgentPos

    if (direction == "north"):
        envState[xAgentPos, yAgentPos] = 0
        envState[xAgentPos, yAgentPos - 1] = 2
        printEnviroment(screen)
        yAgentPos -= 1
    elif (direction == "east"):
        envState[xAgentPos, yAgentPos] = 0
        envState[xAgentPos + 1, yAgentPos] = 2
        printEnviroment(screen)
        xAgentPos += 1
    elif (direction == "south"):
        envState[xAgentPos, yAgentPos] = 0
        envState[xAgentPos, yAgentPos + 1] = 2
        printEnviroment(screen)
        yAgentPos += 1
    elif (direction == "west"):
        envState[xAgentPos, yAgentPos] = 0
        envState[xAgentPos - 1, yAgentPos] = 2
        printEnviroment(screen)
        xAgentPos -= 1

# Dado un arreglo de señales, muta el arreglo asignando la señal
# percibida de las posiciones vecinas del agente.
def storeSignals(signals):
    signals[0] = envState[xAgentPos-1,  yAgentPos-1] # s1
    signals[1] = envState[xAgentPos,    yAgentPos-1] # s2
    signals[2] = envState[xAgentPos+1,  yAgentPos-1] # s3
    signals[3] = envState[xAgentPos+1,  yAgentPos]   # s4
    signals[4] = envState[xAgentPos+1,  yAgentPos+1] # s5
    signals[5] = envState[xAgentPos,    yAgentPos+1] # s6
    signals[6] = envState[xAgentPos-1,  yAgentPos+1] # s7
    signals[7] = envState[xAgentPos-1,  yAgentPos]   # s8

# ---------- Constantes y variables globales ----------

BG_COLOR = (255, 255, 255)
OCCUPIED_CELL_COLOR = (0, 0, 0)
FREE_CELL_COLOR = (200, 200, 200) # Color del contorno de una celda libre.
AGENT_COLOR = (255, 0, 0)

# Graficamente 'x' representa las columnas (izquierda a derecha) y 'y' las filas (arriba a abajo).
width, height = 800, 800 # Ancho y alto de la pantalla.
nX, nY = 16, 16 # Numero de columnas y filas.
xSize = width / nX
ySize = height / nY

# Estado de las celdas del ambiente. Ocupada = 1, libre = 0, agente = 2
envState = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
])
envState = np.transpose(envState)

# ---------- Programa principal ----------

# Agente 1: evita obstáculos. Agente 2: recorre bordes.
agentNumber = 1

# Para el agente que recorre bordes la siguiente posicion hara que el agente
# recorra el borde la parte interna del limite de manera horaria.
xAgentPos = 6
yAgentPos = 2
# Para el agente que recorre bordes la siguiente posicion hara que el agente
# recorra el borde del obstaculo central de manera antihoraria.
# xAgentPos = 4
# yAgentPos = 9

# Se indica donde se encuentra el agente.
envState[xAgentPos, yAgentPos] = 2

pygame.init()
screen = pygame.display.set_mode([height, width])
printEnviroment(screen)
windowIsOpen = True

while windowIsOpen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            windowIsOpen = False
            continue

    # Tiempo de espera para la siguiente acción.
    time.sleep(1)
    print("--- Nueva iteración ---")

    signals = np.zeros(8)
    storeSignals(signals)

    if (agentNumber == 1):
        threshold = 0
        print("Umbral a igualar o superar: ", threshold)
        # not s2 entonces norte
        w1 = np.array([0, -1, 0, 0, 0, 0, 0, 0])
        if (TLU(signals, w1, threshold)):
            moveAgent(envState, "north")
            continue
        # not s4 entonces este
        w2 = np.array([0, 0, 0, -1, 0, 0, 0, 0])
        if (TLU(signals, w2, threshold)):
            moveAgent(envState, "east")
            continue
        # not s6 entonces sur
        w3 = np.array([0, 0, 0, 0, 0, -1, 0, 0])
        if (TLU(signals, w3, threshold)):
            moveAgent(envState, "south")
            continue
        # not s8 entonces oeste
        w4 = np.array([0, 0, 0, 0, 0, 0, 0, -1])
        if (TLU(signals, w4, threshold)):
            moveAgent(envState, "west")
            continue
        
    elif (agentNumber == 2):
        threshold = 0.5
        print("Umbral a igualar o superar: ", threshold)
        # x1 y not x2 entonces este
        w1 = np.array([0, 1, 1, -2, -2, 0, 0, 0])
        if (TLU(signals, w1, threshold)):
            moveAgent(envState, "east")
            continue
        # x2 y not x3 entonces sur
        w2 = np.array([0, 0, 0, 1, 1, -2, -2, 0])
        if (TLU(signals, w2, threshold)):
            moveAgent(envState, "south")
            continue
        # x3 y not x4 entonces oeste
        w3 = np.array([-2, 0, 0, 0, 0, 1, 1, -2])
        if (TLU(signals, w3, threshold)):
            moveAgent(envState, "west")
            continue 
        # x4 y not x1 entonces norte
        w4 = np.array([1, -2, -2, 0, 0, 0, 0, 1])
        if (TLU(signals, w4, threshold)):
            moveAgent(envState, "north")
            continue
        if (1):
            moveAgent(envState, "north")
            continue 

pygame.quit()
