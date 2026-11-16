from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFError, CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Faça login para continuar."
login_manager.login_message_category = "info"
csrf = CSRFProtect()


def create_app(config_object="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    if not app.config.get("SECRET_KEY"):
        raise RuntimeError(
            "SECRET_KEY não definida. Em produção (Render), cadastre a variável "
            "de ambiente SECRET_KEY no painel do serviço."
        )

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app import models  # noqa: F401  (registra os models no SQLAlchemy)
    from app.formatacao import data_br, moeda_brl

    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.cart import cart_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(admin_bp)

    app.jinja_env.filters["brl"] = moeda_brl
    app.jinja_env.filters["data_br"] = data_br

    @app.context_processor
    def inject_cart_count():
        carrinho = session.get("carrinho", {})
        total_itens = sum(carrinho.values()) if carrinho else 0
        return {"carrinho_total_itens": total_itens}

    _registrar_tratadores_de_erro(app)
    return app


def _registrar_tratadores_de_erro(app):
    from app.seguranca import caminho_interno_do_referer

    @app.errorhandler(CSRFError)
    def erro_csrf(_erro):
        flash("Sua sessão expirou ou o formulário ficou desatualizado. Tente novamente.", "warning")
        voltar = caminho_interno_do_referer(request.referrer, request.host)
        return redirect(voltar or url_for("main.index"))

    @app.errorhandler(404)
    def nao_encontrado(_erro):
        return render_template(
            "erro.html", codigo=404, titulo="Página não encontrada",
            mensagem="O endereço acessado não existe ou o item foi removido.",
        ), 404

    @app.errorhandler(500)
    def erro_interno(_erro):
        db.session.rollback()
        return render_template(
            "erro.html", codigo=500, titulo="Algo deu errado",
            mensagem="Tivemos um problema ao processar sua solicitação. Tente novamente em instantes.",
        ), 500
