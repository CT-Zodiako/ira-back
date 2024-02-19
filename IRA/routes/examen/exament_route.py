from flask import Blueprint, request, jsonify
from ...controller.examen.examen_controller import get_examen_by_id_db, eliminar_examen,agregar_examen, cargar_archivo, obtener_examenes, editar_examen
from ...auth import admin_required
from ...models.examen.examen_model import Examen
import json

examen_blueprint = Blueprint('examen', __name__)


@examen_blueprint.route('/crear_examen', methods=['POST'])
# @admin_required
def crear_examen():
    data = request.json
    return agregar_examen(data)

@examen_blueprint.route('/ruta_de_carga_de_archivos', methods=['POST'])
@admin_required
def cargar_excel():
    archivo = request.files['archivo']
    return cargar_archivo(archivo)

@examen_blueprint.route('/examenes', methods=['GET'])
def obtener_todos_examenes():
    try:
        # Consultar todos los exámenes de la tabla Examen
        examenes = Examen.query.all()

        # Convertir objetos Examen a diccionarios
        examenes_dicts = [examen.to_dict() for examen in examenes]

        # Serializar la lista de diccionarios a JSON
        examenes_json = jsonify(examenes_dicts)

        return examenes_json, 200

    except Exception as e:
        return jsonify({'mensaje': 'Error al obtener los exámenes', 'error': str(e)}), 500
    
@examen_blueprint.route("/actividades/<int:examen_id>", methods=["GET"])
def traer_actividades(examen_id):
    examen = Examen.query.get(examen_id)

    if not examen:
        return jsonify(message="Examen no encontrado"), 404

    # Obtén la lista de actividades del examen
    actividades = examen.actividades_formativas or []

    # Modificamos el formato para incluir la descripción por defecto
    actividades_info = [{"descripcion": actividad} for actividad in actividades]

    return jsonify({"actividades": actividades_info})

@examen_blueprint.route('/editar_examen/<int:id>', methods=['PUT'])
# @admin_required
def editar_ruta_examen(id):
    data = request.json
    return editar_examen(id, data)

@examen_blueprint.route('/eliminar_examen/<int:id>', methods=['DELETE'])
# @admin_required
def eliminar_ruta_examen(id):
    return eliminar_examen(id)

@examen_blueprint.route('/examen/<int:id>', methods=['GET'])
def obtener_examen_por_id(id):
    return get_examen_by_id_db(id)