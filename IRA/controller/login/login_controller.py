from flask import Blueprint, request, jsonify
from ...models.evaluador.schemas import EvaluadorConrasenaSchema
from ...models.evaluador.evaluador_model import Evaluador


def verificar_conectar(usuario, contrasena):
    buscarEvaluador = Evaluador.query.filter_by(
        numero_identificacion=usuario).first()
    sEvaluador = EvaluadorConrasenaSchema()
    data = sEvaluador.dump(buscarEvaluador)

    if buscarEvaluador is None:
        return jsonify({'mensaje': 'Usuario no encontrado'})

    comparar_contrasena = Evaluador.verificar_contrasena(
        buscarEvaluador.contrasenna, contrasena)
    
    if comparar_contrasena is False:
        return jsonify({'mensaje': 'Contrseña o usuario incorrecto'})
    else:
        return jsonify({'mensaje': 'Conectado correcto usuario contraseña'})
    
