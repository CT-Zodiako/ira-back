from ...db import db
from ...models.calificacion.schema import CalificacionExamenSchema
from flask import jsonify
from ...models.examen.examen_model import Examen
from enum import Enum
from ...models.calificacion.calificacion_model import CalificacionExamen



def guardar_calificacion_db(data):
    try:
        sCalificacionExamen = CalificacionExamenSchema()
        CalificacionExamen = sCalificacionExamen.load(data)
        
        db.session.add(CalificacionExamen)
        db.session.commit()
            
        return {
            'status': 201,
            'mensaje': 'Calificacion creada exitosamente',
        }

    except Exception as e:
        return {
            'status': 500,
            'mensaje': 'Fallo al crear calificacion',
            'error': str(e)
        }

def actividades_examen(id_examen):
    try:
        examen = Examen.query.filter_by(id=id_examen).first()
        
        if examen:
            return jsonify(examen.actividades_formativas)
        else:
            return jsonify({"error": "Examen no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def calificaciones_by_id_db(id_examen):
    try:
        examen = CalificacionExamen.query.filter_by(examen_id=id_examen).first()
        
        if examen:
            return jsonify(examen.calificacion)
        else:
            return jsonify({"error": "Examen no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def enum_calificacion():
    try:
        enum_options = [{'label': calificacion.value['label'], 'value': calificacion.name, 'color': calificacion.value['color'], 'nota': calificacion.value['nota']} for calificacion in CalificacionEnum]
        return enum_options
    except Exception as e:
        return jsonify({"error en enum calificaiones": str(e)}), 500



class CalificacionEnum(Enum):
    EXCELENTE = {'label': 'EXCELENTE', 'color': '#9AFE2E', 'nota': 5}
    SOBRESALIENTE = {'label': 'SOBRESALIENTE', 'color': '#2E64FE', 'nota': 4}
    SUFICIENTE = {'label': 'SUFICIENTE', 'color': '#FACC2E', 'nota': 3}
    INSUFICIENTE = {'label': 'INSUFICIENTE', 'color': '#FE2E2E' , 'nota': 2}
    NO_CUMPLE = {'label': 'NO CUMPLE', 'color': '#A4A4A4', 'nota': 1}
    NINGUNA_CALIFICACION = {'label': 'NINGUNA CALIFICACION', 'color': '#F7FE2E', 'nota': 0}
   
