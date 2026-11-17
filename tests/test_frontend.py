"""Testes de front-end: HTML gerado pelas Views e o JavaScript do checkout."""
import re
import shutil
import subprocess
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent


def test_menu_tem_botao_para_celular(client):
    """Bug corrigido: sem o navbar-toggler o menu sumia em telas pequenas."""
    html = client.get("/").get_data(as_text=True)
    assert 'class="navbar-toggler"' in html
    assert 'data-bs-target="#menuPrincipal"' in html and 'id="menuPrincipal"' in html


def test_menu_do_visitante(client):
    html = client.get("/").get_data(as_text=True)
    assert "Entrar" in html and "Cadastrar" in html and "Meus pedidos" not in html


def test_menu_do_admin_tem_links_de_produtos_e_pedidos(client, admin_logado):
    html = client.get("/").get_data(as_text=True)
    assert "Admin: Produtos" in html and "Admin: Pedidos" in html


def test_menu_do_cliente_nao_mostra_admin(client, cliente_logado):
    html = client.get("/").get_data(as_text=True)
    assert "Meus pedidos" in html and "Admin:" not in html


@pytest.mark.parametrize("url", ["/login", "/cadastro", "/produto/1"])
def test_todo_formulario_post_tem_token_csrf(client, url):
    html = client.get(url).get_data(as_text=True)
    formularios_post = re.findall(r'<form[^>]*method="post".*?</form>', html, flags=re.S)
    assert formularios_post
    for form in formularios_post:
        assert 'name="csrf_token"' in form


def test_formularios_do_admin_tem_token_csrf(client, admin_logado):
    for url in ["/admin/produtos", "/admin/produtos/novo", "/admin/produtos/1/editar"]:
        html = client.get(url).get_data(as_text=True)
        for form in re.findall(r'<form[^>]*method="post".*?</form>', html, flags=re.S):
            assert 'name="csrf_token"' in form, url


def test_filtros_recolhiveis_no_celular_e_abertos_quando_ativos(client):
    """Melhoria do pré-teste: no celular os filtros ocupavam meia tela."""
    html = client.get("/").get_data(as_text=True)
    assert 'data-bs-target="#filtrosVitrine"' in html
    assert 'id="filtrosVitrine" class="row g-2 mb-4 collapse d-md-flex"' in html  # recolhido
    filtrado = client.get("/?sabor=bau").get_data(as_text=True)
    assert "collapse d-md-flex show" in filtrado and "Filtros (ativos)" in filtrado


def test_link_ver_detalhes_informa_o_produto_para_leitor_de_tela(client):
    html = client.get("/").get_data(as_text=True)
    assert 'Ver detalhes<span class="visually-hidden"> do Cupcake Teste</span>' in html


def test_foto_do_produto_limitada_no_celular(client, produto_id):
    assert "foto-produto" in client.get(f"/produto/{produto_id}").get_data(as_text=True)
    css = client.get("/static/css/style.css").get_data(as_text=True)
    assert "max-height: 35vh" in css


def test_preco_aparece_em_reais_no_formato_brasileiro(client):
    assert "R$ 6,00" in client.get("/").get_data(as_text=True)


def test_campos_de_formulario_tem_rotulos_acessiveis(client):
    html = client.get("/cadastro").get_data(as_text=True)
    for campo in ("nome", "email", "senha"):
        assert f'<label for="{campo}"' in html and f'id="{campo}"' in html


def test_imagem_quebrada_usa_imagem_padrao_local(client):
    html = client.get("/").get_data(as_text=True)
    assert "img/cupcake.svg" in html and "onerror=" in html
    assert client.get("/static/img/cupcake.svg").status_code == 200


def test_checkout_carrega_script_e_dados_para_calculo(client, cliente_logado, produto_id):
    client.post(f"/carrinho/adicionar/{produto_id}", data={"quantidade": 6})
    html = client.get("/checkout").get_data(as_text=True)
    assert "js/checkout.js" in html
    assert 'data-subtotal="36.0"' in html and 'data-taxa="8.0"' in html
    assert client.get("/static/js/checkout.js").status_code == 200


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js não instalado")
def test_javascript_do_checkout_com_node():
    """Roda tests/js/checkout.test.mjs no executor de testes nativo do Node."""
    resultado = subprocess.run(
        ["node", "--test", str(RAIZ / "tests" / "js" / "checkout.test.mjs")],
        capture_output=True, text=True, timeout=60,
    )
    assert resultado.returncode == 0, resultado.stdout + resultado.stderr
