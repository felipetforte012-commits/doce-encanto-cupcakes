from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import db
from app.models import Cliente

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    """US01 - Criar conta de usuário"""
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        erro = None
        if not nome or not email or not senha:
            erro = "Preencha todos os campos obrigatórios."
        elif len(senha) < 8:
            erro = "A senha deve ter no mínimo 8 caracteres."  # CA2
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
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")

        cliente = Cliente.query.filter_by(email=email).first()
        if cliente and cliente.checar_senha(senha):
            login_user(cliente)
            flash(f"Bem-vindo(a), {cliente.nome}!", "success")
            proxima = request.args.get("next")
            return redirect(proxima or url_for("main.index"))

        flash("E-mail ou senha inválidos.", "danger")  # CA3

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "info")
    return redirect(url_for("main.index"))
