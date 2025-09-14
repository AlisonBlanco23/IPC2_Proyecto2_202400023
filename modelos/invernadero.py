from .planta import Planta
from .dron import Dron
from ..tdas.lista_enlazada import ListaEnlazada
from ..tdas.cola import Cola

class Invernadero:
    def __init__(self, nombre, numero_hileras, plantas_por_hilera):
        self.nombre = nombre
        self.numero_hileras = numero_hileras
        self.plantas_por_hilera = plantas_por_hilera
        self.lista_plantas = ListaEnlazada()    
        self.lista_drones = ListaEnlazada()    
        self.asignacion_drones = {}             
        self.planes_riego = {}               

    def agregar_planta(self, planta):
        self.lista_plantas.agregar(planta)

    def agregar_dron(self, dron):
        self.lista_drones.agregar(dron)
        self.asignacion_drones[dron.id] = dron.hilera_asignada

    def agregar_plan(self, nombre_plan, secuencia_str):
        tareas = secuencia_str.split(',')
        cola_tareas = Cola()
        for tarea in tareas:
            cola_tareas.encolar(tarea.strip())
        self.planes_riego[nombre_plan] = cola_tareas

    def obtener_dron_por_hilera(self, hilera):
        for dron in self.lista_drones.iterar():
            if dron.hilera_asignada == hilera:
                return dron
        return None

    def obtener_planta(self, hilera, posicion):
        for planta in self.lista_plantas.iterar():
            if planta.hilera == hilera and planta.posicion == posicion:
                return planta
        return None

    def __str__(self):
        return f"Invernadero {self.nombre} ({self.numero_hileras} hileras)"