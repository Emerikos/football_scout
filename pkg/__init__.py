import os
from flask import Flask
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

csrf = CSRFProtect()
def create_app():
    from pkg.models import db
    from pkg import config
    
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_pyfile('config.py')
    app.config.from_object(config.Config)

    db.init_app(app)
    migrate = Migrate(app,db)
    csrf.init_app(app)
    return app

app = create_app()

from pkg import user_routes,admin_routes,models,forms



