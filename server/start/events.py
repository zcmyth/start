from flask import Blueprint, request, current_app
from .models import Event
from .response import Response

bp = Blueprint('events', __name__)


@bp.route('/<int:id>', methods=['GET'])
def get_event(id):
    return Response.success(Event.query.get(id))
