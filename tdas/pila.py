from .lista_enlazada import ListaEnlazada

class Pila:
    def __init__(self):
        self.lista = ListaEnlazada()

    def apilar(self, dato):
        self.lista.agregar(dato)

    def desapilar(self):
        if self.esta_vacia():
            return None
        ultimo_indice = self.lista.longitud() - 1
        dato = self.lista.obtener(ultimo_indice)
        self.lista.eliminar(dato)
        return dato

    def esta_vacia(self):
        return self.lista.es_vacia()

    def ver_tope(self):
        if self.esta_vacia():
            return None
        ultimo_indice = self.lista.longitud() - 1
        return self.lista.obtener(ultimo_indice)

    def longitud(self):
        return self.lista.longitud()