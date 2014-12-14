from flask import Blueprint, request, current_app
from .models import Order, Event
from .response import Response

bp = Blueprint('orders', __name__)


@bp.route('', methods=['POST'])
def create_order():
    data = request.get_json()
    event = Event.query.get(data['event_id'])
    if not event:
        return Response.error('Invalid event')

    total = event.bus + int(data['lift']) * event.lift + int(data['rental']) * event.rental + int(data['lesson']) * event.lesson
    order = Order(
        event_id=data['event_id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        email=data['email'],
        lift=data['lift'],
        rental=data['rental'],
        lesson=data['lesson'],
        status='PENDING',
        total=total
    )
    current_app.db.session.add(order)
    current_app.db.session.commit()
    return Response.success()