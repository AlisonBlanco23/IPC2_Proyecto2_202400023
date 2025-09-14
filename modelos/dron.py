class Dron:
    def __init__(self, id_dron, nombre, hilera_asignada):
        self.id = id_dron             
        self.nombre = nombre          
        self.hilera_asignada = hilera_asignada  
        self.posicion_actual = 1    
        self.agua_usada = 0.0         
        self.fertilizante_usado = 0    
        self.acciones_realizadas = [] 

    def mover_adelante(self):
        self.posicion_actual += 1
        self.acciones_realizadas.append(f"Adelante(H{self.hilera_asignada}P{self.posicion_actual})")

    def mover_atras(self):
        self.posicion_actual -= 1
        self.acciones_realizadas.append(f"Atras(H{self.hilera_asignada}P{self.posicion_actual})")

    def regar(self, litros, gramos):
        self.agua_usada += litros
        self.fertilizante_usado += gramos
        self.acciones_realizadas.append("Regar")

    def regresar_inicio(self):
        while self.posicion_actual > 1:
            self.mover_atras()
        self.acciones_realizadas.append("FIN")

    def obtener_resumen(self):
        return {
            "nombre": self.nombre,
            "litros_agua": self.agua_usada,
            "gramos_fertilizante": self.fertilizante_usado,
            "acciones": self.acciones_realizadas
        }

    def __str__(self):
        return f"{self.nombre} (H{self.hilera_asignada}, Pos:{self.posicion_actual})"