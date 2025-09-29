from models.invernadero import Invernadero
from models.planta import Planta
from models.dron import Dron
from models.planRiego import PlanRiego
from tda.lista import Lista

class NodoMapa:
    def __init__(self, clave, valor):
        self.clave = clave
        self.valor = valor
        self.siguiente = None

class ListaMapa:
    def __init__(self):
        self.cabeza = None

    def agregar(self, clave, valor):
        nuevo = NodoMapa(clave, valor)
        if self.cabeza is None:
            self.cabeza = nuevo
            return
        actual = self.cabeza
        while actual.siguiente is not None:
            actual = actual.siguiente
        actual.siguiente = nuevo

    def buscar(self, clave):
        actual = self.cabeza
        while actual is not None:
            if actual.clave == clave:
                return actual.valor
            actual = actual.siguiente
        return None

def extraer_etiqueta(contenido, nombre_etiqueta):
    inicio = "<" + nombre_etiqueta + ">"
    fin = "</" + nombre_etiqueta + ">"
    i = contenido.find(inicio)
    if i == -1:
        return ""
    i += len(inicio)
    j = contenido.find(fin, i)
    if j == -1:
        return ""
    return contenido[i:j].strip()

def extraer_contenido_etiqueta(contenido, nombre_etiqueta):
    return extraer_etiqueta(contenido, nombre_etiqueta)

def extraer_atributo(cadena, nombre_atributo):
    patron = nombre_atributo + "="
    i = cadena.find(patron)
    if i == -1:
        return ""
    i += len(patron)
    if i < len(cadena) and (cadena[i] == "'" or cadena[i] == '"'):
        quote = cadena[i]
        i += 1
        j = cadena.find(quote, i)
        if j == -1:
            return ""
        return cadena[i:j].strip()
    else:
        j = i
        while j < len(cadena) and cadena[j] not in " >":
            j += 1
        return cadena[i:j].strip()

def parsear_entrada(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
    except:
        raise Exception("Archivo de entrada no encontrado")

    contenido = contenido.replace('\n', ' ').replace('\t', ' ')
    if contenido.find("<configuracion>") == -1 or contenido.find("</configuracion>") == -1:
        raise Exception("Formato XML inválido: falta <configuracion>")

    inicio = contenido.find("<configuracion>") + len("<configuracion>")
    fin = contenido.find("</configuracion>")
    contenido_interior = contenido[inicio:fin].strip()

    drones_str = extraer_etiqueta(contenido_interior, "listaDrones")
    mapa_drones = ListaMapa()
    partes = drones_str.split("<dron")
    idx = 1
    while idx < len(partes):
        parte = partes[idx]
        id_str = extraer_atributo(parte, "id")
        nombre_str = extraer_atributo(parte, "nombre")
        if id_str != "" and nombre_str != "":
            try:
                id_num = int(id_str)
                mapa_drones.agregar(id_num, nombre_str.strip())
            except:
                pass
        idx += 1

    invernaderos_str = extraer_etiqueta(contenido_interior, "listaInvernaderos")
    partes_invernaderos = invernaderos_str.split("<invernadero")
    resultado = Lista()
    idx = 1
    while idx < len(partes_invernaderos):
        parte_inv = partes_invernaderos[idx]
        nombre = extraer_atributo(parte_inv, "nombre")
        if nombre == "":
            idx += 1
            continue
        num_hileras = extraer_contenido_etiqueta(parte_inv, "numeroHileras")
        plantas_x_hilera = extraer_contenido_etiqueta(parte_inv, "plantasXhilera")
        try:
            num_hileras_i = int(num_hileras.strip())
            plantas_x_hilera_i = int(plantas_x_hilera.strip())
        except:
            idx += 1
            continue

        inv = Invernadero(nombre.strip(), num_hileras_i, plantas_x_hilera_i)

        plantas_str = extraer_etiqueta(parte_inv, "listaPlantas")
        partes_planta = plantas_str.split("<planta")
        j = 1
        while j < len(partes_planta):
            parte_pl = partes_planta[j]
            hil = extraer_atributo(parte_pl, "hilera")
            pos = extraer_atributo(parte_pl, "posicion")
            litros = extraer_atributo(parte_pl, "litrosAgua")
            gramos = extraer_atributo(parte_pl, "gramosFertilizante")
            especie = ""
            fin_tag = parte_pl.find(">")
            if fin_tag != -1:
                texto = parte_pl[fin_tag + 1:]
                fin_texto = texto.find("</planta>")
                if fin_texto != -1:
                    especie = texto[:fin_texto].strip()
            if hil != "" and pos != "" and litros != "" and gramos != "":
                try:
                    h_i = int(hil.strip())
                    p_i = int(pos.strip())
                    l_f = float(litros.strip())
                    g_f = float(gramos.strip())
                    planta = Planta(h_i, p_i, l_f, g_f, especie)
                    inv.agregar_planta(planta)
                except:
                    pass
            j += 1

        asign_str = extraer_etiqueta(parte_inv, "asignacionDrones")
        partes_asig = asign_str.split("<dron")
        j = 1
        while j < len(partes_asig):
            parte_as = partes_asig[j]
            dron_id_s = extraer_atributo(parte_as, "id")
            hilera_s = extraer_atributo(parte_as, "hilera")
            if dron_id_s != "" and hilera_s != "":
                try:
                    dron_id = int(dron_id_s.strip())
                    hilera = int(hilera_s.strip())
                    nombre_dron = mapa_drones.buscar(dron_id)
                    if nombre_dron is not None:
                        dron = Dron(dron_id, nombre_dron.strip(), hilera)
                        inv.agregar_dron(dron)
                except:
                    pass
            j += 1

        planes_str = extraer_etiqueta(parte_inv, "planesRiego")
        partes_planes = planes_str.split("<plan")
        j = 1
        while j < len(partes_planes):
            parte_pln = partes_planes[j]
            nombre_plan = extraer_atributo(parte_pln, "nombre").strip()
            if nombre_plan == "":
                j += 1
                continue
            fin_tag = parte_pln.find(">")
            if fin_tag == -1:
                j += 1
                continue
            texto = parte_pln[fin_tag + 1:]
            fin_texto = texto.find("</plan>")
            if fin_texto == -1:
                j += 1
                continue
            plan_texto = texto[:fin_texto].strip()
            plan_riego = PlanRiego(nombre_plan)
            items = plan_texto.split(",")
            for item in items:
                item_limpio = item.strip()
                if item_limpio:
                    plan_riego.agregar_planta_a_plan(item_limpio)
            inv.agregar_plan(plan_riego)
            j += 1

        resultado.agregar(inv)
        idx += 1

    return resultado