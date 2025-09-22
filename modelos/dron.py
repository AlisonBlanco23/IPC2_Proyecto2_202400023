class Dron:
    def __init__(self, id_dron, nombre, hilera_asignada):
        self.id = id_dron
        self.nombre = nombre
        self.hilera_asignada = hilera_asignada
        self.posicion_actual = 1
        self.agua_usada = 0.0
        self.fertilizante_usado = 0