from ...configuracion_marshmallow import ma
from ...models.calificacion.calificacion_model import CalificacionExamen

class CalificacionExamenSchema(ma.SQLAlchemySchema):
    class Meta:
        model = CalificacionExamen
        fields = ("id", "calificacion", "examen_id", "evaluador_id")
        load_instance = True

