from ...db import db

examen_evaluador_tabla = db.Table(
    'examen_evaluador_tabla',
    db.Column('examen_id', db.Integer, db.ForeignKey('examen.id')),
    db.Column('evaluador_id', db.Integer, db.ForeignKey('evaluador.id'))
)
