from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Produto, Categoria, Pedido

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(f):
    """RN11 - Apenas usuários com perfil administrador podem alterar o catálogo."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Acesso restrito ao administrador da loja.", "danger")
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route("/produtos")
@login_required
@admin_required
def listar_produtos():
    """US17 - Gerenciar catálogo de produtos"""
    produtos = Produto.query.order_by(Produto.nome).all()
    return render_template("admin/produtos.html", produtos=produtos)


@admin_bp.route("/produtos/novo", methods=["GET", "POST"])
@login_required
@admin_required
def novo_produto():
    categorias = Categoria.query.order_by(Categoria.nome).all()

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        preco = request.form.get("preco", type=float)
        foto_url = request.form.get("foto_url", "").strip()

        if not nome or not preco or not foto_url:
            flash("Nome, preço e foto são obrigatórios para publicar um produto.", "warning")  # CA1
            return render_template("admin/produto_form.html", categorias=categorias, produto=None)

        produto = Produto(
            nome=nome,
            sabor=request.form.get("sabor", "").strip(),
            descricao=request.form.get("descricao", "").strip(),
            alergenos=request.form.get("alergenos", "").strip(),
            preco=preco,
            foto_url=foto_url,
            estoque=request.form.get("estoque", type=int, default=0),
            categoria_id=request.form.get("categoria_id", type=int),
            ativo=True,
        )
        db.session.add(produto)
        db.session.commit()
        flash("Produto cadastrado com sucesso.", "success")
        return redirect(url_for("admin.listar_produtos"))

    return render_template("admin/produto_form.html", categorias=categorias, produto=None)


@admin_bp.route("/produtos/<int:produto_id>/editar", methods=["GET", "POST"])
@login_required
@admin_required
def editar_produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    categorias = Categoria.query.order_by(Categoria.nome).all()

    if request.method == "POST":
        produto.nome = request.form.get("nome", "").strip()
        produto.sabor = request.form.get("sabor", "").strip()
        produto.descricao = request.form.get("descricao", "").strip()
        produto.alergenos = request.form.get("alergenos", "").strip()
        produto.preco = request.form.get("preco", type=float)
        produto.foto_url = request.form.get("foto_url", "").strip()
        produto.estoque = request.form.get("estoque", type=int, default=0)
        produto.categoria_id = request.form.get("categoria_id", type=int)
        produto.ativo = bool(request.form.get("ativo"))

        db.session.commit()
        flash("Produto atualizado com sucesso.", "success")
        return redirect(url_for("admin.listar_produtos"))

    return render_template("admin/produto_form.html", categorias=categorias, produto=produto)


@admin_bp.route("/produtos/<int:produto_id>/remover", methods=["POST"])
@login_required
@admin_required
def remover_produto(produto_id):
    """CA2 - Produto removido não aparece mais na vitrine, mas histórico é mantido (soft delete)."""
    produto = Produto.query.get_or_404(produto_id)
    produto.ativo = False
    db.session.commit()
    flash("Produto removido da vitrine.", "info")
    return redirect(url_for("admin.listar_produtos"))


@admin_bp.route("/pedidos")
@login_required
@admin_required
def listar_pedidos():
    """US18 - Painel de pedidos recebidos"""
    status_filtro = request.args.get("status", "")
    query = Pedido.query
    if status_filtro:
        query = query.filter_by(status=status_filtro)
    pedidos = query.order_by(Pedido.criado_em.desc()).all()
    return render_template("admin/pedidos.html", pedidos=pedidos, status_filtro=status_filtro)


@admin_bp.route("/pedidos/<int:pedido_id>/status", methods=["POST"])
@login_required
@admin_required
def atualizar_status_pedido(pedido_id):
    """US15/US16/US18 - Atualizar status do pedido (dispara notificação ao cliente)"""
    pedido = Pedido.query.get_or_404(pedido_id)
    novo_status = request.form.get("status")
    status_validos = {"novo", "em_preparo", "saiu_para_entrega", "entregue", "cancelado"}

    if novo_status in status_validos:
        pedido.status = novo_status
        db.session.commit()
        flash(f"Status do pedido #{pedido.id} atualizado para '{novo_status}'.", "success")
    else:
        flash("Status inválido.", "danger")

    return redirect(url_for("admin.listar_pedidos"))
