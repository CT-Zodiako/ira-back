# app/helpers/respuestas.py


def generar_respuesta(status, mensaje, data=None):
    respuesta = {'status': status, 'mensaje': mensaje}
    if data is not None:
        respuesta['data'] = data
    return respuesta

def respuesta_exitosa(data=None, mensaje="Operación exitosa"):
    return generar_respuesta(200, mensaje, data)

def respuesta_error(status, mensaje="Error"):
    return generar_respuesta(status, mensaje)
