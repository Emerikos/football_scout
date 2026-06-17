import os
from flask import Flask, app
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

csrf = CSRFProtect()
def create_app():
    from pkg.models import db
    from pkg import config
    
    app = Flask(__name__,instance_relative_config=True)
    # app.config.from_pyfile('config.py')
    # app.config.from_object(config.Config)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate = Migrate(app,db)
    csrf.init_app(app)
    from pkg import user_routes,admin_routes,models,forms
    return app

app = create_app()





