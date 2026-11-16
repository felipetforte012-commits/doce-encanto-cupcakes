"""Testes de integração do painel administrativo (US17, US18, US16, RN11)."""
from decimal import Decimal

import pytest

from app import db
from app.models import ItemPedido, Pedido, Produto


def _form_produto(**alteracoes):
    dados = {
        "nome": "Cupcake Novo", "sabor": "Morango", "preco": "7,50", "estoque": "30",
        "foto_url": "https://exemplo.com/foto.png", "categoria_id": "1", "ativo": "on",
        "descricao": "Delicioso", "alergenos": "glúten",
    }
    dados.update(alteracoes)
    return dados


# ---------- US17 - Cadastro de produtos ----------
def test_admin_cadastra_produto_com_preco_em_formato_brasileiro(client, app, admin_logado):
    resp = client.post("/admin/produtos/novo", data=_form_produto(), follow_redirects=True)
    assert "Produto cadastrado com sucesso" in resp.get_data(as_text=True)
    with app.app_context():
        produto = Produto.query.filter_by(nome="Cupcake Novo").one()
        assert produto.preco == Decimal("7.50")
        assert produto.estoque == 30 and produto.ativo


@pytest.mark.parametrize("campo, valor, mensagem", [
    ("nome", "", "Informe o nome"),
    ("sabor", "", "Informe o sabor"),
    ("preco", "", "preço válido"),
    ("preco", "0", "preço válido"),
    ("preco", "-5", "preço válido"),
    ("preco", "abc", "preço válido"),
    ("estoque", "-1", "estoque deve ser"),
    ("foto_url", "", "URL da foto"),
    ("foto_url", "javascript:alert(1)", "http:// ou https://"),
    ("categoria_id", "999", "categoria válida"),
])
def test_admin_cadastro_invalido_mostra_mensagem_sem_erro_500(client, app, admin_logado, campo, valor, mensagem):
    resp = client.post("/admin/produtos/novo", data=_form_produto(**{campo: valor}))
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert mensagem in html
    assert 'value="Morango"' in html or campo == "sabor"  # mantém o que foi digitado
    with app.app_context():
        assert Produto.query.filter_by(nome="Cupcake Novo").count() == 0


def test_admin_edita_produto(client, app, admin_logado, produto_id):
    client.post(f"/admin/produtos/{produto_id}/editar", data=_form_produto(nome="Editado", preco="9.90"))
    with app.app_context():
        produto = db.session.get(Produto, produto_id)
        assert produto.nome == "Editado" and produto.preco == Decimal("9.90")


def test_admin_editar_com_preco_vazio_nao_quebra_e_nao_altera(client, app, admin_logado, produto_id):
    """Bug corrigido: antes gerava erro 500 (IntegrityError)."""
    resp = client.post(f"/admin/produtos/{produto_id}/editar", data=_form_produto(preco=""))
    assert resp.status_code == 200
    assert "preço válido" in resp.get_data(as_text=True)
    with app.app_context():
        assert db.session.get(Produto, produto_id).preco == Decimal("6.00")


def test_admin_formulario_de_edicao_vem_preenchido(client, admin_logado, produto_id):
    html = client.get(f"/admin/produtos/{produto_id}/editar").get_data(as_text=True)
    assert 'value="Cupcake Teste"' in html and 'value="6.00"' in html


def test_admin_remove_produto_sem_apagar_do_banco(client, app, admin_logado, produto_id):
    """CA2 - soft delete: some da vitrine mas o registro (e histórico) continua."""
    client.post(f"/admin/produtos/{produto_id}/remover")
    with app.app_context():
        produto = db.session.get(Produto, produto_id)
        assert produto is not None and produto.ativo is False
    assert b"Cupcake Teste" not in client.get("/").data


def test_cliente_comum_nao_consegue_cadastrar_produto(client, app, cliente_logado):
    """RN11"""
    client.post("/admin/produtos/novo", data=_form_produto())
    with app.app_context():
        assert Produto.query.filter_by(nome="Cupcake Novo").count() == 0


# ---------- US18 / US16 - Pedidos ----------
@pytest.fixture
def pedido_com_6_itens(app, produto_id, criar_cliente):
    """Pedido de 6 unidades já descontadas do estoque (50 -> 44)."""
    cliente_id = criar_cliente(email="comprador@teste.com")
    with app.app_context():
        produto = db.session.get(Produto, produto_id)
        produto.estoque = 44
        pedido = Pedido(cliente_id=cliente_id, subtotal=36, total=36, tipo_entrega="retirada")
        db.session.add(pedido)
        db.session.flush()
        db.session.add(ItemPedido(pedido_id=pedido.id, produto_id=produto_id, quantidade=6, preco_unitario=6))
        db.session.commit()
        return pedido.id


def test_admin_lista_e_filtra_pedidos(client, admin_logado, pedido_com_6_itens):
    html = client.get("/admin/pedidos").get_data(as_text=True)
    assert f"#{pedido_com_6_itens}" in html
    vazio = client.get("/admin/pedidos?status=entregue").get_data(as_text=True)
    assert "Nenhum pedido encontrado" in vazio


def test_admin_atualiza_status(client, app, admin_logado, pedido_com_6_itens):
    resp = client.post(f"/admin/pedidos/{pedido_com_6_itens}/status", data={"status": "em_preparo"}, follow_redirects=True)
    assert "Em preparo" in resp.get_data(as_text=True)
    with app.app_context():
        assert db.session.get(Pedido, pedido_com_6_itens).status == "em_preparo"


def test_admin_rejeita_status_invalido(client, app, admin_logado, pedido_com_6_itens):
    resp = client.post(f"/admin/pedidos/{pedido_com_6_itens}/status", data={"status": "voando"}, follow_redirects=True)
    assert "Status inválido" in resp.get_data(as_text=True)
    with app.app_context():
        assert db.session.get(Pedido, pedido_com_6_itens).status == "novo"


def test_admin_cancelar_pedido_devolve_estoque(client, app, admin_logado, produto_id, pedido_com_6_itens):
    client.post(f"/admin/pedidos/{pedido_com_6_itens}/status", data={"status": "cancelado"})
    with app.app_context():
        assert db.session.get(Pedido, pedido_com_6_itens).status == "cancelado"
        assert db.session.get(Produto, produto_id).estoque == 50


def test_pedido_cancelado_nao_muda_mais_de_status_nem_devolve_estoque_duas_vezes(
        client, app, admin_logado, produto_id, pedido_com_6_itens):
    url = f"/admin/pedidos/{pedido_com_6_itens}/status"
    client.post(url, data={"status": "cancelado"})
    resp = client.post(url, data={"status": "novo"}, follow_redirects=True)
    client.post(url, data={"status": "cancelado"})
    assert "não pode mudar de status" in resp.get_data(as_text=True)
    with app.app_context():
        assert db.session.get(Pedido, pedido_com_6_itens).status == "cancelado"
        assert db.session.get(Produto, produto_id).estoque == 50


def test_cliente_acompanha_mudanca_de_status(client, app, pedido_com_6_itens, login, criar_cliente):
    """US15/US16 - o cliente vê em "Meus pedidos" o status definido pelo admin."""
    with app.app_context():
        db.session.get(Pedido, pedido_com_6_itens).status = "saiu_para_entrega"
        db.session.commit()
    login(email="comprador@teste.com")
    assert "Saiu para entrega" in client.get("/pedidos").get_data(as_text=True)


def test_admin_pode_ver_detalhe_de_qualquer_pedido(client, admin_logado, pedido_com_6_itens):
    resp = client.get(f"/pedidos/{pedido_com_6_itens}")
    assert resp.status_code == 200
    assert "Cupcake Teste" in resp.get_data(as_text=True)
