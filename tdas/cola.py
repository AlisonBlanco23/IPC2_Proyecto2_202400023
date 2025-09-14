from .lista_enlazada import ListaEnlazada

class Cola:
    def __init__(self):
        self.lista = ListaEnlazada()

    def encolar(self, dato):
        self.lista.agregar(dato)

    def desencolar(self):
        if self.esta_vacia():
            return None
        dato = self.lista.obtener(0)
        self.lista.eliminar(dato)
        return dato

    def esta_vacia(self):
        return self.lista.es_vacia()

    def longitud(self):
        return self.lista.longitud()

    def ver_primero(self):
        if self.esta_vacia():
            return None
        return self.lista.obtener(0)

    def __str__(self):
        return str(self.lista)