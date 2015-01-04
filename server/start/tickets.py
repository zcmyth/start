import uuid
from flask import Blueprint, request, current_app, url_for,\
    render_template
from datetime import datetime
from .models import TicketOrder, Ticket
from .response import Response
from paypal.exceptions import PayPalAPIResponseError

bp = Blueprint('tickets', __name__)


@bp.route('/<int:id>', methods=['GET'])
def get_ticket(id):
    return Response.success(Ticket.query.get(id))


@bp.route('', methods=['POST'])
def create_ticket_order():
    data = request.get_json()
    ticket = Ticket.query.get(data['ticket_id'])
    if not ticket:
        return Response.error('Invalid ticket')

    if int(data['lift']) < 6:
        return Response.error('Mininum 6 tickets')

    total = (int(data['lift']) * ticket.lift
             + int(data['snowboard']) * ticket.snowboard
             + int(data['ski']) * ticket.ski)
    order = TicketOrder(
        id=str(uuid.uuid1()),
        ticket_id=data['ticket_id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data['phone'],
        email=data['email'],
        lift=data['lift'],
        snowboard=data['snowboard'],
        ski=data['ski'],
        status='PENDING',
        create_time=datetime.utcnow(),
        total=total
    )

    kw = {
        'PAYMENTREQUEST_0_AMT': total,
        'PAYMENTREQUEST_0_PAYMENTACTION': 'Sale',
        'SOLUTIONTYPE': 'Sole',
        'currencycode': 'USD',
        'returnurl': url_for(
            'tickets.paypal_confirm', order_id=order.id, _external=True),
        'cancelurl': url_for(
            'ngapp.home', _external=True) + '#/' + data['ticket_id'],
    }

    n = 0
    template = 'L_PAYMENTREQUEST_0_%s%s'
    if int(data['lift']) > 0:
        kw[template % ('NAME', n)] = 'Lift'
        kw[template % ('AMT', n)] = ticket.lift
        kw[template % ('QTY', n)] = int(data['lift'])
        n = n + 1

    if int(data['snowboard']) > 0:
        kw[template % ('NAME', n)] = 'Snowboard rental'
        kw[template % ('AMT', n)] = ticket.snowboard
        kw[template % ('QTY', n)] = int(data['snowboard'])
        n = n + 1

    if int(data['ski']) > 0:
        kw[template % ('NAME', n)] = 'Ski rental'
        kw[template % ('AMT', n)] = ticket.ski
        kw[template % ('QTY', n)] = int(data['ski'])
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

    order = TicketOrder.query.get(request.args['order_id'])
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
        current_app.paypal.do_express_checkout_payment(**kw)
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
