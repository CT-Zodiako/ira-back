from ...db import db
from ...models.examen.examen_model import Examen

class CalificacionExamen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calificacion = db.Column(db.JSON)
    examen_id = db.Column(db.Integer,nullable=False)
    evaluador_id = db.Column(db.Integer, nullable=False)
 
    

    def __init__(self, calificacion,examen_id,evaluador_id):
        self.calificacion = calificacion
        self.examen_id = examen_id
        self.evaluador_id = evaluador_id
