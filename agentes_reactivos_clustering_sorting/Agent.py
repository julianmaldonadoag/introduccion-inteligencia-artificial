import random
from Environment import *

class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.loaded = False # ¿Esta cargando un objeto?
        self.object = None # Objeto que podria a cargar, de tipo Corpse.
        # Memoria de objetos percibidos en los ultimos T tiempos, por tipo de objeto.
        # Es una lista de diccionarios con 3 pares clave-valor, donde cada diccionario tiene 
        # como llave el tipo de objeto y como valor la cantidad de objetos percibidos del tipo
        # correspondiente en determinado tiempo, por ejemplo { 'a': 2, 'b': 1, 'c': 3 }
        self.memory = []

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

    def updateMemory(self, perceived_objects, T) -> None:
        '''
        Actualiza la memoria del agente agregando el diccionario de los nuevos objetos percibidos 
        por cada tipo a la lista, verifica tambien que la memoria no exceda el T maximo, de ser asi 
        se elimina el diccionario que guarda los objetos percibidos por cada tipo de mayor tiempo, 
        (el primero de la lista) lo que hace que la memoria se comporte como una cola.
        '''
        # Se agrega al final de la lista la nueva observación de objetos percibidos.
        self.memory.append({ 
            'a': perceived_objects['a'], 
            'b': perceived_objects['b'],
            'c': perceived_objects['c']
        })
        # Se mantiene el tamaño de la memoria maximo, eliminando el primer diccionario en caso de 
        # superarse el valor maximo de la memoria.
        if len(self.memory) > T:
            self.memory.pop(0)
            