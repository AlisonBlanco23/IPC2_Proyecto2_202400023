from flask import Flask, render_template, request, redirect, url_for, send_from_directory, Response
import os
from utils.xml_parser import parsear_entrada
from utils.xml_generator import generar_salida
from utils.html_generator import generar_reporte_html
from utils.graphviz_generator import generar_grafo_tda
from tda.lista import Lista
from models.instruccion import Instruccion
from models.accion import Accion
from models.invernadero import Invernadero
from models.dron import Dron
from models.planRiego import PlanRiego
from utils.xml_parser import ListaMapa

app = Flask(__name__)
os.makedirs('output', exist_ok=True)
os.makedirs('entradas', exist_ok=True)

INVERNADEROS = Lista()
INVERNADERO_SELECCIONADO = None
PLAN_SELECCIONADO = None
TIEMPO_T = 1

def limpiar_configuracion():
    global INVERNADEROS, INVERNADERO_SELECCIONADO, PLAN_SELECCIONADO, TIEMPO_T
    INVERNADEROS = Lista()
    INVERNADERO_SELECCIONADO = None
    PLAN_SELECCIONADO = None
    TIEMPO_T = 1

@app.route('/')
def index():
    return render_template('index.html', invernaderos=INVERNADEROS)

@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

@app.route('/limpiar', methods=['POST'])
def limpiar():
    limpiar_configuracion()
    return redirect(url_for('index'))

@app.route('/cargar', methods=['POST'])
def cargar():
    limpiar_configuracion()
    archivo = request.files.get('archivo')
    if archivo and archivo.filename.endswith('.xml'):
        nombre_archivo = archivo.filename
        ruta_guardado = os.path.join('entradas', nombre_archivo)
        archivo.save(ruta_guardado)
        try:
            global INVERNADEROS
            INVERNADEROS = parsear_entrada(ruta_guardado)
        except Exception as e:
            print("Error al parsear:", e)
            INVERNADEROS = Lista()
    return redirect(url_for('index'))

@app.route('/get-plans')
def get_plans():
    inv_nombre = request.args.get('invernadero', '').strip()
    if not inv_nombre:
        return Response('{"planes":[]}', mimetype='application/json')
    
    json_str = '{"planes": ['
    first = True
    inv_actual = INVERNADEROS.cabeza
    while inv_actual is not None:
        inv = inv_actual.dato
        if inv.nombre.strip() == inv_nombre:
            p_actual = inv.lista_planes.cabeza
            while p_actual is not None:
                if not first:
                    json_str += ', '
                plan_name = p_actual.dato.nombre.strip().replace('"', '\\"')
                json_str += f'"{plan_name}"'
                first = False
                p_actual = p_actual.siguiente
            break
        inv_actual = inv_actual.siguiente

    json_str += ']}'
    return Response(json_str, mimetype='application/json')

@app.route('/simular', methods=['POST'])
def simular():
    global INVERNADEROS, INVERNADERO_SELECCIONADO, PLAN_SELECCIONADO
    inv_nombre = request.form.get('invernadero', '').strip()
    plan_nombre = request.form.get('plan', '').strip()

    inv_original = None
    inv_actual = INVERNADEROS.cabeza
    while inv_actual is not None:
        if inv_actual.dato.nombre.strip() == inv_nombre:
            inv_original = inv_actual.dato
            break
        inv_actual = inv_actual.siguiente

    if inv_original is None:
        return redirect(url_for('index'))

    plan_original = None
    p_actual = inv_original.lista_planes.cabeza
    while p_actual is not None:
        if p_actual.dato.nombre.strip() == plan_nombre:
            plan_original = p_actual.dato
            break
        p_actual = p_actual.siguiente

    if plan_original is None:
        return redirect(url_for('index'))

    inv_sim = Invernadero(inv_original.nombre, inv_original.num_hileras, inv_original.plantas_x_hilera)
    
    p_actual = inv_original.lista_plantas.cabeza
    while p_actual is not None:
        inv_sim.agregar_planta(p_actual.dato)
        p_actual = p_actual.siguiente
    
    d_actual = inv_original.lista_drones.cabeza
    while d_actual is not None:
        dron = d_actual.dato
        nuevo_dron = Dron(dron.id_dron, dron.nombre, dron.hilera_asignada)
        inv_sim.agregar_dron(nuevo_dron)
        d_actual = d_actual.siguiente
    
    plan_sim = PlanRiego(plan_original.nombre)
    pp_actual = plan_original.lista_riego.cabeza
    while pp_actual is not None:
        plan_sim.agregar_planta_a_plan(pp_actual.dato)
        pp_actual = pp_actual.siguiente
    inv_sim.agregar_plan(plan_sim)

    dr_actual = inv_sim.lista_drones.cabeza
    while dr_actual is not None:
        dr = dr_actual.dato
        dr.posicion_actual = 0
        dr.agua_usada = 0.0
        dr.fert_usado = 0.0
        dr_actual = dr_actual.siguiente

    tam_plan = plan_sim.lista_riego.obtener_tamanio()
    plan_sim.instrucciones = Lista()
    tiempo = 0
    idx_plan = 0
    drones_terminados = ListaMapa()

    while idx_plan < tam_plan:
        tiempo += 1
        instr = Instruccion(tiempo)
        riego_realizado = False

        dr_actual = inv_sim.lista_drones.cabeza
        while dr_actual is not None:
            dron = dr_actual.dato
            dron_key = dron.nombre
            terminado = drones_terminados.buscar(dron_key)
            if terminado is None:
                terminado = False
                drones_terminados.agregar(dron_key, terminado)

            if terminado:
                if dron.posicion_actual > 0:
                    dron.posicion_actual -= 1
                    accion = "Atras (Inicio)"
                else:
                    accion = "FIN"
            else:
                if idx_plan < tam_plan and not riego_realizado:
                    planta_str = plan_sim.lista_riego.obtener(idx_plan)
                    partes = planta_str.split('-')
                    try:
                        hilera_obj = int(partes[0][1:])
                        pos_obj = int(partes[1][1:])
                        if dron.hilera_asignada == hilera_obj:
                            if dron.posicion_actual < pos_obj:
                                dron.posicion_actual += 1
                                accion = f"Adelante (H{hilera_obj}P{dron.posicion_actual})"
                            elif dron.posicion_actual > pos_obj:
                                dron.posicion_actual -= 1
                                accion = f"Atras (H{hilera_obj}P{dron.posicion_actual})"
                            elif dron.posicion_actual == pos_obj:
                                planta = inv_sim.obtener_planta_por_hilera_pos(hilera_obj, pos_obj)
                                if planta:
                                    dron.agua_usada += planta.litros_agua
                                    dron.fert_usado += planta.gramos_fertilizante
                                accion = f"Regar ({planta_str})"
                                riego_realizado = True
                                idx_plan += 1

                                tiene_mas_tareas = False
                                for i in range(idx_plan, tam_plan):
                                    p = plan_sim.lista_riego.obtener(i)
                                    p_partes = p.split('-')
                                    try:
                                        h = int(p_partes[0][1:])
                                        if dron.hilera_asignada == h:
                                            tiene_mas_tareas = True
                                            break
                                    except:
                                        continue
                                if not tiene_mas_tareas:
                                    drones_terminados.agregar(dron_key, True)
                            else:
                                accion = "Esperar"
                        else:
                            tiene_tarea = False
                            for i in range(idx_plan, tam_plan):
                                p = plan_sim.lista_riego.obtener(i)
                                p_partes = p.split('-')
                                try:
                                    h = int(p_partes[0][1:])
                                    if dron.hilera_asignada == h:
                                        tiene_tarea = True
                                        break
                                except:
                                    continue
                            if not tiene_tarea:
                                if dron.posicion_actual > 0:
                                    dron.posicion_actual -= 1
                                    accion = "Atras (Inicio)"
                                else:
                                    accion = "Esperar"
                                drones_terminados.agregar(dron_key, True)
                            else:
                                for i in range(idx_plan, tam_plan):
                                    p = plan_sim.lista_riego.obtener(i)
                                    p_partes = p.split('-')
                                    try:
                                        h = int(p_partes[0][1:])
                                        p_pos = int(p_partes[1][1:])
                                        if dron.hilera_asignada == h:
                                            if dron.posicion_actual < p_pos:
                                                dron.posicion_actual += 1
                                                accion = f"Adelante (H{h}P{dron.posicion_actual})"
                                            elif dron.posicion_actual > p_pos:
                                                dron.posicion_actual -= 1
                                                accion = f"Atras (H{h}P{dron.posicion_actual})"
                                            else:
                                                accion = "Esperar"
                                            break
                                    except:
                                        continue
                    except:
                        accion = "Esperar"
                else:
                    accion = "Esperar"

            instr.agregar_accion(Accion(dron.nombre, accion))
            dr_actual = dr_actual.siguiente

        plan_sim.instrucciones.agregar(instr)

    todos_en_inicio = False
    while not todos_en_inicio:
        tiempo += 1
        instr = Instruccion(tiempo)
        todos_en_inicio = True
        dr_actual = inv_sim.lista_drones.cabeza
        while dr_actual is not None:
            dron = dr_actual.dato
            if dron.posicion_actual > 0:
                dron.posicion_actual -= 1
                accion = "Atras (Inicio)"
                todos_en_inicio = False
            else:
                accion = "FIN"
            instr.agregar_accion(Accion(dron.nombre, accion))
            dr_actual = dr_actual.siguiente
        plan_sim.instrucciones.agregar(instr)

    plan_sim.tiempo_optimo = tiempo

    total_agua = 0.0
    total_fert = 0.0
    dr_actual = inv_sim.lista_drones.cabeza
    while dr_actual is not None:
        dron = dr_actual.dato
        total_agua += dron.agua_usada
        total_fert += dron.fert_usado
        dr_actual = dr_actual.siguiente

    plan_sim.agua_total = total_agua
    plan_sim.fert_total = total_fert

    INVERNADERO_SELECCIONADO = inv_sim
    PLAN_SELECCIONADO = plan_sim

    invernaderos_salida = Lista()
    invernaderos_salida.agregar(inv_sim)
    generar_salida(invernaderos_salida, 'output/salida.xml')
    generar_reporte_html(invernaderos_salida, 'output/ReporteInvernaderos.html')

    return redirect(url_for('reporte'))

@app.route('/reporte')
def reporte():
    if INVERNADERO_SELECCIONADO is None or PLAN_SELECCIONADO is None:
        return redirect(url_for('index'))
    return render_template('report.html', invernadero=INVERNADERO_SELECCIONADO, plan=PLAN_SELECCIONADO, tiempo_t=TIEMPO_T)

@app.route('/generar_grafo', methods=['POST'])
def generar_grafo():
    global TIEMPO_T
    t = request.form.get('tiempo_t', '1')
    try:
        TIEMPO_T = max(1, min(int(t), PLAN_SELECCIONADO.tiempo_optimo))
    except:
        TIEMPO_T = 1
    generar_grafo_tda(INVERNADERO_SELECCIONADO, PLAN_SELECCIONADO, TIEMPO_T)
    return redirect(url_for('reporte'))

@app.route('/grafo')
def ver_grafo():
    return render_template('graph.html', tiempo_t=TIEMPO_T)

@app.route('/output/<path:filename>')
def output_static(filename):
    return send_from_directory('output', filename)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)