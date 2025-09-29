from tda.lista import Lista

class Invernadero:
    def __init__(self, nombre, num_hileras, plantas_x_hilera):
        self.nombre = nombre
        self.num_hileras = num_hileras
        self.plantas_x_hilera = plantas_x_hilera
        self.lista_plantas = Lista()
        self.lista_drones = Lista()
        self.lista_planes = Lista()

    def agregar_planta(self, planta):
        self.lista_plantas.agregar(planta)

    def agregar_dron(self, dron):
        self.lista_drones.agregar(dron)

    def agregar_plan(self, plan):
        self.lista_planes.agregar(plan)

    def obtener_planta_por_hilera_pos(self, hilera, posicion):
        actual = self.lista_plantas.cabeza
        while actual:
            p = actual.dato
            if p.hilera == hilera and p.posicion == posicion:
                return p
            actual = actual.siguiente
        return None