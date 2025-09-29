from tda.lista import Lista

class PlanRiego:
    def __init__(self, nombre):
        self.nombre = nombre
        self.lista_riego = Lista()
        self.instrucciones = Lista()
        self.tiempo_optimo = 0
        self.agua_total = 0.0
        self.fert_total = 0.0

    def agregar_planta_a_plan(self, planta_str):
        self.lista_riego.agregar(planta_str)