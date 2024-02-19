from ...db import db

class ResultadoAprendizaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.Boolean, default=True)
    examenes = db.relationship('Examen', backref='resultado_aprendizaje', lazy='dynamic')


    def __init__(self, titulo, descripcion):
        self.titulo = titulo
        self.descripcion = descripcion
        
    
