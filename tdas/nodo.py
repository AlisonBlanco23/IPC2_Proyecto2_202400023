class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

    def obtener_dato(self):
        return self.dato

    def obtener_siguiente(self):
        return self.siguiente

    def asignar_siguiente(self, nuevo_siguiente):
        self.siguiente = nuevo_siguiente