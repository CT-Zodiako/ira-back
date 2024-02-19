from ...configuracion_marshmallow import ma
from ...models.programa.programas_model import Programa

class TraerProgramaSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Programa
        fields = ("id", "nombre")
        load_instance = True