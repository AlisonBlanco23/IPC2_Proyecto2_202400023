from tda.lista import Nodo

class Cola:
    def __init__(self):
        self.cabeza = None
        self.cola = None
        self.tamanio = 0

    def esta_vacia(self):
        return self.cabeza is None

    def enqueue(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
            self.cola = nuevo_nodo
        else:
            self.cola.siguiente = nuevo_nodo
            self.cola = nuevo_nodo
        self.tamanio += 1

    def dequeue(self):
        if self.esta_vacia():
            raise Exception("No se puede desencolar de una cola vacía")
        dato = self.cabeza.dato
        self.cabeza = self.cabeza.siguiente
        if self.cabeza is None:
            self.cola = None
        self.tamanio -= 1
        return dato

    def frente(self):
        if self.esta_vacia():
            return None
        return self.cabeza.dato

    def obtener_tamanio(self):
        return self.tamanio