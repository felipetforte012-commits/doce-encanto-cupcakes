"""Testes de segurança: CSRF, redirecionamento aberto e cookies."""
import re

import pytest

from app import create_app, db
from app.models import Categoria, Cliente, Produto
from app.seguranca import caminho_interno_do_referer, destino_seguro
from tests.conftest import TestConfig


# ---------- Open redirect ----------
@pytest.mark.parametrize("alvo", ["/checkout", "/pedidos?x=1", "/"])
def test_destino_seguro_aceita_caminhos_internos(alvo):
    assert destino_seguro(alvo)


@pytest.mark.parametrize("alvo", [
    None, "", "https://site-falso.com", "//site-falso.com", "/\\site-falso.com",
    "javascript:alert(1)", "http:/site-falso.com", "pedidos",
])
def test_destino_seguro_recusa_externos(alvo):
    assert not destino_seguro(alvo)


def test_referer_so_e_aceito_se_for_do_mesmo_site():
    assert caminho_interno_do_referer("http://loja.com/carrinho?a=1", "loja.com") == "/carrinho?a=1"
    assert caminho_interno_do_referer("http://outro.com/carrinho", "loja.com") is None
    assert caminho_interno_do_referer(None, "loja.com") is None


def test_login_ignora_next_externo(client, criar_cliente):
    criar_cliente(email="r@teste.com")
    resp = client.post("/login?next=https://site-falso.com",
                       data={"email": "r@teste.com", "senha": "12345678"})
    assert resp.status_code == 302
    assert "site-falso" not in resp.headers["Location"]


def test_login_respeita_next_interno(client, criar_cliente):
    criar_cliente(email="r2@teste.com")
    resp = client.post("/login?next=/pedidos", data={"email": "r2@teste.com", "senha": "12345678"})
    assert resp.headers["Location"].endswith("/pedidos")


def test_logout_por_get_nao_e_permitido(client, cliente_logado):
    """Um link/imagem externo não consegue deslogar o usuário."""
    assert client.get("/logout").status_code == 405


# ---------- CSRF (ligado, como em produção) ----------
class ConfigComCSRF(TestConfig):
    WTF_CSRF_ENABLED = True


@pytest.fixture
def app_csrf():
    app = create_app(ConfigComCSRF)
    with app.app_context():
        db.create_all()
        categoria = Categoria(nome="Doces")
        db.session.add(categoria)
        db.session.commit()
        db.session.add(Produto(nome="P", sabor="S", preco=6, estoque=20,
                               foto_url="http://x/y.png", categoria_id=categoria.id))
        cliente = Cliente(nome="C", email="c@teste.com")
        cliente.set_senha("12345678")
        db.session.add(cliente)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


def _token(html):
    return re.search(r'name="csrf_token" value="([^"]+)"', html).group(1)


def test_post_sem_token_csrf_e_bloqueado(app_csrf):
    client = app_csrf.test_client()
    resp = client.post("/carrinho/adicionar/1", data={"quantidade": 6}, follow_redirects=True)
    assert "sessão expirou" in resp.get_data(as_text=True)
    with client.session_transaction() as sess:
        assert not sess.get("carrinho")


def test_post_com_token_csrf_valido_funciona(app_csrf):
    client = app_csrf.test_client()
    token = _token(client.get("/produto/1").get_data(as_text=True))
    client.post("/carrinho/adicionar/1", data={"quantidade": 6, "csrf_token": token})
    with client.session_transaction() as sess:
        assert sess["carrinho"] == {"1": 6}


def test_login_sem_token_csrf_e_bloqueado(app_csrf):
    client = app_csrf.test_client()
    resp = client.post("/login", data={"email": "c@teste.com", "senha": "12345678"}, follow_redirects=True)
    assert "Bem-vindo" not in resp.get_data(as_text=True)


# ---------- Cookies ----------
def test_cookie_de_sessao_nao_acessivel_por_javascript(app_csrf):
    client = app_csrf.test_client()
    client.get("/login")
    cookie = client.get_cookie("session")
    assert cookie is not None and cookie.http_only
