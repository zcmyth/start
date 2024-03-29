from .models import Event

_transform_map = {}


_transform_map[Event.__tablename__] = [
    'description', 'lift', 'rental',
    'beginner', 'helmet', 'bus', 'ticket_num', 'ticket_left']


def transform_sqlalchemy_obj(obj):
    items = _transform_map.get(obj.__tablename__)
    if items:
        result = {}
        for item in items:
            if isinstance(item, str):
                value = getattr(obj, item)
                if value is not None:
                    result[item] = value
            elif 'transform' in item:
                value = item.get('transform')(obj)
                if value is not None:
                    result[item.get('name')] = value
            elif 'filter' in item:
                value = {}
                subobj = getattr(obj, item.get('name'))
                for key in item.get('filter'):
                    value[key] = getattr(subobj, key)
                result[item.get('name')] = value
        return result
    return {k: v for k, v in obj.__dict__.iteritems()
            if (not k.startswith('_')) and (v is not None)}
