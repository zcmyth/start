from flask import Blueprint, request, current_app, url_for, redirect
from .models import Order, Event
from .response import Response

bp = Blueprint('orders', __name__)


@bp.route('', methods=['POST'])
def create_order():
    data = request.get_json()
    event = Event.query.get(data['event_id'])
    if not event:
        return Response.error('Invalid event')

    total = (event.bus + int(data['lift']) * event.lift
                       + int(data['rental']) * event.rental
                       + int(data['lesson']) * event.lesson)
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

    kw = {
        'amt': total,
        'currencycode': 'USD',
        'returnurl': url_for(
            'orders.paypal_confirm', order_id=order.id, _external=True),
        'cancelurl': url_for(
            'ngapp.home', _external=True) + '#/' + data['event_id'],
        'paymentaction': 'Sale'
    }

    setexp_response = current_app.paypal.set_express_checkout(**kw)
    order.paypal_token = setexp_response.token
    return Response.success(
        current_app.paypal.generate_express_checkout_redirect_url(
            setexp_response.token))


@bp.route('/confirm', methods=['GET'])
def paypal_confirm():
    token = request.args.get('token', '')

    order = Order.query.get(request.args['order_id'])
    if not order:
        return 'Invalid order id'
    if order.paypal_token != token:
        return 'Invalid paypal token'

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
        data = current_app.paypal.do_express_checkout_payment(**kw)
        checkout_response = current_app \
            .paypal.get_express_checkout_details(token=token)
        if checkout_response['CHECKOUTSTATUS'] == 'PaymentActionCompleted':
            order.status = 'PAID'
        return """
            Awesome! Thank you for your %s %s purchase.<br/>
            An email will be sent to your to confirm this order.
        """ % (checkout_response['AMT'], checkout_response['CURRENCYCODE'])
    return 'Something wrong in Paypal'


@bp.route("/status/<string:token>")
def paypal_status(token):
    checkout_response = current_app.paypal.get_express_checkout_details(
        token=token)

    if checkout_response['CHECKOUTSTATUS'] == 'PaymentActionCompleted':
        # Here you would update a database record.
        return """
            Awesome! Thank you for your %s %s purchase.<br/>
            An email will be sent to your to confirm this order.
        """ % (checkout_response['AMT'], checkout_response['CURRENCYCODE'])
    else:
        return """
            Oh no! PayPal doesn't acknowledge the transaction.
            Here's the status:
            <pre>
                %s
            </pre>
        """ % checkout_response['CHECKOUTSTATUS']