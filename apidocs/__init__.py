import os
from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        #DATABASE=os.path.join(app.instance_path, 'nextel-docs.sqlite'),
        UPLOAD_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from apidocs.modules.base import controllers
    app.register_blueprint(controllers.bp)
    app.add_url_rule('/', endpoint='index')	        

    from apidocs.modules.access_control import controllers
    app.register_blueprint(controllers.bp)

    from apidocs.modules.register import controllers
    app.register_blueprint(controllers.bp)

    from apidocs.modules.api import controllers
    app.register_blueprint(controllers.bp)

    from apidocs.modules.orch import controllers
    app.register_blueprint(controllers.bp)

    from apidocs.modules.service import controllers
    app.register_blueprint(controllers.bp)

    from apidocs.modules.search import controllers
    app.register_blueprint(controllers.bp)

    from apidocs.modules.tsonline import controllers
    app.register_blueprint(controllers.bp)

    from apidocs.modules.configuration import controllers
    app.register_blueprint(controllers.bp)

    from apidocs.modules.audit_log import controllers
    app.register_blueprint(controllers.bp)

    from apidocs.modules.user import controllers
    app.register_blueprint(controllers.bp)

    return app