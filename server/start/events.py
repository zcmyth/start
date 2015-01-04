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
    ).all()
    return render_template('status.html', orders=orders)


@bp.route('/ticketstatusxuning/<int:id>', methods=['GET'])
def get_ticket_order_status(id):
    orders = TicketOrder.query.filter_by(
        ticket_id=id,
        status='PAID'
    ).all()
    return render_template('ticket_status.html', orders=orders)
