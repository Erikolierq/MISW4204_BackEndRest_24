import json
from flask import Response, request
from ..modelos import db, Vuelo, VueloSchema, Reserva, ReservaSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from celery import Celery

celery = Celery(__name__)
celery.conf.broker_url = 'amqp://guest:guest@localhost:5672/'

Vuelo_Schema = VueloSchema()
Reserva_Schema = ReservaSchema()

@celery.task
def crear_reserva(vuelo_id, nombre_pasajero, correo_pasajero, num_pasajeros):
    vuelo = Vuelo.query.get(vuelo_id)
    if not vuelo:
        return {"error": "El vuelo no existe"}
    if vuelo.sillas_disponibles < num_pasajeros:
        return {"error": "No hay suficientes sillas en el vuelo"}
    nueva_reserva = Reserva(vuelo_id=vuelo_id,
                            nombre_pasajero=nombre_pasajero,
                            correo_pasajero=correo_pasajero,
                            num_pasajeros=num_pasajeros)
    vuelo.sillas_disponibles -= num_pasajeros
    db.session.add(nueva_reserva)
    db.session.commit()
    return Reserva_Schema.dump(nueva_reserva)

class VistaVuelos(Resource):

    def post(self):
        nuevo_vuelo = Vuelo(origen=request.json["origen"], destino=request.json["destino"], hora_salida=request.json["hora_salida"], sillas_disponibles=request.json["sillas_disponibles"])
        db.session.add(nuevo_vuelo)
        db.session.commit()
        return Vuelo_Schema.dump(nuevo_vuelo)

    def get(self):
        return [Vuelo_Schema.dump(ca) for ca in Vuelo.query.all()]

class VistaReserva(Resource):

    def get(self, id_reserva):
        return Reserva_Schema.dump(Reserva.query.get_or_404(id_reserva))

    def put(self, id_reserva):
        reserva = Reserva.query.get_or_404(id_reserva)
        reserva.nombre_pasajero = request.json.get("nombre pasajero:",reserva.nombre_pasajero)
        reserva.correo_pasajero = request.json.get("correo pasajero",reserva.correo_pasajero)
        reserva.num_pasajeros = request.json.get("segundos",reserva.num_pasajeros)
        
        db.session.commit()
        return Reserva_Schema.dump(reserva)

    def delete(self, id_reserva):
        reserva = Reserva.query.get_or_404(id_reserva)
        db.session.delete(reserva)
        db.session.commit()
        return '',204


class VistaReservas(Resource):
    def get(self):
        return [Reserva_Schema.dump(ca) for ca in Reserva.query.all()]

    def post(self):
        reserva_data = request.json
        if not all(key in reserva_data for key in ['vuelo_id', 'nombre_pasajero', 'correo_pasajero', 'num_pasajeros']):
            return Response(response=json.dumps({"error": "Faltan campos requeridos"}), status=400, mimetype='application/json')
    
        # Envía la tarea Celery para manejar la creación de la reserva
        task = crear_reserva.delay(reserva_data['vuelo_id'], reserva_data['nombre_pasajero'], reserva_data['correo_pasajero'], reserva_data['num_pasajeros'])
    
        # Puedes devolver la información de la tarea, si lo deseas
        return Response(response=json.dumps({"task_id": task.id}), status=202, mimetype='application/json')