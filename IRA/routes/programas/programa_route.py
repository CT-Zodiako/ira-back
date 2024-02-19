from flask import Blueprint, request, jsonify
from ...controller.programa.programa_controller import traer_programas_db
from ...auth import admin_required, evaluador_required

programa_blueprint = Blueprint('programa', __name__)


@programa_blueprint.route('/', methods=['GET'])
@admin_required
def traer_programas():
    resultados = traer_programas_db()
    return jsonify(resultados)
