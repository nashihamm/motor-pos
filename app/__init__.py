from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_talisman import Talisman
from mangum import Mangum

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    Talisman(app)
    CORS(app)
    db.init_app(app)
    migrate.init_app(app,db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import user_bp
    from app.routes.motor_routes import motor_bp
    from app.routes.tenant_routes import tenant_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(motor_bp)
    app.register_blueprint(tenant_bp)

    handler = Mangum(app)
    return app