from .nodo import Nodo

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None
        self.tamanio = 0

    def es_vacia(self):
        return self.cabeza is None

    def agregar(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.es_vacia():
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.obtener_siguiente() is not None:
                actual = actual.obtener_siguiente()
            actual.asignar_siguiente(nuevo_nodo)
        self.tamanio += 1

    def obtener(self, indice):
        if indice < 0 or indice >= self.tamanio:
            raise IndexError("Índice fuera de rango")
        actual = self.cabeza
        for i in range(indice):
            actual = actual.obtener_siguiente()
        return actual.obtener_dato()

    def eliminar(self, dato):
        if self.es_vacia():
            return False
        if self.cabeza.obtener_dato() == dato:
            self.cabeza = self.cabeza.obtener_siguiente()
            self.tamanio -= 1
            return True
        actual = self.cabeza
        while actual.obtener_siguiente() is not None:
            if actual.obtener_siguiente().obtener_dato() == dato:
                actual.asignar_siguiente(actual.obtener_siguiente().obtener_siguiente())
                self.tamanio -= 1
                return True
            actual = actual.obtener_siguiente()
        return False

    def longitud(self):
        return self.tamanio

    def iterar(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.obtener_dato()
            actual = actual.obtener_siguiente()

    def __str__(self):
        elementos = [str(dato) for dato in self.iterar()]
        return "[" + ", ".join(elementos) + "]"