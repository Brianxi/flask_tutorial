"""
The name if this file, __init__.py tells Python that the containing directory
(flaskr) should be considered a Python package.  It can (and does) contain
initialization code for the package.
"""
import os
from flask import Flask

def create_app(test_config=None):
    """
    This is the Flask application factory function.  It allows you to have
    multiple instances of hte same application running in the same application
    process.
    """
    print("running __init__.create_app")
    # create and configure the create_app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed if __name__ == '__main__':
        app.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db, auth, blog
    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    return app
