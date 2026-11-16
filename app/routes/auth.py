import re

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import db
from app.models import Cliente
from app.seguranca import destino_seguro

auth_bp = Blueprint("auth", __name__)

EMAIL_VALIDO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
TAMANHO_MINIMO_SENHA = 8


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    """US01 - Criar conta de usuário"""
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        erro = None
        if not nome or not email or not senha:
            erro = "Preencha todos os campos obrigatórios."
        elif len(nome) > 120:
            erro = "O nome pode ter no máximo 120 caracteres."
        elif len(email) > 150 or not EMAIL_VALIDO.match(email):
            erro = "Informe um e-mail válido (ex.: nome@exemplo.com)."
        elif len(senha) < TAMANHO_MINIMO_SENHA:
            erro = f"A senha deve ter no mínimo {TAMANHO_MINIMO_SENHA} caracteres."  # CA2
        elif Cliente.query.filter_by(email=email).first():
            erro = "Este e-mail já está cadastrado."  # CA3

        if erro:
            flash(erro, "danger")
            return render_template("cadastro.html", nome=nome, email=email)

        cliente = Cliente(nome=nome, email=email)
        cliente.set_senha(senha)
        db.session.add(cliente)
        db.session.commit()

        flash("Conta criada com sucesso! Faça login para continuar.", "success")
        return redirect(url_for("auth.login"))

    return render_template("cadastro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """US02 - Efetuar login"""
    proxima = request.args.get("next")

    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        cliente = Cliente.query.filter_by(email=email).first()
        if cliente and cliente.checar_senha(senha):
            login_user(cliente)
            flash(f"Bem-vindo(a), {cliente.nome}!", "success")
            # Só redireciona para endereços internos (evita "open redirect").
            return redirect(proxima if destino_seguro(proxima) else url_for("main.index"))

        flash("E-mail ou senha inválidos.", "danger")  # CA3
        return render_template("login.html", email=email)

    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """Logout via POST (com token CSRF) para que links externos não desconectem o usuário."""
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("main.index"))
