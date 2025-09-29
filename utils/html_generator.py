def generar_reporte_html(invernaderos, archivo_salida):
    html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte GuateRiegos 2.0</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f0f9ff; }
        .header { 
            background: linear-gradient(120deg, #1976d2, #2196f3); 
            color: white; 
            padding: 20px; 
            text-align: center; 
            border-radius: 0 0 12px 12px; 
        }
        .card { 
            box-shadow: 0 4px 8px rgba(0,0,0,0.08); 
            margin-bottom: 24px; 
            border-radius: 10px; 
            border: none; 
        }
        table { background: white; }
        .stats { 
            background-color: #e3f2fd; 
            padding: 15px; 
            border-radius: 8px; 
            margin: 15px 0; 
        }
        /* 👇 Encabezados de tabla en tono azul claro — forzado */
        thead th {
            background-color: #4fc3f7 !important; /* Azul claro brillante */
            color: #01579b !important;
            font-weight: bold !important;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Reporte de Riego y Aplicación de Fertilizante - GuateRiegos 2.0</h1>
    </div>
    <div class="container mt-4">
"""

    inv_actual = invernaderos.cabeza
    while inv_actual is not None:
        inv = inv_actual.dato
        html += f'<div class="card"><div class="card-body"><h2 class="text-primary">Invernadero: {inv.nombre}</h2>'
        plan_actual = inv.lista_planes.cabeza
        while plan_actual is not None:
            plan = plan_actual.dato
            html += f"""
                <h3 class="mt-3">Plan: {plan.nombre}</h3>
                <div class="stats">
                    <strong>Tiempo óptimo:</strong> {plan.tiempo_optimo} segundos<br>
                    <strong>Agua total:</strong> {plan.agua_total} litros<br>
                    <strong>Fertilizante total:</strong> {plan.fert_total} gramos
                </div>
                <h4>Asignación de Drones</h4>
                <table class="table table-striped">
                    <thead><tr><th>Hilera</th><th>Dron</th></tr></thead>
                    <tbody>
"""
            dr_actual = inv.lista_drones.cabeza
            while dr_actual is not None:
                dron = dr_actual.dato
                html += f"<tr><td>H{dron.hilera_asignada}</td><td>{dron.nombre}</td></tr>"
                dr_actual = dr_actual.siguiente
            html += "</tbody></table>"

            html += "<h4>Instrucciones por Segundo</h4><table class='table table-bordered'><thead><tr><th>Segundo</th>"
            dr_actual = inv.lista_drones.cabeza
            while dr_actual is not None:
                html += f"<th>{dr_actual.dato.nombre}</th>"
                dr_actual = dr_actual.siguiente
            html += "</tr></thead><tbody>"

            inst_actual = plan.instrucciones.cabeza
            while inst_actual is not None:
                instr = inst_actual.dato
                html += f"<tr><td>{instr.tiempo}</td>"
                dr_actual = inv.lista_drones.cabeza
                while dr_actual is not None:
                    dron = dr_actual.dato
                    accion = "Esperar"
                    acc_actual = instr.acciones.cabeza
                    while acc_actual is not None:
                        a = acc_actual.dato
                        if a.dron == dron.nombre:
                            accion = a.accion
                            break
                        acc_actual = acc_actual.siguiente
                    html += f"<td>{accion}</td>"
                    dr_actual = dr_actual.siguiente
                html += "</tr>"
                inst_actual = inst_actual.siguiente
            html += "</tbody></table>"

            html += "<h4>Eficiencia por Dron</h4><table class='table table-info'><thead><tr><th>Dron</th><th>Agua (L)</th><th>Fertilizante (g)</th></tr></thead><tbody>"
            dr_actual = inv.lista_drones.cabeza
            while dr_actual is not None:
                dron = dr_actual.dato
                html += f"<tr><td>{dron.nombre}</td><td>{dron.agua_usada}</td><td>{dron.fert_usado}</td></tr>"
                dr_actual = dr_actual.siguiente
            html += "</tbody></table></div>"
            plan_actual = plan_actual.siguiente
        html += "</div>"
        inv_actual = inv_actual.siguiente

    html += """
    </div>
</body>
</html>
"""

    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write(html)