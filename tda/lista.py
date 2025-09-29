class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class Lista:
    def __init__(self):
        self.cabeza = None
        self.tamanio = 0

    def esta_vacia(self):
        return self.cabeza is None

    def agregar(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        self.tamanio += 1

    def obtener(self, indice):
        if indice < 0 or indice >= self.tamanio:
            raise IndexError("Índice fuera de rango")
        actual = self.cabeza
        for _ in range(indice):
            actual = actual.siguiente
        return actual.dato

    def obtener_tamanio(self):
        return self.tamanio

    def __iter__(self):
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente