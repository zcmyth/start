from flask import current_app
from flask.ext.login import LoginManager
from .wechat import get_user
from .models import User

login_manager = LoginManager()


@login_manager.request_loader
def load_user_from_request(request):
    access_token = request.args.get('access_token')
    if access_token:
        wechat_user = get_user(access_token)
        if wechat_user:
            user = User.query.filter_by(wechat_id=wechat_user.open_id).first()
            if user:
                return user
            else:
                new_user = User(wechat_id=wechat_user.open_id)
                current_app.db.session.add(new_user)
                current_app.db.session.commit()
    return None
