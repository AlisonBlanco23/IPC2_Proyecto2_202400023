from tdas.nodo import Nodo
from tdas.lista_enlazada import ListaEnlazada
from tdas.cola import Cola
from modelos.planta import Planta
from modelos.dron import Dron

# Prueba ListaEnlazada
lista = ListaEnlazada()
lista.agregar("A")
lista.agregar("B")
print("Lista:", [x for x in lista.iterar()])  # ['A', 'B']

# Prueba Cola
cola = Cola()
cola.encolar("H1-P2")
cola.encolar("H2-P1")
print("Cola primero:", cola.ver_primero())  # H1-P2
print("Desencolar:", cola.desencolar())     # H1-P2

# Prueba objetos
planta = Planta(1, 2, 1.0, 100, "ciprés")
dron = Dron(1, "DR01", 1)
print("Planta:", planta.hilera, planta.posicion)
print("Dron:", dron.nombre, dron.hilera_asignada)