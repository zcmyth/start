from flask import Flask, redirect, url_for
from paypal import PayPalConfig
from paypal import PayPalInterface
from .utils import CustomJSONEncoder
from .models import db


def _log_config(app):
    if not app.debug and not app.testing:
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(
            app.config.get('LOGGING_PATH'),
            maxBytes=app.config.get('LOGGING_SIZE'))
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


def create_app(config):
    app = Flask(
        __name__,
        template_folder='../../client/templates',
        static_folder='../../client/static',
        static_url_path="/static")
    app.config.from_object(config)

    _log_config(app)

    app.json_encoder = CustomJSONEncoder
    app.paypal = PayPalInterface(
        config=PayPalConfig(**app.config['PAYPAL_CONFIG']))

    @app.route('/')
    def to_app():
        return redirect(url_for('ngapp.home'))

    app.db = db
    db.init_app(app)

    # from .login import login_manager
    # login_manager.init_app(app)

    from .response import init as response_init
    response_init(app)

    # register bp
    import ngapp
    app.register_blueprint(ngapp.bp)

    import orders
    app.register_blueprint(orders.bp, url_prefix='/api/orders')

    import events
    app.register_blueprint(events.bp, url_prefix='/api/events')

    # import wechat
    # app.register_blueprint(wechat.bp, url_prefix='/api/wechat')

    return app
