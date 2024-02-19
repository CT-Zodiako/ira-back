from flask import Blueprint, request, jsonify
from ...controller.login.login_controller import verificar_conectar
from ...models.evaluador.evaluador_model import Evaluador
from ...auth import bcrypt, jwt
from flask_jwt_extended import create_access_token

login_blueprint = Blueprint('login', __name__)


@login_blueprint.route('/conectar', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    evaluador = Evaluador.query.filter_by(numero_identificacion=username).first()

    if evaluador is None:
        return jsonify({"message": "Usuario no encontrado"}), 404

    if bcrypt.check_password_hash(evaluador.contrasenna, password):

        # Crear el token con los datos del usuario en la carga útil
        usuario_data = {
            "id": evaluador.id,
            "nombre": evaluador.nombre_evaluador,
            "rol": evaluador.rol
        }
        print(usuario_data)
        access_token = create_access_token(identity=usuario_data)

        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Credenciales incorrectas"}), 401
