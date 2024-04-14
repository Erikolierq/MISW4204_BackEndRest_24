from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum


db = SQLAlchemy()



class Vuelo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origen = db.Column(db.String(100), nullable=False)
    destino = db.Column(db.String(100), nullable=False)
    hora_salida = db.Column(db.String(100), nullable=False)
    sillas_disponibles = db.Column(db.Integer, nullable=False)

class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vuelo_id = db.Column(db.Integer, db.ForeignKey('vuelo.id'), nullable=False)
    nombre_pasajero = db.Column(db.String(100), nullable=False)
    correo_pasajero = db.Column(db.String(100), nullable=False)
    num_pasajeros = db.Column(db.Integer, nullable=False)

    vuelo = db.relationship('Vuelo', backref=db.backref('reservas', lazy=True))
    

class VueloSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Vuelo
         include_relationships = True
         load_instance = True

class ReservaSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Reserva
         include_relationships = True
         load_instance = True