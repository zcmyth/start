import uuid
from flask import Blueprint, request, current_app, url_for, redirect, render_template
from datetime import datetime, date
from .models import Order, Event
from .response import Response
from paypal.exceptions import PayPalAPIResponseError

bp = Blueprint('orders', __name__)

_ITEMS = ['bus', 'lift', 'rental', 'beginner', 'helmet']


@bp.route('', methods=['POST'])
def create_order():
    data = request.get_json()
    event = Event.query.get(data['event_id'])
    if not event:
        return Response.error('Invalid event')

    if event.ticket_left < 1:
        return Response.error('Sold out')

    if event.status == 'INACTIVE':
        return Response.error('The order system has been closed. If you have any questions, please contact info@startnewyork.us')

    if event.event_date < date.today():
        return Response.error('Event has finished')

    if int(data['bus']) < 1 and int(data['lift']) < 6:
        return Response.error('Group tickets requires mininum 6 tickets')

    total = 0
    for item in _ITEMS:
        if (item in data) and int(data[item]) > 0:
            total += (int(data[item])) * getattr(event, item)
    order = Order(
        id=str(uuid.uuid1()),
        event_id=data['event_id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        bus=data['bus'],
        lift=data.get('lift', 0),
        beginner=data.get('beginner', 0),
        rental=data.get('rental', 0),
        helmet=data.get('helmet', 0),
        location=data['location'],
        status='PENDING',
        create_time=datetime.utcnow(),
        total=total,
        rental_type=data.get('rental_type', ''),
        checked_in=False,
        ticket_picked=False
    )

    kw = {
        'PAYMENTREQUEST_0_AMT': total,
        'PAYMENTREQUEST_0_PAYMENTACTION': 'Sale',
        'SOLUTIONTYPE': 'Sole',
        'currencycode': 'USD',
        'returnurl': url_for(
            'orders.paypal_confirm', order_id=order.id, _external=True),
        'cancelurl': url_for(
            'ngapp.home', _external=True) + '#/' + data['event_id'],
    }

    n = 0
    template = 'L_PAYMENTREQUEST_0_%s%s'
    for item in _ITEMS:
        if (item in data) and int(data[item]) > 0:
            kw[template % ('NAME', n)] = item
            kw[template % ('AMT', n)] = getattr(event, item)
            kw[template % ('QTY', n)] = int(data[item])
            n = n + 1

    try:
        setexp_response = current_app.paypal.set_express_checkout(**kw)
        order.paypal_token = setexp_response.token
        current_app.db.session.add(order)

        return Response.success(
            current_app.paypal.generate_express_checkout_redirect_url(
                setexp_response.token) + '&useraction=commit')
    except PayPalAPIResponseError as e:
        current_app.logger.warning(str(e))
        return Response.error(str(e))


@bp.route('/confirm', methods=['GET'])
def paypal_confirm():
    token = request.args.get('token', '')

    order = Order.query.get(request.args['order_id'])
    if not order:
        return 'Invalid order id'
    if order.paypal_token != token:
        return 'Invalid paypal token'
    if order.event.ticket_left < 1:
        return 'Sold out'
    # TODO(zhangchun): ideally we should have a lock here to make sure
    # only one payment will be accept each time

    getexp_response = current_app.paypal.get_express_checkout_details(
        token=token)
    if getexp_response['ACK'] == 'Success':
        kw = {
            'amt': getexp_response['AMT'],
            'paymentaction': 'Sale',
            'payerid': getexp_response['PAYERID'],
            'token': token,
            'currencycode': getexp_response['CURRENCYCODE']
        }
        current_app.paypal.do_express_checkout_payment(**kw)
        checkout_response = current_app \
            .paypal.get_express_checkout_details(token=token)
        if checkout_response['CHECKOUTSTATUS'] == 'PaymentActionCompleted':
            order.status = 'PAID'
        return redirect(url_for('ngapp.home', _external=True) + '#/order_confirm/' + order.id)
    return 'Something wrong in Paypal'


@bp.route('/<order_id>')
def get_order(order_id):
    order = Order.query.get(order_id)
    result = {
        'first_name': order.first_name,
        'last_name': order.last_name,
        'description': order.event.description,
        'qrcode': url_for('orders.order_status', order_id=order.id, _external=True),
        'bus': order.bus,
        'lift': order.lift,
        'beginner': order.beginner,
        'rental': order.rental,
        'helmet': order.helmet
    }
    return Response.success(result)


@bp.route('/<order_id>/status')
def order_status(order_id):
    order = Order.query.get(order_id)
    if order.status != 'PAID':
        return 'Invalid order'
    return render_template('order_status.html', order=order)


@bp.route('/<order_id>/bus', methods=['POST'])
def update_order_status_bus(order_id):
    order = Order.query.get(order_id)
    if order.status != 'PAID':
        return Response.error('Invalid order')
    order.checked_in = not order.checked_in
    return Response.success()


@bp.route('/<order_id>/ticket', methods=['POST'])
def update_order_status_ticket(order_id):
    order = Order.query.get(order_id)
    if order.status != 'PAID':
        return Response.error('Invalid order')
    order.ticket_picked = not order.ticket_picked
    return Response.success()
