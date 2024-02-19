from ...db import db
from ...models.resultados_aprendizaje.resultados_aprendizaje_model import ResultadoAprendizaje
from ...models.resultados_aprendizaje.schemas import ResultadoAprendizajeSchema,TraerResultadoSchema
from flask import jsonify



def crear_resultado_aprendizaje(data):
    try:
        sResultado = ResultadoAprendizajeSchema()
        resultado = sResultado.load(data)

        db.session.add(resultado)
        db.session.commit()

        return {
            'status': 201,
            'mensaje': 'Resultado de aprendizaje creado exitosamente',
        }

    except Exception as e:
        return {
            'status': 500,
            'mensaje': 'Fallo al crear resultado de aprendizaje',
            'error': str(e)
        }


def traer_resultados_aprendizaje():
    try:
        sResultado = TraerResultadoSchema(many=True)
        resultados = ResultadoAprendizaje.query.all()


        data = sResultado.dump(resultados)
        return {
            'status': 200,
            'mensaje' : 'Resultados de aprendizaje obtenidos exitosamente',
            'data': data
        }

    except Exception as e:
        return {
            'status': 500,
            'mensaje' : 'Fallo al obtener resultados de aprendizaje',
            'error': f'Ocurrió un error interno en el controllador'
        }
      

def cambiar_estado_resultado_db(resultado_id):
    try:
        resultado = ResultadoAprendizaje.query.get(resultado_id)

        if resultado is None:
            return jsonify({'mensaje': 'Resultado de aprendizaje no encontrado', 'status': 404}), 404

        resultado.estado = not resultado.estado

        db.session.commit()

        mensaje_estado = 'desactivado' if not resultado.estado else 'activado'
        return jsonify({'mensaje': f'Estado del resultado de aprendizaje {mensaje_estado} exitosamente', 'status': 200}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje': 'Fallo al cambiar el estado del resultado de aprendizaje', 'error': str(e), 'status': 500}), 500