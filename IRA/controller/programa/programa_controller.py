from ...models.programa.programas_model import Programa
from ...models.programa.schemas import TraerProgramaSchema






def traer_programas_db():
    try:
        sResultado = TraerProgramaSchema(many=True)
        resultados = Programa.query.all()


        data = sResultado.dump(resultados)
        return {
            'status': 200,
            'mensaje' : 'Programas obtenidos exitosamente',
            'data': data
        }

    except Exception as e:
        return {
            'status': 500,
            'mensaje' : 'Fallo al obtener Programas',
            'error': f'Ocurrió un error interno en el controllador'
        }
      
