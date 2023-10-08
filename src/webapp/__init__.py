from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
import os
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"
DB_PATH = os.path.join("../instance", DB_NAME)

def create_app():
    app = Flask(__name__)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config['SECRET_KEY'] = 'ohYEA'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
    app.secret_key = "BLAZEBLOCK"

    db.init_app(app)

    from .views import views
    from .map import map
    from .admin import admin
    from .user_alert import uas

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(map, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    app.register_blueprint(uas, url_prefix='/')

    dirpath = app.instance_path + '/uploads'
    create_database(app)
    create_uploads(dirpath)

    return app


def create_uploads(dirpath):
    if not path.exists(dirpath):
        os.mkdir(dirpath)
    print('Created Upload Directory')

def create_database(app):
    if not path.exists(DB_PATH):
        with app.app_context():
            db.create_all()
        print('Created Database')
