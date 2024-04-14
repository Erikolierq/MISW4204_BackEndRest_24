import json
from flask import Response, request
from ..modelos import db, Vuelo, VueloSchema, Reserva, ReservaSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

Vuelo_Schema = VueloSchema()
Reserva_Schema = ReservaSchema()



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
            response = Response(response=json.dumps({"error": "Faltan campos requeridos"}), status=400, mimetype='application/json')
            return response
        vuelo = Vuelo.query.get(reserva_data['vuelo_id'])
        if not vuelo:
            response = Response(response=json.dumps({"error": "El vuelo no existe"}), status=404, mimetype='application/json')
            return response
        if vuelo.sillas_disponibles < reserva_data['num_pasajeros']:
            response = Response(response=json.dumps({"error": "No hay suficientes sillas en el vuelo"}), status=400, mimetype='application/json')
            return response
        nueva_reserva = Reserva(vuelo_id=reserva_data['vuelo_id'],
                            nombre_pasajero=reserva_data['nombre_pasajero'],
                            correo_pasajero=reserva_data['correo_pasajero'],
                            num_pasajeros=reserva_data['num_pasajeros'])
        vuelo.sillas_disponibles -= reserva_data['num_pasajeros']
        db.session.add(nueva_reserva)
        db.session.commit()
        response = Response(response=json.dumps(Reserva_Schema.dump(nueva_reserva)), status=201, mimetype='application/json')
        return response