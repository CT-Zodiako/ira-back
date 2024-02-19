from ...db import db
from flask import jsonify
from ...models.examen.examen_model import Examen
from ...models.evaluador.evaluador_model import Evaluador
import os
import pandas as pd


def agregar_examen(data):
    try:
        programa_id = data.get('programa_id')
        proyecto_integrador = data.get('proyecto_integrador')
        actividades_formativas = data.get('actividades_formativas')
        estudiantes = data.get('estudiantes')
        resultado_aprendizaje_id = data.get('resultado_aprendizaje_id')
        evaluadores_ids = data.get('evaluadores_ids')
        
        if not (programa_id and proyecto_integrador and actividades_formativas and estudiantes and resultado_aprendizaje_id and evaluadores_ids):
            return jsonify({'mensaje': 'Faltan campos obligatorios en los datos'}), 400

        examen = Examen(programa_id=programa_id, proyecto_integrador=proyecto_integrador,
                        actividades_formativas=actividades_formativas, estudiantes=estudiantes,
                        resultado_aprendizaje_id=resultado_aprendizaje_id)

        evaluadores = Evaluador.query.filter(
            Evaluador.id.in_(evaluadores_ids)).all()
        
        if len(evaluadores) != len(evaluadores_ids):
            return jsonify({'mensaje': 'Uno o más evaluadores no existen'}), 400
        
        examen.evaluadores_relacion = evaluadores

        db.session.add(examen)
        db.session.commit()

        return jsonify({'mensaje': 'Examen creado con exito'}), 201

    except Exception as e:
        return jsonify({'mensaje': 'Fallo para agregar examen', 'error': f'{e}'}), 500


def cargar_archivo(archivo):
    try:
        from ... import create_app
        app = create_app()
        if archivo:
            
            archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], archivo.filename))
        
            ruta_archivo_xlsx = os.path.join(app.config['UPLOAD_FOLDER'], archivo.filename)
            df = pd.read_excel(ruta_archivo_xlsx)

            datos_json = df.to_json(orient='records')
            
            os.remove(ruta_archivo_xlsx)

            return datos_json
        else:
            return jsonify({'mensaje': 'No hay datos de estudiantes'}), 400
    except Exception as e:
        print(f"Error al cargar el archivo: {str(e)}")
        return jsonify({'mensaje': 'Error al cargar el archivo', 'error': str(e)}), 500

    
def obtener_examenes():
    try:
        # Query all exams from the Examen table
        examenes = Examen.query.all()

        # Convert the list of exams to a JSON response
        examenes_json = jsonify(examenes)

        return examenes_json, 200

    except Exception as e:
        return jsonify({'mensaje': 'Error al obtener los exámenes', 'error': str(e)}), 500
    

def editar_examen(id, data):
    try:
        examen = get_examen_by_id(id)
        if not examen:
            return jsonify({'mensaje': 'Examen no encontrado'}), 404

        programa_id = data.get('programa_id')
        print(programa_id)
        proyecto_integrador = data.get('proyecto_integrador')
        actividades_formativas = data.get('actividades_formativas')
        estudiantes = data.get('estudiantes')
        resultado_aprendizaje_id = data.get('resultado_aprendizaje_id')
        evaluadores_ids = data.get('evaluadores_ids')

        if programa_id is not None:
            examen.programa_id = programa_id
        if proyecto_integrador is not None:
            examen.proyecto_integrador = proyecto_integrador
        if actividades_formativas is not None:
            examen.actividades_formativas = actividades_formativas
        if estudiantes is not None:
            examen.estudiantes = estudiantes
        if resultado_aprendizaje_id is not None:
            examen.resultado_aprendizaje_id = resultado_aprendizaje_id
        if evaluadores_ids is not None:
            evaluadores = Evaluador.query.filter(
                Evaluador.id.in_(evaluadores_ids)).all()
            if len(evaluadores) != len(evaluadores_ids):
                return jsonify({'mensaje': 'Uno o más evaluadores no existen'}), 400
            examen.evaluadores_relacion = evaluadores

        db.session.commit()

        return jsonify({'mensaje': 'Examen actualizado con éxito'}), 200

    except Exception as e:
        return jsonify({'mensaje': 'Fallo para actualizar examen', 'error': f'{e}'}), 500
    
def get_examen_by_id(id):
    try:
        examen = Examen.query.get(id)
        if not examen:
            return None
        return examen
    except Exception as e:
        print(f'Error al obtener el examen: {e}')
        return None

def eliminar_examen(id):
    try:
        examen = Examen.query.get(id)
        if not examen:
            return jsonify({'mensaje': 'Examen no encontrado'}), 404

        db.session.delete(examen)
        db.session.commit()

        return jsonify({'mensaje': 'Examen eliminado con éxito'}), 200

    except Exception as e:
        return jsonify({'mensaje': 'Fallo para eliminar examen', 'error': f'{e}'}), 500
    
    
def get_examen_by_id_db(id):
    try:
        examen = Examen.query.get(id)
        if not examen:
            return jsonify({'mensaje': 'Examen no encontrado'}), 404
        return jsonify(examen.to_dict()), 200  # Asegúrate de que tu modelo Examen tiene un método to_dict
    except Exception as e:
        print(f'Error al obtener el examen: {e}')
        return jsonify({'mensaje': 'Error al obtener el examen', 'error': f'{e}'}), 500