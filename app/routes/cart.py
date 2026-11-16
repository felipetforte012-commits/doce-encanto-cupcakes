from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models import QUANTIDADE_MINIMA_POR_SABOR, ItemPedido, Pedido, Produto

cart_bp = Blueprint("cart", __name__)

TAXA_ENTREGA_PADRAO = 8.00


def _get_carrinho():
    return session.setdefault("carrinho", {})


def _msg_estoque_insuficiente(produto, ja_no_carrinho=0):
    msg = f"Estoque insuficiente: temos {produto.estoque} unidade(s) de {produto.nome}"
    if ja_no_carrinho:
        msg += f" e você já tem {ja_no_carrinho} no carrinho"
    return msg + "."


@cart_bp.route("/carrinho/adicionar/<int:produto_id>", methods=["POST"])
def adicionar_ao_carrinho(produto_id):
    """US07 - Adicionar itens ao carrinho"""
    produto = db.get_or_404(Produto, produto_id)
    voltar = redirect(url_for("main.produto_detalhe", produto_id=produto_id))
    quantidade = request.form.get("quantidade", type=int)

    if quantidade is None or quantidade < QUANTIDADE_MINIMA_POR_SABOR:
        flash(f"Quantidade mínima por sabor é {QUANTIDADE_MINIMA_POR_SABOR} unidades.", "warning")  # RN07
        return voltar

    if not produto.disponivel():
        flash("Este produto não está disponível no momento.", "warning")
        return voltar

    carrinho = _get_carrinho()
    chave = str(produto_id)
    ja_no_carrinho = carrinho.get(chave, 0)
    if not produto.tem_estoque_para(ja_no_carrinho + quantidade):
        flash(_msg_estoque_insuficiente(produto, ja_no_carrinho), "warning")  # CA1
        return voltar

    carrinho[chave] = ja_no_carrinho + quantidade
    session.modified = True
    flash(f"{produto.nome} adicionado ao carrinho.", "success")
    return redirect(url_for("cart.ver_carrinho"))


@cart_bp.route("/carrinho/remover/<int:produto_id>", methods=["POST"])
def remover_do_carrinho(produto_id):
    """US09 - Remover itens do carrinho"""
    carrinho = _get_carrinho()
    carrinho.pop(str(produto_id), None)
    session.modified = True
    flash("Item removido do carrinho.", "info")
    return redirect(url_for("cart.ver_carrinho"))


@cart_bp.route("/carrinho/atualizar/<int:produto_id>", methods=["POST"])
def atualizar_carrinho(produto_id):
    """US09 - Editar quantidade de itens do carrinho"""
    carrinho = _get_carrinho()
    chave = str(produto_id)
    nova_quantidade = request.form.get("quantidade", type=int)
    produto = db.session.get(Produto, produto_id)

    if chave not in carrinho:
        flash("Este item não está no seu carrinho.", "warning")
    elif nova_quantidade is None or nova_quantidade < QUANTIDADE_MINIMA_POR_SABOR:
        flash(f"Quantidade mínima por sabor é {QUANTIDADE_MINIMA_POR_SABOR} unidades.", "warning")
    elif produto is None or not produto.disponivel():
        flash("Este produto não está mais disponível. Remova-o do carrinho.", "warning")
    elif not produto.tem_estoque_para(nova_quantidade):
        flash(_msg_estoque_insuficiente(produto), "warning")
    else:
        carrinho[chave] = nova_quantidade
        session.modified = True
        flash("Carrinho atualizado.", "success")

    return redirect(url_for("cart.ver_carrinho"))


def _montar_itens_carrinho():
    """Monta os itens do carrinho, marcando os que não podem ser comprados."""
    carrinho = _get_carrinho()
    itens = []
    subtotal = 0.0
    for produto_id_str, quantidade in list(carrinho.items()):
        produto = db.session.get(Produto, int(produto_id_str))
        if not produto:
            carrinho.pop(produto_id_str)  # produto não existe mais no banco
            session.modified = True
            continue

        problema = None
        if not produto.disponivel():
            problema = "Produto indisponível no momento"
        elif quantidade > produto.estoque:
            problema = f"Estoque insuficiente (restam {produto.estoque})"

        item_subtotal = float(produto.preco) * quantidade
        subtotal += item_subtotal
        itens.append({
            "produto": produto, "quantidade": quantidade,
            "item_subtotal": item_subtotal, "problema": problema,
        })
    return itens, subtotal


@cart_bp.route("/carrinho")
def ver_carrinho():
    """US09 / US10 - Ver e editar carrinho"""
    itens, subtotal = _montar_itens_carrinho()
    tem_problema = any(item["problema"] for item in itens)
    return render_template("carrinho.html", itens=itens, subtotal=subtotal, tem_problema=tem_problema)


def _render_checkout(itens, subtotal, form=None):
    return render_template(
        "checkout.html", itens=itens, subtotal=subtotal, taxa_entrega=TAXA_ENTREGA_PADRAO,
        tipos_entrega=Pedido.TIPOS_ENTREGA, formas_pagamento=Pedido.FORMAS_PAGAMENTO,
        form=form or {},
    )


@cart_bp.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    """US10 - Resumo do pedido / US08 / US11 / US14 - Entrega e pagamento"""
    itens, subtotal = _montar_itens_carrinho()

    if not itens:
        flash("Seu carrinho está vazio.", "warning")
        return redirect(url_for("cart.ver_carrinho"))

    if any(item["problema"] for item in itens):
        flash("Alguns itens do carrinho precisam de ajuste antes de finalizar a compra.", "warning")
        return redirect(url_for("cart.ver_carrinho"))

    if request.method == "GET":
        return _render_checkout(itens, subtotal)

    tipo_entrega = request.form.get("tipo_entrega", "entrega")  # US14
    endereco = request.form.get("endereco", "").strip()
    forma_pagamento = request.form.get("forma_pagamento", "cartao")  # US11
    mensagem_presente = request.form.get("mensagem_presente", "").strip()[:200]  # CA2 US08

    # O TiDB está com CHECK desativado: a validação dos valores é feita aqui.
    erro = None
    if tipo_entrega not in Pedido.TIPOS_ENTREGA:
        erro = "Escolha uma forma de entrega válida."
    elif forma_pagamento not in Pedido.FORMAS_PAGAMENTO:
        erro = "Escolha uma forma de pagamento válida."
    elif tipo_entrega == "entrega" and not endereco:
        erro = "Informe o endereço de entrega ou escolha retirada na loja."
    elif len(endereco) > 255:
        erro = "O endereço pode ter no máximo 255 caracteres."
    if erro:
        flash(erro, "warning")
        return _render_checkout(itens, subtotal, request.form)

    try:
        # Relê os produtos BLOQUEANDO as linhas (SELECT ... FOR UPDATE) para que
        # duas compras simultâneas não vendam o mesmo estoque duas vezes.
        ids = [item["produto"].id for item in itens]
        produtos = {
            p.id: p for p in db.session.execute(
                select(Produto).where(Produto.id.in_(ids)).with_for_update()
                .execution_options(populate_existing=True)
            ).scalars()
        }
        for item in itens:
            produto = produtos.get(item["produto"].id)
            if produto is None or not produto.tem_estoque_para(item["quantidade"]):
                db.session.rollback()
                flash("O estoque de um dos itens mudou enquanto você comprava. Confira o carrinho.", "warning")
                return redirect(url_for("cart.ver_carrinho"))

        subtotal = sum(float(produtos[i["produto"].id].preco) * i["quantidade"] for i in itens)
        taxa_entrega = TAXA_ENTREGA_PADRAO if tipo_entrega == "entrega" else 0.0

        pedido = Pedido(
            cliente_id=current_user.id,
            status="novo",
            tipo_entrega=tipo_entrega,
            endereco_entrega=endereco if tipo_entrega == "entrega" else None,
            forma_pagamento=forma_pagamento,
            status_pagamento="aprovado",  # simulação de gateway de pagamento (US11/US12)
            subtotal=subtotal,
            taxa_entrega=taxa_entrega,
            total=subtotal + taxa_entrega,
            mensagem_presente=mensagem_presente or None,
        )
        db.session.add(pedido)
        db.session.flush()  # obtém pedido.id antes do commit

        for item in itens:
            produto = produtos[item["produto"].id]
            produto.estoque -= item["quantidade"]
            db.session.add(ItemPedido(
                pedido_id=pedido.id, produto_id=produto.id,
                quantidade=item["quantidade"], preco_unitario=produto.preco,
            ))

        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("Falha ao gravar pedido")
        flash("Não foi possível concluir o pedido agora. Nenhum valor foi cobrado; tente novamente.", "danger")
        return redirect(url_for("cart.ver_carrinho"))

    session["carrinho"] = {}
    session.modified = True
    flash("Pagamento aprovado! Pedido confirmado com sucesso.", "success")  # US12
    return redirect(url_for("cart.detalhe_pedido", pedido_id=pedido.id))


@cart_bp.route("/pedidos")
@login_required
def meus_pedidos():
    """US15 - Acompanhar status do pedido"""
    pedidos = (
        Pedido.query.filter_by(cliente_id=current_user.id)
        .order_by(Pedido.criado_em.desc())
        .all()
    )
    return render_template("pedidos.html", pedidos=pedidos)


@cart_bp.route("/pedidos/<int:pedido_id>")
@login_required
def detalhe_pedido(pedido_id):
    """US15 - Detalhe do pedido (o cliente só vê os próprios pedidos)"""
    pedido = db.get_or_404(Pedido, pedido_id)
    if pedido.cliente_id != current_user.id and not current_user.is_admin:
        flash("Você não tem permissão para ver este pedido.", "danger")
        return redirect(url_for("cart.meus_pedidos"))
    return render_template("pedido_detalhe.html", pedido=pedido)
