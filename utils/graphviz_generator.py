from tda.grafoTDA import GrafoTDA

def generar_grafo_tda(invernadero, plan, tiempo):
    grafo = GrafoTDA()
    
    instruccion_en_t = None
    nodo_inst = plan.instrucciones.cabeza
    while nodo_inst is not None:
        if nodo_inst.dato.tiempo == tiempo:
            instruccion_en_t = nodo_inst.dato
            break
        nodo_inst = nodo_inst.siguiente

    if instruccion_en_t is None:
        grafo.agregar_nodo(f"Segundo {tiempo}")
        grafo.agregar_nodo("Sin instrucciones")
        grafo.agregar_arista(f"Segundo {tiempo}", "Sin instrucciones", "")
        return grafo.generar_dot(tiempo)

    nodo_raiz = f"Segundo {tiempo}"
    grafo.agregar_nodo(nodo_raiz)
    
    nodo_acc = instruccion_en_t.acciones.cabeza
    nodo_previo = nodo_raiz
    
    while nodo_acc is not None:
        accion = nodo_acc.dato
        texto_nodo = f"{accion.dron}: {accion.accion}"
        grafo.agregar_nodo(texto_nodo)
        grafo.agregar_arista(nodo_previo, texto_nodo, "")
        nodo_previo = texto_nodo
        nodo_acc = nodo_acc.siguiente

    return grafo.generar_dot(tiempo)