"""Testes unitários das regras de negócio do Model e dos filtros de exibição."""
from datetime import datetime

from app.formatacao import data_br, moeda_brl
from app.models import ItemPedido, Pedido, Produto


def _produto(estoque=10, ativo=True):
    return Produto(nome="P", sabor="S", preco=6, estoque=estoque, ativo=ativo)


def test_produto_disponivel_exige_ativo_e_estoque():
    assert _produto().disponivel()
    assert not _produto(estoque=0).disponivel()
    assert not _produto(ativo=False).disponivel()


def test_produto_tem_estoque_para_quantidade():
    produto = _produto(estoque=10)
    assert produto.tem_estoque_para(10)
    assert not produto.tem_estoque_para(11)
    assert not _produto(estoque=10, ativo=False).tem_estoque_para(6)


def test_item_subtotal():
    assert ItemPedido(quantidade=6, preco_unitario=6.5).subtotal_item() == 39.0


def test_pedido_rotulos_legiveis():
    pedido = Pedido(status="saiu_para_entrega", tipo_entrega="retirada", forma_pagamento="pix",
                    status_pagamento="aprovado")
    assert pedido.status_rotulo == "Saiu para entrega"
    assert pedido.status_cor == "primary"
    assert pedido.tipo_entrega_rotulo == "Retirada na loja"
    assert pedido.forma_pagamento_rotulo == "Pix"
    assert pedido.status_pagamento_rotulo == "Aprovado"


def test_cancelar_pedido_devolve_estoque_uma_unica_vez():
    produto = _produto(estoque=4)
    pedido = Pedido(status="em_preparo")
    pedido.itens.append(ItemPedido(produto=produto, quantidade=6, preco_unitario=6))

    pedido.cancelar()
    pedido.cancelar()  # segunda chamada não devolve de novo

    assert pedido.status == "cancelado"
    assert produto.estoque == 10
    assert not pedido.pode_mudar_status()


def test_moeda_no_formato_brasileiro():
    assert moeda_brl(6.5) == "R$ 6,50"
    assert moeda_brl(1234.5) == "R$ 1.234,50"
    assert moeda_brl(None) == "R$ 0,00"


def test_data_convertida_para_horario_de_brasilia():
    # 15:00 UTC = 12:00 em Brasília (UTC-3)
    assert data_br(datetime(2026, 11, 16, 15, 0)) == "16/11/2026 12:00"
    # virada de dia: 01:30 UTC = 22:30 do dia anterior
    assert data_br(datetime(2026, 11, 16, 1, 30)) == "15/11/2026 22:30"
    assert data_br(None) == ""
