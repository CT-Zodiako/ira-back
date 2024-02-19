from flask import Blueprint, jsonify
from ...controller.informes.informes_controller import traer_calificaciones_por_examen
from ...models.calificacion.calificacion_model import CalificacionExamen
from ...auth import admin_required
from enum import Enum

informes_blueprint = Blueprint('informes', __name__)

@informes_blueprint.route('/traer_calificaciones/<int:examen_id>', methods=['GET'])
# @admin_required
def traer_calificaciones(examen_id):
    return traer_calificaciones_por_examen(examen_id)


class CalificacionEnum(Enum):
    EXCELENTE = {'label': 'EXCELENTE', 'color': 'green', 'nota': 5}
    SOBRESALIENTE = {'label': 'SOBRESALIENTE', 'color': 'blue', 'nota': 4}
    SUFICIENTE = {'label': 'SUFICIENTE', 'color': 'orange', 'nota': 3}
    INSUFICIENTE = {'label': 'INSUFICIENTE', 'color': 'red' , 'nota': 2}
    NO_CUMPLE = {'label': 'NO CUMPLE', 'color': 'gray', 'nota': 1}
    NINGUNA_CALIFICACION = {'label': 'NINGUNA CALIFICACION', 'color': 'yellow', 'nota': 0}

def procesar_calificaciones(calificacion_lista):
    conteo_calificaciones = {nota.value['label']: 0 for nota in CalificacionEnum}

    for elemento in calificacion_lista:
        if "calificacion" in elemento and "notas" in elemento["calificacion"]:
            notas = elemento["calificacion"]["notas"]
            promedio = sum(notas) / len(notas) if len(notas) > 0 else None
            elemento["calificacion"]["promedio"] = promedio
            for nota in CalificacionEnum:
                if nota.value['nota'] == int(promedio):
                    conteo_calificaciones[nota.value['label']] += 1

    return {"calificaciones": calificacion_lista, "conteo": conteo_calificaciones}

@informes_blueprint.route('/calificacion_by_id_examen/<int:examen_id>', methods=['GET'])
# @admin_required
def obtener_calificaciones_por_examen(examen_id):
    calificaciones_examenes = CalificacionExamen.query.filter_by(examen_id=examen_id).all()

    if not calificaciones_examenes:
        return jsonify(message="No se encontraron calificaciones para el examen especificado"), 404
    
    # Procesar calificaciones de todos los exámenes relacionados
    calificacion_lista = []
    for calificacion_examen in calificaciones_examenes:
        calificacion_lista.extend(calificacion_examen.calificacion)

    response_data = procesar_calificaciones(calificacion_lista)

    return jsonify(response_data)



