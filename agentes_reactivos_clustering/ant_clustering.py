'''
Author: Julian Maldonado.
Description: Clusterización de objetos basado en el comportamiento de las hormigas.
'''

import pygame
import sys
import numpy as np
import random
import time
import winsound

class Corpse:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def probPickup(k1, f) -> float:
        '''Probabilidad de que un objecto (Corpse) sea recogido por algún agente.'''
        return ( (k1 / (k1+f))**2 )

    @staticmethod
    def probDeposit(k2, f) -> float:
        '''
        Probabilidad de que algún agente que esta cargando un objeto (Corpse)
        deposite al objeto en una celda vacia
        '''
        return ( (f / (k2+f))**2 )

class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.loaded = False # ¿Esta cargando un objeto?
        self.object = None # Objeto que podria a cargar, de tipo Corpse.

    def move(self) -> None:
        '''
        El agente se mueve una posición (valida) de las 8 posibles celdas
        vecinas de manera aleatoria.
        '''
        invalid_position = True
        while (invalid_position):
            new_pos = random.randint(1, 8)
            if new_pos == 1 and Environment.validPosition(self.x - 1, self.y - 1):
                self.x = self.x - 1
                self.y = self.y - 1
                invalid_position = False
            elif new_pos == 2 and Environment.validPosition(self.x, self.y - 1):
                self.y = self.y - 1
                invalid_position = False
            elif new_pos == 3 and Environment.validPosition(self.x + 1, self.y - 1):
                self.x = self.x + 1
                self.y = self.y - 1
                invalid_position = False
            elif new_pos == 4 and Environment.validPosition(self.x + 1, self.y):
                self.x = self.x + 1
                invalid_position = False
            elif new_pos == 5 and Environment.validPosition(self.x + 1, self.y + 1):
                self.x = self.x + 1
                self.y = self.y + 1
                invalid_position = False
            elif new_pos == 6 and Environment.validPosition(self.x, self.y + 1):
                self.y = self.y + 1
                invalid_position = False
            elif new_pos == 7 and Environment.validPosition(self.x - 1, self.y + 1):
                self.x = self.x - 1
                self.y = self.y + 1
                invalid_position = False
            elif new_pos == 8 and Environment.validPosition(self.x - 1, self.y):
                self.x = self.x - 1
                invalid_position = False

class Environment:
    x_max = 200
    y_max = 200

    def __init__(self, state, agents, width, height):
        self.state = state # Array bidimensional donde se almacenan los objetos Corpse.
        self.agents = agents # Lista de objetos Agent.
        self.width = width
        self.height = height
        self.bg_color = (255, 255, 255) # Color del fondo.
        self.object_cell_color = (0, 0, 0) # Color de la celda que tiene un objeto.

    def printEnviroment(self, screen) -> None:
        '''Imprime el ambiente del estado actual.'''
        # Nota: Graficamente 'x' representa las columnas (izquierda a derecha) 
        # mientras que 'y' las filas (arriba a abajo).
        screen.fill(self.bg_color)

        # Por cada objeto Corpse que se encuentre en la matriz se pinta un pixel.
        for x in range(self.width):
            for y in range(self.height):
                if self.state[x, y]:
                    screen.set_at((x, y), self.object_cell_color)
        pygame.display.flip() # Muestra la cuadricula

    def fractionObjects(self, agent) -> float:
        '''
        Le permite a un agente percibir la fracción de objetos que se encuentran a su alrededor.
        '''
        count = 0
        if Environment.validPosition(agent.x-1,  agent.y-1) and self.state[agent.x-1,  agent.y-1]:
            count += 1
        if Environment.validPosition(agent.x,    agent.y-1) and self.state[agent.x,    agent.y-1]:
            count += 1
        if Environment.validPosition(agent.x+1,  agent.y-1) and self.state[agent.x+1,  agent.y-1]:
            count += 1
        if Environment.validPosition(agent.x+1,  agent.y  ) and self.state[agent.x+1,  agent.y  ]:
            count += 1
        if Environment.validPosition(agent.x+1,  agent.y+1) and self.state[agent.x+1,  agent.y+1]:
            count += 1
        if Environment.validPosition(agent.x,    agent.y+1) and self.state[agent.x,    agent.y+1]:
            count += 1
        if Environment.validPosition(agent.x-1,  agent.y+1) and self.state[agent.x-1,  agent.y+1]:
            count += 1
        if Environment.validPosition(agent.x-1,  agent.y  ) and self.state[agent.x-1,  agent.y  ]:
            count += 1
        return count / 8

    def step(self, k1, k2, screen) -> None:
        '''
        Procedimientos realizados en cada iteración del ambiente.
        '''
        for agent in self.agents:
            if (not agent.loaded and self.state[agent.x, agent.y]):
                f = self.fractionObjects(agent)
                p_p = Corpse.probPickup(k1, f)
                if random.random() < p_p:
                    corpse = self.state[agent.x, agent.y]
                    corpse.x, corpse.y = None, None # Temporalmente se queda sin posicion.
                    agent.object = corpse # El agente carga al objeto.
                    agent.loaded = True
                    self.state[agent.x, agent.y] = None # Se libera la celda.
            elif agent.loaded and self.state[agent.x, agent.y] == None:
                f = self.fractionObjects(agent)
                p_d = Corpse.probDeposit(k2, f)
                if random.random() < p_d:
                    corpse = agent.object
                    corpse.x, corpse.y = agent.x, agent.y
                    agent.object = None # El agente libera al objeto.
                    agent.loaded = False
                    self.state[agent.x, agent.y] = corpse # Se coloca el objeto en la celda.
            agent.move()
        # En cado paso se deberia reimprimir la pantalla, pero por cuestiones de rendimiento
        # esto no se hara asi, sino cada cantidad de pasos fuera de esta funcion.
        # self.printEnviroment(screen)

    @staticmethod
    def validPosition(x, y) -> bool:
        return (x >= 0 and y >= 0 and x < Environment.x_max and y < Environment.y_max)

# -------------------------------- Programa principal -------------------------------

def main():
    # Parametros establecidos.
    width, height = 200, 200 # Numero de columnas y filas.
    num_objects = 5000
    num_agents = 10
    k1 = 0.1
    k2 = 0.3
    t = 0
    t_max = 5000000

    # Estado de las celdas del ambiente. Celda con objeto = objeto Corpse, celda libre = None
    env_state = np.full((width, height), None)
    # Se crean y ubican los objetos (Corpse) aleatorimente.
    for _ in range(num_objects):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        env_state[x, y] = Corpse(x, y)
    # Se crean y ubican aleatoriamente los agentes.
    agents = []
    for _ in range(num_agents):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        agents.append(Agent(x, y))
    # Se crea el ambiente.
    env = Environment(env_state, agents, width, height)

    # Se configura e inicializa la interfaz grafica.
    pygame.init()
    pygame.display.set_caption('Ant clustering')
    screen = pygame.display.set_mode((width, height))
    env.printEnviroment(screen)

    # Bucle principal.
    while (t <= t_max):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if (t % 25000 == 0):
            print('t = ', t)
            env.printEnviroment(screen)
        if (t == 0 or t == 50000 or t == 1000000 or t == 5000000):
            print('Take the screenshot!')
            winsound.Beep(1500, 200)
            time.sleep(10)

        env.step(k1, k2, screen)
        t += 1

if __name__ == "__main__":
    main()