# ...
from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    # this configuration is to avoid extra lines when processing lists
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True
    # reading a default configuration to set some paramenters
    app.config.from_object(config_class)

    if app.config['SERVERS']:
        pass

    from app.main import bp_main
    app.register_blueprint(bp_main, url_prefix='/')

    # ...
    from app.api import bp_api
    app.register_blueprint(bp_api, url_prefix='/api/v1')

    # ...
    return app