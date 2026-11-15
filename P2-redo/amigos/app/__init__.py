from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import app_config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate = Migrate(app, db)
    from app import models


    from .html import html as html_blueprint
    app.register_blueprint(html_blueprint, url_prefix='/html')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    @app.route("/")
    def prueba():
        return "¡Hola Flask con MariaDB!"
    
    @app.route("/health")
    def health():
        try:
            db.session.execute(db.text("SELECT 1"))
            return {"status": "ok", "database": "ok"}, 200
        except Exception:
            return {"status": "error", "database": "error"}, 503
    
    from .metrics import metrics as metrics_blueprint
    app.register_blueprint(metrics_blueprint)
        
    return app