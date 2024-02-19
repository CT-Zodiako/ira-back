from ...db import db


class Programa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    examenes = db.relationship('Examen', backref='programa', lazy=True)

    def __init__(self, nombre, ):
        self.nombre = nombre
