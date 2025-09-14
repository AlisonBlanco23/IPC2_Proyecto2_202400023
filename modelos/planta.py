class Planta:
    def __init__(self, hilera, posicion, litros_agua, gramos_fertilizante, especie):
        self.hilera = hilera          
        self.litros_agua = litros_agua 
        self.gramos_fertilizante = gramos_fertilizante
        self.especie = especie      

    def __str__(self):
        return f"Planta(H{self.hilera}-P{self.posicion}: {self.especie})"