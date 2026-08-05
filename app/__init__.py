from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Faça login para continuar."


def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)
   
    db.init_app(app)
    login_manager.init_app(app)

    from app import models  # noqa: F401  (registra os models no SQLAlchemy)

    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.cart import cart_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def inject_cart_count():
        from flask import session
        carrinho = session.get("carrinho", {})
        total_itens = sum(carrinho.values()) if carrinho else 0
        return {"carrinho_total_itens": total_itens}

    return app
