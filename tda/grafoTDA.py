from tda.lista import Lista

class GrafoTDA:
    def __init__(self):
        self.nodos = Lista()
        self.aristas = Lista()

    def agregar_nodo(self, nombre):
        actual = self.nodos.cabeza
        while actual:
            if actual.dato == nombre:
                return
            actual = actual.siguiente
        self.nodos.agregar(nombre)

    def agregar_arista(self, origen, destino, etiqueta):
        self.aristas.agregar((origen, destino, etiqueta))

    def generar_dot(self, tiempo):
        from graphviz import Digraph
        dot = Digraph(comment=f'Estado de TDAs en tiempo t={tiempo}')
        dot.attr(rankdir='LR')  
        dot.attr('node', shape='box', style='rounded,filled', fillcolor='#e0f7fa', fontname='Arial')
        dot.attr('edge', fontname='Arial', arrowhead='normal')

        actual = self.nodos.cabeza
        while actual:
            dot.node(actual.dato, actual.dato)
            actual = actual.siguiente

        actual = self.aristas.cabeza
        while actual:
            origen, destino, etiqueta = actual.dato
            dot.edge(origen, destino, label=etiqueta)
            actual = actual.siguiente

        dot.render(f'output/tda_graph_t={tiempo}', format='png', cleanup=True)
        return f'tda_graph_t={tiempo}.png'