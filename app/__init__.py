# ...
from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if app.config['SERVERS']:
        pass

    from app.main import bp_main
    app.register_blueprint(bp_main, url_prefix='/')

    # ...
    from app.api import bp_api
    app.register_blueprint(bp_api, url_prefix='/api')

    # ...
    return app