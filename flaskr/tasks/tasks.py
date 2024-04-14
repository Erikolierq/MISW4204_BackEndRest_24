from celery import shared_task
from modelos import Flight

@shared_task
def process_reservation(reservation_data):
    flight_id = reservation_data['flight_id']
    number_of_passengers = reservation_data['number_of_passengers']

    flight = Flight.query.get(flight_id)

    if flight and flight.available_seats >= number_of_passengers:
        flight.available_seats -= number_of_passengers
        flight.save()
        return True
    else:
        return False
