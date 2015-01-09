from flask import Blueprint, render_template
from .models import Event, Order, TicketOrder
from .response import Response

bp = Blueprint('events', __name__)


@bp.route('/<int:id>', methods=['GET'])
def get_event(id):
    return Response.success(Event.query.get(id))


@bp.route('/eventstatusxuning/<int:id>', methods=['GET'])
def get_event_order_status(id):
    orders = Order.query.filter_by(
        event_id=id,
        status='PAID'
    ).order_by(Order.location).order_by(Order.create_time).all()
    s = {
        'bus': 0,
        'lift': 0,
        'rental': 0,
        'lesson': 0,
        'total': 0
    }
    for order in orders:
        if order.bus:
            s['bus'] += 1
        if order.lift:
            s['lift'] += 1
        if order.rental:
            s['rental'] += 1
        if order.lesson:
            s['lesson'] += 1
        s['total'] += order.total
    return render_template('status.html', orders=orders, status=s)


@bp.route('/ticketstatusxuning/<int:id>', methods=['GET'])
def get_ticket_order_status(id):
    orders = TicketOrder.query.filter_by(
        ticket_id=id,
        status='PAID'
    ).all()
    return render_template('ticket_status.html', orders=orders)
