import pygame
import random
from Corpse import *

class Environment:
    x_max = 200
    y_max = 200

    def __init__(self, grid, agents, width, height):
        self.grid = grid # Matriz donde se almacenan los objetos Corpse.
        self.agents = agents # Lista de objetos Agent.
        self.width = width
        self.height = height
        self.bg_color = (255, 255, 255) # Color del fondo.
         # Color de la celda que tiene un objeto, por tipo de objeto.
        self.object_colors = { 
            'a': (255, 0, 0), # Rojo
            'b': (0, 255, 0), # Verde
            'c': (0, 0, 255)  # Azul
        }

    def printEnviroment(self, screen) -> None:
        '''Imprime el estado actual del ambiente.'''
        screen.fill(self.bg_color)

        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x, y] != None:
                    color = self.object_colors[self.grid[x, y].type]
                    screen.set_at((x, y), color)
        pygame.display.flip() # Muestra la cuadricula

    def countObjects(self, agent) -> dict:
        '''
        Le permite a un agente percibir la cantidad de objetos que se encuentran a su alrededor
        por cada uno de los diferentes tipos de objeto.
        '''
        count = {
            'a': 0,
            'b': 0,
            'c': 0
        }
        for i in range(-1, 2):
            for j in range(-1, 2):
                condition = (
                    (i != 0 or j != 0)
                    and Environment.validPosition(agent.x + i,  agent.y + j) 
                    and self.grid[agent.x + i,  agent.y + j] != None
                )
                if condition:
                    type_corpse = self.grid[agent.x + i,  agent.y + j].type
                    count[type_corpse] += 1

        return count

    def fractionObjects(self, agent, type_corpse) -> float:
        '''
        Le permite a un agente obtener la fracción de objetos que se encuentran a su alrededor
        en los ultimos T tiempos y que son de un determinado tipo de objeto.
        '''
        total = 0
        for mem in agent.memory:
            total += mem[type_corpse]
        size_mem = len(agent.memory)
        return ( total / (8*size_mem) )

    def step(self, k1, k2, T) -> None:
        '''
        Procedimientos realizados en cada iteración del ambiente.
        '''
        for agent in self.agents:
            if not agent.loaded and self.grid[agent.x, agent.y] != None:
                corpse = self.grid[agent.x, agent.y]
                perceived_objects = self.countObjects(agent)
                agent.updateMemory(perceived_objects, T)
                f = self.fractionObjects(agent, corpse.type)
                p_p = Corpse.probPickup(k1, f)
                if random.random() <= p_p:
                    corpse.x, corpse.y = None, None # Temporalmente se queda sin posicion.
                    agent.object = corpse # El agente carga al objeto.
                    self.grid[agent.x, agent.y] = None # Se remueve el objeto de la celda.
                    agent.loaded = True
            elif agent.loaded and self.grid[agent.x, agent.y] == None:
                corpse = agent.object
                perceived_objects = self.countObjects(agent)
                agent.updateMemory(perceived_objects, T)
                f = self.fractionObjects(agent, corpse.type)
                p_d = Corpse.probDeposit(k2, f)
                if random.random() <= p_d:
                    corpse.x, corpse.y = agent.x, agent.y
                    agent.object = None # El agente libera al objeto.
                    self.grid[agent.x, agent.y] = corpse # Se coloca el objeto en la celda.
                    agent.loaded = False
            agent.move()

    @staticmethod
    def validPosition(x, y) -> bool:
        return (x >= 0 and y >= 0 and x < Environment.x_max and y < Environment.y_max)
        