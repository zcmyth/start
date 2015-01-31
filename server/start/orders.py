import uuid
from flask import Blueprint, request, current_app, url_for, redirect,\
    render_template
from datetime import datetime, date
from .models import Order, Event
from .response import Response
from paypal.exceptions import PayPalAPIResponseError

bp = Blueprint('orders', __name__)


@bp.route('', methods=['POST'])
def create_order():
    # TODO(zhangchun): verify form data
    data = request.get_json()
    event = Event.query.get(data['event_id'])
    if not event:
        return Response.error('Invalid event')

    if event.ticket_left < 1:
        return Response.error('Sold out')

    if event.end_date < date.today():
        return Response.error('Event has finished')

    total = (int(data['bus']) * event.bus
             + int(data['lift']) * event.lift
             + int(data['rental']) * event.rental
             + int(data['beginner']) * event.beginner
             + int(data['helmet']) * event.helmet)
    order = Order(
        id=str(uuid.uuid1()),
        event_id=data['event_id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        email=data['email'],
        bus=data['bus'],
        lift=data['lift'],
        rental=data['rental'],
        helmet=data['helmet'],
        beginner=data['beginner'],
        location=data['location'],
        status='PENDING',
        create_time=datetime.utcnow(),
        total=total,
        rental_type=data.get('rental_type', '')
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
    if int(data['bus']) > 0:
        kw[template % ('NAME', n)] = 'Bus'
        kw[template % ('AMT', n)] = event.bus
        n = n + 1

    if int(data['lift']) > 0:
        kw[template % ('NAME', n)] = 'Lift'
        kw[template % ('AMT', n)] = event.lift
        n = n + 1

    if int(data['rental']) > 0:
        kw[template % ('NAME', n)] = 'Rental'
        kw[template % ('AMT', n)] = event.rental
        n = n + 1

    if int(data['beginner']) > 0:
        kw[template % ('NAME', n)] = 'Beginner package'
        kw[template % ('AMT', n)] = event.beginner
        n = n + 1

    if int(data['helmet']) > 0:
        kw[template % ('NAME', n)] = 'helmet'
        kw[template % ('AMT', n)] = event.helmet
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
        data = current_app.paypal.do_express_checkout_payment(**kw)
        checkout_response = current_app \
            .paypal.get_express_checkout_details(token=token)
        if checkout_response['CHECKOUTSTATUS'] == 'PaymentActionCompleted':
            order.status = 'PAID'
        return render_template('confirm.html', **{
            'email': 'startnewyork@gmail.com',
            'order_id': order.id,
            'total': checkout_response['AMT'],
            'first_name': order.first_name
        })
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
