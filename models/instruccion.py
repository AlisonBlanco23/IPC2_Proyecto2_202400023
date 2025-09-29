from tda.lista import Lista
from models.accion import Accion

class Instruccion:
    def __init__(self, tiempo):
        self.tiempo = tiempo
        self.acciones = Lista()

    def agregar_accion(self, accion: Accion):
        self.acciones.agregar(accion)