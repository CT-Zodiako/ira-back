from ...db import db
from flask import jsonify
from ...models.evaluador.evaluador_model import Evaluador
from ...models.examen.examen_model import Examen
from ...models.evaluador.schemas import EvaluadorSchema, ExamenEvaluadorSchema
from sqlalchemy.exc import IntegrityError
from ...models.relaciones.relacion_examen_evaluador import examen_evaluador_tabla
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required


def agregar_evaluador(data):
    try:
        nombre_evaluador = data.get('nombre_evaluador')
        correo = data.get('correo')
        numero_identificacion = data.get('numero_identificacion')
        contrasenna = data.get('contrasenna')
        telefono = data.get('telefono')

        if not (nombre_evaluador and correo and numero_identificacion and contrasenna and telefono):
            return jsonify({'mensaje': 'Todos los campos son obligatorios.', 'status': 400}), 400

        if Evaluador.query.filter_by(correo=correo).first():
            db.session.rollback()
            return jsonify({'mensaje': 'El correo ya está en uso.', 'status': 400}), 400
        
        if Evaluador.query.filter_by(numero_identificacion=numero_identificacion).first():
            db.session.rollback()
            return jsonify({'mensaje': 'El usuario ya está en uso.', 'status': 400}), 400

        nuevo_evaluador = Evaluador(nombre_evaluador=nombre_evaluador, correo=correo,
                                    numero_identificacion=numero_identificacion, contrasenna=contrasenna, telefono=telefono)

        db.session.add(nuevo_evaluador)
        db.session.commit()

        return jsonify({'mensaje': 'Evaluador creado con éxito', 'status': 201}), 201

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'mensaje': 'Error de integridad de la base de datos.', 'status': 500}), 500

    except Exception as e:
        return jsonify({'mensaje': 'Fallo al crear el evaluador', 'status': 500}), 500


def traer_evaluadores_db():
    try:
        sEvaluador = EvaluadorSchema(many=True)
        evaluadores = Evaluador.query.all()
        data = sEvaluador.dump(evaluadores)

        return jsonify({'mensaje': 'Evaluadores obtenidos con éxito', 'data': data, 'status': 200}), 200

    except Exception as e:
        return jsonify({'mensaje': 'Fallo al obtener evaluadores', 'error': str(e), 'status': 500}), 500


def traer_evaluadores_examen_db(evaluador_id):
    try:
        sExamenEvaluador = ExamenEvaluadorSchema(many=True)
        examenEvaluador = Evaluador.query.get(evaluador_id)

        if examenEvaluador is None:
            return jsonify({'message': 'Evaluador no encontrado'}), 404

        examenes = examenEvaluador.examenes_evaluador_relacion
        data = sExamenEvaluador.dump(examenes)

        return jsonify({'mensaje': 'Examenes del evaluador con exito', 'data': data}), 200

    except Exception as e:
        return jsonify({'message': 'Error al obtener los examenes del evaluador', 'error': str(e)}), 500

def traer_estudiantes_examen_db(examen_id):
    try:
        examen = Examen.query.get(examen_id)

        if examen is None:
            return jsonify({'message': 'Examen no encontrado'}), 404
        estudiantes = examen.estudiantes
        data = {'estudiantes': estudiantes}

        return jsonify({'mensaje': 'Estudiantes del examen con éxito', 'data': data}), 200

    except Exception as e:
        return jsonify({'message': 'Error al obtener los estudiantes del examen', 'error': str(e)}), 500




def eliminar_evaluador_sf(evaluador_id):
    try:
        evaluador = Evaluador.query.get_or_404(evaluador_id)
    
        evaluaciones_relacionadas = db.session.query(examen_evaluador_tabla).filter_by(evaluador_id=evaluador_id).count()
        if evaluaciones_relacionadas > 0:
            evaluador.estado = False 
            db.session.commit()
            return jsonify({'mensaje': 'El evaluador se ha desactivado debido a las evaluaciones relacionadas', 'status': 200}), 200

        db.session.delete(evaluador)
        db.session.commit()

        return jsonify({'mensaje': 'Evaluador eliminado con éxito', 'status': 200}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje': 'Fallo al eliminar evaluador', 'error': str(e), 'status': 500}), 500
  
def traer_evaluador_por_id(evaluador_id):
    try:
        sEvaluador = EvaluadorSchema()
        evaluador = Evaluador.query.filter_by(id=evaluador_id).first()

        if evaluador:
            data = sEvaluador.dump(evaluador)
            return jsonify({'mensaje': 'Evaluador obtenido con éxito', 'data': data, 'status': 200}), 200
        else:
            return jsonify({'mensaje': 'No se encontró un evaluador con esa identificación', 'status': 404}), 404

    except Exception as e:
        return jsonify({'mensaje': 'Fallo al obtener el evaluador', 'error': str(e), 'status': 500}), 500


def actualizar_evaluador_db(data,evaluador_id):
    
    evaluador = Evaluador.query.filter_by(id=evaluador_id).first()
    
    try:
        numero_identificacion_nuevo= data.get('nuevo_numero_identificacion')
        if not numero_identificacion_nuevo:
            numero_identificacion_nuevo = evaluador.numero_identificacion

        nuevo_nombre_evaluador = data.get('nuevo_nombre_evaluador')
        if not nuevo_nombre_evaluador:
            nuevo_nombre_evaluador = evaluador.nombre_evaluador

        nuevo_correo = data.get('nuevo_correo')
        if not nuevo_correo:
             nuevo_correo = evaluador.correo

        nueva_contrasena = data.get('nueva_contrasena')
        if not nueva_contrasena:
            nueva_contrasena = evaluador.contrasenna

        nuevo_telefono = data.get('nuevo_telefono')
        if not nuevo_telefono:
            nuevo_telefono = evaluador.telefono

        

        if evaluador:
            evaluador.numero_identificacion = numero_identificacion_nuevo
            evaluador.nombre_evaluador = nuevo_nombre_evaluador
            evaluador.correo = nuevo_correo
            evaluador.contrasenna = generate_password_hash(nueva_contrasena)
            evaluador.telefono = nuevo_telefono

            db.session.commit()

            return jsonify({'mensaje': 'Evaluador actualizado con éxito', 'status': 200}), 200
        else:
            return jsonify({'mensaje': 'No se encontró un evaluador con esa identificación', 'status': 404}), 404

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'mensaje': 'Error de integridad de la base de datos.', 'status': 500}), 500

    except Exception as e:
        return jsonify({'mensaje': 'Fallo al actualizar el evaluador', 'error': str(e), 'status': 500}), 500
