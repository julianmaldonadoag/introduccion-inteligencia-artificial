'''
Author: Julian Maldonado.
Description: 
    Agrupamiento y ordenamiento de objetos de diferentes tipos (3) basado en el comportamiento 
    de las hormigas, ademas se hace uso de una memoria para la cantidad de objetos percibidos 
    por el agente para los ultimos T pasos. 
'''

import pygame
import sys
import numpy as np
import random
import time
import winsound
from Agent import *
from Corpse import *
from Environment import *

def main():
    # Parametros establecidos.
    width, height = 200, 200 # Numero de columnas y filas.
    num_objects = 5000
    num_agents = 10
    k1 = 0.1
    k2 = 0.3
    T = 50
    t = 0
    t_max = 5000000

    # Estado de las celdas del ambiente representada como una matriz (cuadricula).
    # Celda con objeto = objeto Corpse, celda libre = None
    initial_grid = np.full((width, height), None)
    # Se crean y ubican los objetos (Corpse) aleatorimente.
    for i in range(num_objects):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        while initial_grid[x, y] != None:
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
        # De manera equitativa se divide la cantidad de objetos para los 3 diferentes tipos.
        if i < 1666:
            initial_grid[x, y] = Corpse(x, y, 'a')
        elif i < 3333:
            initial_grid[x, y] = Corpse(x, y, 'b')
        else:
            initial_grid[x, y] = Corpse(x, y, 'c')
    # Se crean y ubican aleatoriamente los agentes.
    agents = []
    for _ in range(num_agents):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        agents.append(Agent(x, y))
    # Se crea el ambiente.
    env = Environment(initial_grid, agents, width, height)

    # Se configura e inicializa la interfaz grafica.
    pygame.init()
    pygame.display.set_caption('Ant clustering and sorting')
    screen = pygame.display.set_mode((width, height))

    # Bucle principal.
    while (t <= t_max):
        # Control del cierre de la ventana grafica.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Reimpresion de la pantalla cada 50,000 pasos.
        if (t % 50000 == 0):
            print('t = ', t)
            env.printEnviroment(screen)
        # Valores de "t" a capturar.
        if (t == 0 or t == 50000 or t == 1000000 or t == 5000000):
            print('Take the screenshot!')
            winsound.Beep(1500, 200)
            time.sleep(10)

        env.step(k1, k2, T)
        t += 1

if __name__ == "__main__":
    main()
