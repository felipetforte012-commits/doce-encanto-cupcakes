"""Testes de integração do carrinho (US07, US09) e do checkout (US08, US10-US12, US14, US15)."""
from decimal import Decimal

import pytest

from app import db
from app.models import ItemPedido, Pedido, Produto


def _adicionar(client, produto_id, quantidade):
    return client.post(f"/carrinho/adicionar/{produto_id}", data={"quantidade": quantidade}, follow_redirects=True)


def _carrinho(client):
    with client.session_transaction() as sess:
        return dict(sess.get("carrinho", {}))


def _definir_estoque(app, produto_id, estoque=None, ativo=None):
    with app.app_context():
        produto = db.session.get(Produto, produto_id)
        if estoque is not None:
            produto.estoque = estoque
        if ativo is not None:
            produto.ativo = ativo
        db.session.commit()


# ---------- US07 - Adicionar ao carrinho ----------
def test_adicionar_ao_carrinho_respeita_minimo(client, produto_id):
    resp = _adicionar(client, produto_id, 2)
    assert "mínima por sabor" in resp.get_data(as_text=True)
    assert _carrinho(client) == {}


def test_adicionar_ao_carrinho_sucesso(client, produto_id):
    resp = _adicionar(client, produto_id, 6)
    assert resp.status_code == 200
    assert _carrinho(client)[str(produto_id)] == 6


def test_adicionar_quantidade_maior_que_estoque_e_rejeitado(client, app, produto_id):
    _definir_estoque(app, produto_id, estoque=10)
    resp = _adicionar(client, produto_id, 12)
    assert "Estoque insuficiente" in resp.get_data(as_text=True)
    assert _carrinho(client) == {}


def test_adicionar_duas_vezes_considera_o_que_ja_esta_no_carrinho(client, app, produto_id):
    """Bug corrigido: antes era possível somar 6 + 6 com estoque 6."""
    _definir_estoque(app, produto_id, estoque=6)
    _adicionar(client, produto_id, 6)
    resp = _adicionar(client, produto_id, 6)
    assert "você já tem 6 no carrinho" in resp.get_data(as_text=True)
    assert _carrinho(client)[str(produto_id)] == 6


def test_adicionar_produto_inativo_e_rejeitado(client, app, produto_id):
    _definir_estoque(app, produto_id, ativo=False)
    resp = _adicionar(client, produto_id, 6)
    assert "não está disponível" in resp.get_data(as_text=True)


@pytest.mark.parametrize("quantidade, mensagem", [
    ("1,5", "número inteiro"),
    ("1.5", "número inteiro"),
    ("abc", "número inteiro"),
    ("", "número inteiro"),
    ("-6", "mínima por sabor"),
    ("5", "mínima por sabor"),
])
def test_adicionar_quantidade_invalida_mostra_mensagem_especifica(client, produto_id, quantidade, mensagem):
    """Melhoria do pré-teste: '1,5' agora pede número inteiro em vez de 'mínimo 6'."""
    resp = client.post(f"/carrinho/adicionar/{produto_id}", data={"quantidade": quantidade}, follow_redirects=True)
    assert mensagem in resp.get_data(as_text=True)
    assert _carrinho(client) == {}


def test_atualizar_com_quantidade_decimal_pede_numero_inteiro(client, produto_id):
    _adicionar(client, produto_id, 6)
    resp = client.post(f"/carrinho/atualizar/{produto_id}", data={"quantidade": "7,5"}, follow_redirects=True)
    assert "número inteiro" in resp.get_data(as_text=True)
    assert _carrinho(client)[str(produto_id)] == 6


# ---------- US09 - Editar / remover itens ----------
def test_atualizar_quantidade_no_carrinho(client, produto_id):
    _adicionar(client, produto_id, 6)
    client.post(f"/carrinho/atualizar/{produto_id}", data={"quantidade": 12})
    assert _carrinho(client)[str(produto_id)] == 12


def test_atualizar_acima_do_estoque_e_rejeitado(client, app, produto_id):
    _definir_estoque(app, produto_id, estoque=8)
    _adicionar(client, produto_id, 6)
    resp = client.post(f"/carrinho/atualizar/{produto_id}", data={"quantidade": 50}, follow_redirects=True)
    assert "Estoque insuficiente" in resp.get_data(as_text=True)
    assert _carrinho(client)[str(produto_id)] == 6


def test_atualizar_item_que_nao_esta_no_carrinho_e_ignorado(client, produto_id):
    resp = client.post(f"/carrinho/atualizar/{produto_id}", data={"quantidade": 6}, follow_redirects=True)
    assert "não está no seu carrinho" in resp.get_data(as_text=True)
    assert _carrinho(client) == {}


def test_remover_do_carrinho(client, produto_id):
    _adicionar(client, produto_id, 6)
    client.post(f"/carrinho/remover/{produto_id}")
    assert _carrinho(client) == {}


def test_carrinho_destaca_item_que_ficou_indisponivel(client, app, produto_id):
    _adicionar(client, produto_id, 6)
    _definir_estoque(app, produto_id, ativo=False)
    html = client.get("/carrinho").get_data(as_text=True)
    assert "Produto indisponível no momento" in html


# ---------- Checkout ----------
def test_checkout_exige_login(client, produto_id):
    _adicionar(client, produto_id, 6)
    resp = client.get("/checkout")
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]


def test_checkout_com_carrinho_vazio_volta_para_carrinho(client, cliente_logado):
    resp = client.get("/checkout", follow_redirects=True)
    assert "Seu carrinho está vazio" in resp.get_data(as_text=True)


def test_checkout_entrega_cria_pedido_baixa_estoque_e_limpa_carrinho(client, app, produto_id, cliente_logado):
    """US10/US11/US12/US14 - Fluxo completo de compra com entrega."""
    _adicionar(client, produto_id, 6)
    resp = client.post("/checkout", data={
        "tipo_entrega": "entrega", "endereco": "Rua A, 10", "forma_pagamento": "pix",
        "mensagem_presente": "Parabéns!",
    }, follow_redirects=True)

    assert "Pedido confirmado" in resp.get_data(as_text=True)
    with app.app_context():
        pedido = Pedido.query.one()
        assert pedido.cliente_id == cliente_logado
        assert pedido.subtotal == Decimal("36.00")
        assert pedido.taxa_entrega == Decimal("8.00")
        assert pedido.total == Decimal("44.00")
        assert pedido.status == "novo" and pedido.status_pagamento == "aprovado"
        assert pedido.mensagem_presente == "Parabéns!"
        item = ItemPedido.query.one()
        assert item.quantidade == 6 and item.preco_unitario == Decimal("6.00")
        assert db.session.get(Produto, produto_id).estoque == 44
    assert _carrinho(client) == {}


def test_checkout_retirada_nao_cobra_taxa(client, app, produto_id, cliente_logado):
    _adicionar(client, produto_id, 6)
    client.post("/checkout", data={"tipo_entrega": "retirada", "forma_pagamento": "cartao"})
    with app.app_context():
        pedido = Pedido.query.one()
        assert pedido.taxa_entrega == Decimal("0.00")
        assert pedido.endereco_entrega is None


def test_checkout_entrega_sem_endereco_e_rejeitado(client, app, produto_id, cliente_logado):
    _adicionar(client, produto_id, 6)
    resp = client.post("/checkout", data={"tipo_entrega": "entrega", "endereco": "", "forma_pagamento": "pix"})
    assert "Informe o endereço" in resp.get_data(as_text=True)
    with app.app_context():
        assert Pedido.query.count() == 0


def test_checkout_rejeita_forma_de_pagamento_invalida(client, app, produto_id, cliente_logado):
    _adicionar(client, produto_id, 6)
    resp = client.post("/checkout", data={"tipo_entrega": "retirada", "forma_pagamento": "bitcoin"})
    assert "forma de pagamento válida" in resp.get_data(as_text=True)
    with app.app_context():
        assert Pedido.query.count() == 0


def test_checkout_bloqueia_se_estoque_acabou_depois_de_adicionar(client, app, produto_id, cliente_logado):
    """Estoque nunca fica negativo, mesmo se outro cliente comprou antes."""
    _adicionar(client, produto_id, 6)
    _definir_estoque(app, produto_id, estoque=3)
    resp = client.post("/checkout", data={"tipo_entrega": "retirada", "forma_pagamento": "pix"}, follow_redirects=True)
    assert "precisam de ajuste" in resp.get_data(as_text=True)
    with app.app_context():
        assert Pedido.query.count() == 0
        assert db.session.get(Produto, produto_id).estoque == 3


def test_checkout_limita_mensagem_de_presente_a_200_caracteres(client, app, produto_id, cliente_logado):
    """US08 / CA2"""
    _adicionar(client, produto_id, 6)
    client.post("/checkout", data={"tipo_entrega": "retirada", "forma_pagamento": "pix", "mensagem_presente": "x" * 300})
    with app.app_context():
        assert len(Pedido.query.one().mensagem_presente) == 200


# ---------- US15 - Acompanhar pedidos ----------
def test_meus_pedidos_lista_apenas_pedidos_do_cliente(client, app, produto_id, cliente_logado, criar_cliente):
    _adicionar(client, produto_id, 6)
    client.post("/checkout", data={"tipo_entrega": "retirada", "forma_pagamento": "pix"})
    outro_id = criar_cliente(email="outro@teste.com")
    with app.app_context():
        db.session.add(Pedido(cliente_id=outro_id, subtotal=10, total=10, tipo_entrega="retirada"))
        db.session.commit()

    html = client.get("/pedidos").get_data(as_text=True)
    assert "#1" in html and "#2" not in html
    assert "Recebido" in html  # status legível em vez de "novo"


def test_cliente_nao_ve_pedido_de_outro_cliente(client, app, criar_cliente, login):
    dono_id = criar_cliente(email="dono@teste.com")
    with app.app_context():
        pedido = Pedido(cliente_id=dono_id, subtotal=10, total=10, tipo_entrega="retirada")
        db.session.add(pedido)
        db.session.commit()
        pedido_id = pedido.id

    criar_cliente(email="intruso@teste.com")
    login(email="intruso@teste.com")
    resp = client.get(f"/pedidos/{pedido_id}", follow_redirects=True)
    assert "não tem permissão" in resp.get_data(as_text=True)
