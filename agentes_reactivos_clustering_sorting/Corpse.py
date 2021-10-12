class Corpse:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type # Tipo de objeto: a, b, c

    @staticmethod
    def probPickup(k1, f) -> float:
        '''Probabilidad de que un objeto Corpse sea recogido por algún agente.'''
        return ( (k1 / (k1+f))**2 )

    @staticmethod
    def probDeposit(k2, f) -> float:
        '''
        Probabilidad de que algún agente que esta cargando un objeto Corpse
        deposite al objeto en una celda vacia.
        '''
        return ( (f / (k2+f))**2 )
        