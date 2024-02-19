from ...configuracion_marshmallow import ma
from ...models.resultados_aprendizaje.resultados_aprendizaje_model import ResultadoAprendizaje

class ResultadoAprendizajeSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ResultadoAprendizaje
        fields = ("titulo", "descripcion")
        load_instance = True

class TraerResultadoSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ResultadoAprendizaje
        fields = ("titulo", "descripcion","estado","id")
        load_instance = True
