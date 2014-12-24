from flask import Blueprint, request, current_app, render_template
from .models import Event, Order
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
