
from ...db import db
from ...models.relaciones.relacion_examen_evaluador import examen_evaluador_tabla
from ...models.programa.programas_model import Programa

class Examen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    programa_id = db.Column(db.Integer, db.ForeignKey(Programa.id), nullable=False)
    proyecto_integrador = db.Column(db.String(255), nullable=False)
    actividades_formativas = db.Column(db.JSON)
    estudiantes = db.Column(db.JSON)
    resultado_aprendizaje_id = db.Column(db.Integer, db.ForeignKey('resultado_aprendizaje.id'))
    estado = db.Column(db.Boolean, default=False)
    evaluadores_relacion = db.relationship('Evaluador', secondary=examen_evaluador_tabla, back_populates='examenes_evaluador_relacion')

    def __init__(self, programa_id, proyecto_integrador, actividades_formativas, estudiantes, resultado_aprendizaje_id):
        self.programa_id = programa_id
        self.proyecto_integrador = proyecto_integrador
        self.actividades_formativas = actividades_formativas
        self.estudiantes = estudiantes
        self.resultado_aprendizaje_id = resultado_aprendizaje_id

    def to_dict(self):
        return {
            'id': self.id,
            'programa_id': self.programa_id,
            'proyecto_integrador': self.proyecto_integrador,
            'actividades_formativas': self.actividades_formativas,
            'estudiantes': self.estudiantes,
            'resultado_aprendizaje_id': self.resultado_aprendizaje_id,
            'estado': self.estado,
            'evaluadores_relacion': [evaluador.id for evaluador in self.evaluadores_relacion],
            'nombres_evaluadores': self.get_nombres_evaluadores(),  # Agrega esta línea para obtener los nombres de los evaluadores
        }

    def get_nombres_evaluadores(self):
        return [evaluador.nombre_evaluador for evaluador in self.evaluadores_relacion]
    
    def obtener_correos_evaluadores_por_id(self, examen_id):
        # Buscar el examen por su ID
        examen = Examen.query.get(examen_id)

        if not examen:
            return 'Examen no encontrado'

        # Obtener los correos de los evaluadores asociados al examen
        correos_evaluadores = [evaluador.correo_evaluador for evaluador in examen.evaluadores_relacion]

        return correos_evaluadores
