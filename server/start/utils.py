import calendar
import pytz
import requests
from flask import Flask, jsonify, request, current_app
from flask.json import JSONEncoder
from datetime import datetime
from dateutil import parser
from .transforms import transform_sqlalchemy_obj
from .response import Response, InvalidArgument
import time


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                if obj.utcoffset():
                    obj = obj - obj.utcoffset()
                millis = int(
                    calendar.timegm(obj.timetuple()) * 1000 +
                    obj.microsecond / 1000
                )
                return millis
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        # For sqlalchemy
        if hasattr(obj, '__tablename__'):
            return transform_sqlalchemy_obj(obj)
        return JSONEncoder.default(self, obj)