from ...db import db
from flask import jsonify
from ...models.calificacion.calificacion_model import CalificacionExamen
from enum import Enum
from flask import jsonify
from collections import defaultdict
from collections import Counter
from ...models.evaluador.evaluador_model import Evaluador
from ...models.examen.examen_model import Examen  # Añadir la importación del modelo Examen

class CalificacionEnum(Enum):
    EXCELENTE = {'label': 'EXCELENTE', 'color': 'green', 'nota': 5}
    SOBRESALIENTE = {'label': 'SOBRESALIENTE', 'color': 'blue', 'nota': 4}
    SUFICIENTE = {'label': 'SUFICIENTE', 'color': 'orange', 'nota': 3}
    INSUFICIENTE = {'label': 'INSUFICIENTE', 'color': 'red', 'nota': 2}
    NO_CUMPLE = {'label': 'NO CUMPLE', 'color': 'gray', 'nota': 1}
    NINGUNA_CALIFICACION = {'label': 'NINGUNA CALIFICACION', 'color': 'yellow', 'nota': 0}

def clasificar_calificacion(promedio):
    for nota in CalificacionEnum:
        if nota.value['nota'] == int(promedio):
            return nota.value['label']

def traer_actividades(examen_id):
    examen = Examen.query.get(examen_id)

    if not examen:
        return jsonify(message="Examen no encontrado"), 404

    # Obtén la lista de actividades del examen
    actividades = examen.actividades_formativas or []

    # Modificamos el formato para incluir la descripción por defecto
    actividades_info = [{"descripcion": actividad} for actividad in actividades]

    return jsonify({"actividades": actividades_info})

# ... (código anterior)

def traer_calificaciones_por_examen(examen_id):
    calificaciones_examenes = CalificacionExamen.query.filter_by(examen_id=examen_id).all()

    if not calificaciones_examenes:
        return jsonify(message="No se encontraron calificaciones para el examen especificado"), 404

    calificaciones_serializables = []
    promedios_estudiantes = defaultdict(list)
    conteo_calificaciones = defaultdict(int)
    conteo_actividades_estudiantes = defaultdict(lambda: defaultdict(int))
    observaciones_totales = []
    evaluadores_totales = []  

  
    actividades_info = traer_actividades(examen_id).json['actividades']

    for calificacion_examen in calificaciones_examenes:
        evaluador = Evaluador.query.get(calificacion_examen.evaluador_id) 

        calificacion_serializable = {
            "id": calificacion_examen.id,
            "examen_id": calificacion_examen.examen_id,
            "evaluador_id": calificacion_examen.evaluador_id,
            "evaluador_nombre": evaluador.nombre_evaluador if evaluador else None,  
            "calificacion": [],
            "actividades": actividades_info  
        }

        for i, actividad_info in enumerate(calificacion_serializable["actividades"]):
            actividad = f"Actividad{i + 1}"
            actividad_info["calificacion"] = {}  
            actividad_info["descripcion_actividad"] = actividad  
        for estudiante in calificacion_examen.calificacion:
            nombre_estudiante = estudiante["nombre"]
            notas_estudiante = estudiante["calificacion"]["notas"]
            observaciones_estudiante = estudiante["calificacion"]["observaciones"]
            promedio_notas = round(sum(notas_estudiante) / len(notas_estudiante)) if len(notas_estudiante) > 0 else None

            calificacion_estudiante = {
                "nombre": nombre_estudiante,
                "calificacion": {
                    "notas": notas_estudiante,
                    "observaciones": observaciones_estudiante,
                    "promedio": promedio_notas
                }
            }

            calificacion_serializable["calificacion"].append(calificacion_estudiante)
            promedios_estudiantes[nombre_estudiante].append(promedio_notas)

            for i, nota in enumerate(notas_estudiante):
                actividad = f"Actividad{i + 1}"
                calificacion_actividad = clasificar_calificacion(nota)
                conteo_actividades_estudiantes[actividad][nombre_estudiante] = calificacion_actividad

                
                for actividad_info in calificacion_serializable["actividades"]:
                    if actividad_info["descripcion_actividad"] == actividad:
                        actividad_info["calificacion"][calificacion_actividad] = actividad_info["calificacion"].get(calificacion_actividad, 0) + 1

            observaciones_totales.extend(observaciones_estudiante)

        evaluadores_totales.append(evaluador.nombre_evaluador if evaluador else None)  

        calificaciones_serializables.append(calificacion_serializable)

    for estudiante, promedios in promedios_estudiantes.items():
        promedio_final = round(sum(promedios) / len(promedios)) if len(promedios) > 0 else None
        calificacion_final = clasificar_calificacion(promedio_final)
        conteo_calificaciones[calificacion_final] += 1

    conteo_actividades = defaultdict(dict)

    for actividad, estudiantes in conteo_actividades_estudiantes.items():
        conteo_por_actividad = Counter(estudiantes.values())
        for actividad_info in actividades_info:
            if actividad_info["descripcion_actividad"] == actividad:
                conteo_actividades[actividad]["descripcion_actividad"] = actividad_info["descripcion"]
                conteo_actividades[actividad].update(dict(conteo_por_actividad))

    return jsonify(
        calificaciones=calificaciones_serializables,
        conteo=conteo_calificaciones,
        conteo_actividades=conteo_actividades,
        observaciones_totales=observaciones_totales,
        evaluadores_totales=evaluadores_totales
    )

