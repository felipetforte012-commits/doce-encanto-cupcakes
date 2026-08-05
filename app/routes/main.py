from flask import Blueprint, render_template, request
from app.models import Produto, Categoria

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """US04 - Navegar pela vitrine / US05 - Filtrar produtos"""
    categoria_id = request.args.get("categoria", type=int)
    sabor = request.args.get("sabor", "").strip()
    preco_max = request.args.get("preco_max", type=float)

    query = Produto.query.filter_by(ativo=True)
    if categoria_id:
        query = query.filter_by(categoria_id=categoria_id)
    if sabor:
        query = query.filter(Produto.sabor.ilike(f"%{sabor}%"))
    if preco_max:
        query = query.filter(Produto.preco <= preco_max)

    produtos = query.order_by(Produto.nome).all()
    categorias = Categoria.query.order_by(Categoria.nome).all()

    return render_template(
        "index.html",
        produtos=produtos,
        categorias=categorias,
        categoria_id=categoria_id,
        sabor=sabor,
        preco_max=preco_max,
    )


@main_bp.route("/produto/<int:produto_id>")
def produto_detalhe(produto_id):
    """US04 / US06 - Ver detalhes, alérgenos e informações do produto"""
    produto = Produto.query.get_or_404(produto_id)
    return render_template("produto.html", produto=produto)
