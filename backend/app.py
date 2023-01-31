from flask import Flask
from flask_restx import Api
from flask_migrate import Migrate
from models import User, Post
from exts import db
from flask_jwt_extended import JWTManager
from post import post_ns
from auth import auth_ns


def create_app (config):
    app = Flask(__name__)
    api = Api(app, doc='/docs')
    api.add_namespace(auth_ns)
    api.add_namespace(post_ns)

    # configure
    app.config.from_object(config)

    db.init_app(app)

    # Migrate
    migrate = Migrate(app, db)

    # JWT
    JWTManager(app)



    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "Post": Post,
            "user": User
        }
    
    return app
