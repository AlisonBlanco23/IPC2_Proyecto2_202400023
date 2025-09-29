from tda.cola import Cola

class Dron:
    def __init__(self, id_dron, nombre, hilera_asignada):
        self.id_dron = id_dron
        self.nombre = nombre
        self.hilera_asignada = hilera_asignada
        self.posicion_actual = 1
        self.agua_usada = 0.0
        self.fert_usado = 0.0

    def mover_adelante(self, max_pos=None):
        if max_pos is None or self.posicion_actual < max_pos:
            self.posicion_actual += 1

    def mover_atras(self):
        if self.posicion_actual > 1:
            self.posicion_actual -= 1