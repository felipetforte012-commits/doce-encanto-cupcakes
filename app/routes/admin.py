from decimal import Decimal, InvalidOperation
from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models import Categoria, Pedido, Produto

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

PRECO_MAXIMO = Decimal("99999.99")


def admin_required(f):
    """RN11 - Apenas usuários com perfil administrador podem alterar o catálogo."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Acesso restrito ao administrador da loja.", "danger")
            return redirect(url_for("main.index"))
        return f(*args, **kwargs)
    return decorated


def _valores_do_produto(produto):
    return {
        "nome": produto.nome, "sabor": produto.sabor, "descricao": produto.descricao or "",
        "alergenos": produto.alergenos or "", "preco": f"{produto.preco:.2f}",
        "estoque": str(produto.estoque), "foto_url": produto.foto_url or "",
        "categoria_id": produto.categoria_id, "ativo": produto.ativo,
    }


def _ler_formulario_produto(categorias):
    """Lê e valida o formulário de produto. Retorna (valores, dados_validos, erros)."""
    f = request.form
    valores = {
        "nome": f.get("nome", "").strip(),
        "sabor": f.get("sabor", "").strip(),
        "descricao": f.get("descricao", "").strip(),
        "alergenos": f.get("alergenos", "").strip(),
        "preco": f.get("preco", "").strip(),
        "estoque": f.get("estoque", "").strip(),
        "foto_url": f.get("foto_url", "").strip(),
        "categoria_id": f.get("categoria_id", type=int),
        "ativo": bool(f.get("ativo")),
    }
    erros = []

    if not valores["nome"]:
        erros.append("Informe o nome do produto.")
    elif len(valores["nome"]) > 120:
        erros.append("O nome pode ter no máximo 120 caracteres.")

    if not valores["sabor"]:
        erros.append("Informe o sabor.")
    elif len(valores["sabor"]) > 80:
        erros.append("O sabor pode ter no máximo 80 caracteres.")

    preco = None
    try:
        preco = Decimal(valores["preco"].replace(",", "."))
        if not preco.is_finite() or preco <= 0 or preco > PRECO_MAXIMO:
            raise InvalidOperation
        preco = preco.quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        erros.append("Informe um preço válido, maior que zero (ex.: 6,50).")

    estoque = 0
    if valores["estoque"]:
        try:
            estoque = int(valores["estoque"])
            if estoque < 0:
                raise ValueError
        except ValueError:
            erros.append("O estoque deve ser um número inteiro igual ou maior que zero.")

    if not valores["foto_url"]:
        erros.append("Informe a URL da foto (CA1: produto não pode ser publicado sem foto).")
    elif len(valores["foto_url"]) > 255 or not valores["foto_url"].startswith(("http://", "https://")):
        erros.append("A URL da foto deve começar com http:// ou https:// (máx. 255 caracteres).")

    if len(valores["alergenos"]) > 255:
        erros.append("O campo alérgenos pode ter no máximo 255 caracteres.")

    if valores["categoria_id"] not in {c.id for c in categorias}:
        erros.append("Escolha uma categoria válida.")

    dados = {
        "nome": valores["nome"], "sabor": valores["sabor"], "descricao": valores["descricao"],
        "alergenos": valores["alergenos"], "preco": preco, "estoque": estoque,
        "foto_url": valores["foto_url"], "categoria_id": valores["categoria_id"], "ativo": valores["ativo"],
    }
    return valores, dados, erros


def _render_form(categorias, valores, produto=None):
    return render_template("admin/produto_form.html", categorias=categorias, valores=valores, produto=produto)


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
    """US17 - Cadastrar produto"""
    categorias = Categoria.query.order_by(Categoria.nome).all()

    if request.method == "POST":
        valores, dados, erros = _ler_formulario_produto(categorias)
        if erros:
            for erro in erros:
                flash(erro, "warning")
            return _render_form(categorias, valores)

        db.session.add(Produto(**dados))
        db.session.commit()
        flash("Produto cadastrado com sucesso.", "success")
        return redirect(url_for("admin.listar_produtos"))

    return _render_form(categorias, {"ativo": True, "estoque": "0"})


@admin_bp.route("/produtos/<int:produto_id>/editar", methods=["GET", "POST"])
@login_required
@admin_required
def editar_produto(produto_id):
    """US17 - Editar produto"""
    produto = db.get_or_404(Produto, produto_id)
    categorias = Categoria.query.order_by(Categoria.nome).all()

    if request.method == "POST":
        valores, dados, erros = _ler_formulario_produto(categorias)
        if erros:
            for erro in erros:
                flash(erro, "warning")
            return _render_form(categorias, valores, produto)

        for campo, valor in dados.items():
            setattr(produto, campo, valor)
        db.session.commit()
        flash("Produto atualizado com sucesso.", "success")
        return redirect(url_for("admin.listar_produtos"))

    return _render_form(categorias, _valores_do_produto(produto), produto)


@admin_bp.route("/produtos/<int:produto_id>/remover", methods=["POST"])
@login_required
@admin_required
def remover_produto(produto_id):
    """CA2 - Produto removido não aparece mais na vitrine, mas histórico é mantido (soft delete)."""
    produto = db.get_or_404(Produto, produto_id)
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
    if status_filtro in Pedido.STATUS:
        query = query.filter_by(status=status_filtro)
    pedidos = query.order_by(Pedido.criado_em.desc()).all()
    return render_template(
        "admin/pedidos.html", pedidos=pedidos, status_filtro=status_filtro, status_opcoes=Pedido.STATUS
    )


@admin_bp.route("/pedidos/<int:pedido_id>/status", methods=["POST"])
@login_required
@admin_required
def atualizar_status_pedido(pedido_id):
    """US16/US18 - Atualizar status do pedido (o cliente acompanha em "Meus pedidos")."""
    pedido = db.get_or_404(Pedido, pedido_id)
    novo_status = request.form.get("status")

    if novo_status not in Pedido.STATUS:
        flash("Status inválido.", "danger")
    elif not pedido.pode_mudar_status():
        flash(f"O pedido #{pedido.id} está cancelado e não pode mudar de status.", "warning")
    elif novo_status == pedido.status:
        flash(f"O pedido #{pedido.id} já está como '{pedido.status_rotulo}'.", "info")
    else:
        if novo_status == "cancelado":
            pedido.cancelar()  # devolve os itens ao estoque
        else:
            pedido.status = novo_status
        db.session.commit()
        msg = f"Status do pedido #{pedido.id} atualizado para '{pedido.status_rotulo}'."
        if novo_status == "cancelado":
            msg += " Os itens voltaram para o estoque."
        flash(msg, "success")

    return redirect(url_for("admin.listar_pedidos"))
