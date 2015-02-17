import requests
from flask import Blueprint, url_for, request
from flask_oauthlib.client import OAuth
from werkzeug.urls import url_parse, url_encode

bp = Blueprint('wechat', __name__)


def _fixup_weixin_oauth(weixin):
    """Fixes the nonstandard OAuth interface of Tencent WeChat."""

    original_methods = {
        'authorize': weixin.authorize,
        'authorized_response': weixin.authorized_response,
    }

    def authorize(*args, **kwargs):
        response = original_methods['authorize'](*args, **kwargs)
        url = url_parse(response.headers['Location'])
        args = url.decode_query()

        # replace the nonstandard argument
        args['appid'] = args.pop('client_id')
        # replace the nonstandard fragment
        url = url.replace(query=url_encode(args), fragment='wechat_redirect')

        response.headers['Location'] = url.to_url()
        return response

    def authorized_response(*args, **kwargs):
        original_access_token_params = weixin.access_token_params
        weixin.access_token_params = {
            'appid': weixin.consumer_key,
            'secret': weixin.consumer_secret,
        }
        response = original_methods['authorized_response'](*args, **kwargs)
        weixin.access_token_params = original_access_token_params
        return response

    weixin.authorize = authorize
    weixin.authorized_response = authorized_response


_wechat = OAuth().remote_app(
    'weixin',
    app_key='WECHAT',
    request_token_params={'scope': 'snsapi_base'},
    base_url='https://api.weixin.qq.com',
    authorize_url='https://open.weixin.qq.com/connect/oauth2/authorize',
    access_token_url='https://api.weixin.qq.com/sns/oauth2/access_token',
    # important: ignore the 'text/plain' said by weixin api and enforce the
    #            response be parsed as json.
    content_type='application/json',
)
_fixup_weixin_oauth(_wechat)


@bp.route('/login')
def login():
    return _wechat.authorize(callback=url_for('wechat.user'),
                             next=request.args.get('next') or request.referrer or '//')


def get_user(access_token):
    return {
        'open_id': 'lalala'
    }


@bp.route('/user')
def user():
    return 'Haha'
