from models.invernadero import Invernadero
from models.planta import Planta
from models.dron import Dron
from models.planRiego import PlanRiego
from tda.lista import Lista

def generar_salida(invernaderos, archivo_salida):
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0"?>\n')
        f.write('<datosSalida>\n')
        f.write('  <listaInvernaderos>\n')

        actual_inv = invernaderos.cabeza
        while actual_inv is not None:
            inv = actual_inv.dato
            f.write(f'    <invernadero nombre="{inv.nombre}">\n')
            f.write('      <listaPlanes>\n')

            actual_plan = inv.lista_planes.cabeza
            while actual_plan is not None:
                plan = actual_plan.dato
                f.write(f'        <plan nombre="{plan.nombre}">\n')
                f.write(f'          <tiempoOptimoSegundos>{plan.tiempo_optimo}</tiempoOptimoSegundos>\n')
                f.write(f'          <aguaRequeridaLitros>{plan.agua_total}</aguaRequeridaLitros>\n')
                f.write(f'          <fertilizanteRequeridoGramos>{plan.fert_total}</fertilizanteRequeridoGramos>\n')
                f.write('          <eficienciaDronesRegadores>\n')

                dr_actual = inv.lista_drones.cabeza
                while dr_actual is not None:
                    dron = dr_actual.dato
                    f.write(f'            <dron nombre="{dron.nombre}" litrosAgua="{dron.agua_usada}" gramosFertilizante="{dron.fert_usado}"/>\n')
                    dr_actual = dr_actual.siguiente

                f.write('          </eficienciaDronesRegadores>\n')
                f.write('          <instrucciones>\n')

                inst_actual = plan.instrucciones.cabeza
                while inst_actual is not None:
                    inst = inst_actual.dato
                    f.write(f'            <tiempo segundos="{inst.tiempo}">\n')
                    acc_actual = inst.acciones.cabeza
                    while acc_actual is not None:
                        accion = acc_actual.dato
                        f.write(f'              <dron nombre="{accion.dron}" accion="{accion.accion}"/>\n')
                        acc_actual = acc_actual.siguiente
                    f.write('            </tiempo>\n')
                    inst_actual = inst_actual.siguiente

                f.write('          </instrucciones>\n')
                f.write('        </plan>\n')
                actual_plan = actual_plan.siguiente

            f.write('      </listaPlanes>\n')
            f.write('    </invernadero>\n')
            actual_inv = actual_inv.siguiente

        f.write('  </listaInvernaderos>\n')
        f.write('</datosSalida>\n')