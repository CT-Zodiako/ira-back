from ...db import db
from flask import Blueprint, request, jsonify
from ...models.examen.examen_model import Examen
import smtplib
from email.mime.text import MIMEText

email_blueprint = Blueprint('email', __name__)


def configure_smtp_server():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("tryhardskill98@gmail.com", "ybpy hspa fzje jdzh")
    return server


def close_smtp_connection(server):
    server.quit()


def create_email_message(destinatario, asunto, cuerpo):
    msg = MIMEText(cuerpo)
    msg['Subject'] = asunto
    msg['From'] = "tryhardskill98@gmail.com"
    msg['To'] = destinatario
    return msg


def enviar_correo(destinatario, asunto, cuerpo):
    server = configure_smtp_server()
    msg = create_email_message(destinatario, asunto, cuerpo)
    server.sendmail("tryhardskill98@gmail.com", destinatario, msg.as_string())
    close_smtp_connection(server)

# Cambié el nombre de la función para evitar conflictos


@email_blueprint.route('/enviar_correo', methods=['POST'])
def enviar_correo_route():
    if request.method == 'POST':
        # Obtener la lista de destinatarios desde la base de datos o alguna fuente
        # Asume que el ID del examen está en el cuerpo de la solicitud
        examen_id = request.json.get('examen_id')
        destinatarios = obtener_destinatarios_por_examen(examen_id)

        # Detalles del mensaje
        asunto = "Tienes exámenes por calificar"
        cuerpo = "Estimado evaluador, tienes exámenes pendientes por calificar. Por favor, revisa tu cuenta para más detalles."

        # Enviar correos a cada destinatario
        for destinatario in destinatarios:
            enviar_correo(destinatario, asunto, cuerpo)

        return {
            'status': 200,
            'mensaje': 'Correos enviados correctamente'
        }

    return {
        'status': 400,
        'mensaje': 'No se realizó ninguna acción'
    }


def obtener_destinatarios_por_examen(examen_id):
    examen = Examen.query.get(examen_id)
    if not examen:
        return []
    print([evaluador.correo for evaluador in examen.evaluadores_relacion])
    return [evaluador.correo for evaluador in examen.evaluadores_relacion]


@email_blueprint.route('/cambiar_estado_resultado/<int:resultado_id>', methods=['PUT'])
def cambiar_estado_resultado(resultado_id):
    return cambiar_estado_resultado_db(resultado_id)


def cambiar_estado_resultado_db(resultado_id):
    try:
        resultado = Examen.query.get(resultado_id)

        if resultado is None:
            return jsonify({'mensaje': 'Resultado de aprendizaje no encontrado', 'status': 404}), 404

        resultado.estado = not resultado.estado

        db.session.commit()

        mensaje_estado = 'desactivado' if not resultado.estado else 'activado'
        return jsonify({'mensaje': f'Estado del resultado de aprendizaje {mensaje_estado} exitosamente', 'status': 200}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'mensaje': 'Fallo al cambiar el estado del resultado de aprendizaje', 'error': str(e), 'status': 500}), 500
