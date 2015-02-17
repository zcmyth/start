from flask import Blueprint, render_template
from .models import Event, Order
from .response import Response
from .httpauth import auth

bp = Blueprint('events', __name__)


@bp.route('/<int:id>', methods=['GET'])
def get_event(id):
    return Response.success(Event.query.get(id))


@bp.route('/<int:id>/status', methods=['GET'])
@auth.login_required
def get_event_order_status(id):
    event = Event.query.get(id)
    if not event:
        return 'Invalid event id'
    orders = Order.query.filter_by(
        event_id=id,
        status='PAID'
    ).order_by(Order.location).order_by(Order.last_name).all()
    s = {
        'bus': 0,
        'lift': 0,
        'rental': 0,
        'beginner': 0,
        'helmet': 0,
        'total': 0
    }
    for order in orders:
        if order.bus:
            s['bus'] += 1
        if order.lift:
            s['lift'] += 1
        if order.rental:
            s['rental'] += 1
        if order.beginner:
            s['beginner'] += 1
        if order.helmet:
            s['helmet'] += 1
        s['total'] += order.total

    return render_template(
        'status.html',
        name=event.description,
        orders=orders,
        status=s)
