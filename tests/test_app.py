import pytest
from app import create_app, db
from app.models import Cliente, Categoria, Produto


class TestConfig:
    SECRET_KEY = "teste"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    TESTING = True


@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()

        categoria = Categoria(nome="Doces")
        db.session.add(categoria)
        db.session.commit()

        produto = Produto(
            nome="Cupcake Teste", sabor="Baunilha", categoria_id=categoria.id,
            preco=6.0, estoque=50, foto_url="http://teste.com/img.png"
        )
        db.session.add(produto)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# ---------- US04 - Vitrine ----------
def test_vitrine_lista_produtos(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Cupcake Teste" in resp.data


# ---------- US01 - Cadastro ----------
def test_cadastro_sucesso(client):
    resp = client.post("/cadastro", data={
        "nome": "Felipe Teste", "email": "felipe@teste.com", "senha": "12345678"
    }, follow_redirects=True)
    assert resp.status_code == 200
    with client.application.app_context():
        assert Cliente.query.filter_by(email="felipe@teste.com").first() is not None


def test_cadastro_senha_curta_e_rejeitado(client):
    resp = client.post("/cadastro", data={
        "nome": "Felipe Teste", "email": "felipe2@teste.com", "senha": "123"
    })
    assert b"m\xc3\xadnimo 8 caracteres" in resp.data
    with client.application.app_context():
        assert Cliente.query.filter_by(email="felipe2@teste.com").first() is None


def test_cadastro_email_duplicado_e_rejeitado(client, app):
    with app.app_context():
        c = Cliente(nome="Existente", email="dup@teste.com")
        c.set_senha("12345678")
        db.session.add(c)
        db.session.commit()

    resp = client.post("/cadastro", data={
        "nome": "Outro", "email": "dup@teste.com", "senha": "12345678"
    })
    assert "já está cadastrado".encode("utf-8") in resp.data


# ---------- US02 - Login ----------
def test_login_sucesso(client, app):
    with app.app_context():
        c = Cliente(nome="Felipe", email="login@teste.com")
        c.set_senha("12345678")
        db.session.add(c)
        db.session.commit()

    resp = client.post("/login", data={"email": "login@teste.com", "senha": "12345678"}, follow_redirects=True)
    assert "Bem-vindo".encode("utf-8") in resp.data


def test_login_senha_invalida(client, app):
    with app.app_context():
        c = Cliente(nome="Felipe", email="login2@teste.com")
        c.set_senha("12345678")
        db.session.add(c)
        db.session.commit()

    resp = client.post("/login", data={"email": "login2@teste.com", "senha": "errada"})
    assert "inválidos" in resp.get_data(as_text=True)


# ---------- US07 - Carrinho ----------
def test_adicionar_ao_carrinho_respeita_minimo(client, app):
    with app.app_context():
        produto = Produto.query.first()
        produto_id = produto.id

    resp = client.post(f"/carrinho/adicionar/{produto_id}", data={"quantidade": 2}, follow_redirects=True)
    assert "mínima por sabor" in resp.get_data(as_text=True)


def test_adicionar_ao_carrinho_sucesso(client, app):
    with app.app_context():
        produto_id = Produto.query.first().id

    resp = client.post(f"/carrinho/adicionar/{produto_id}", data={"quantidade": 6}, follow_redirects=True)
    assert resp.status_code == 200
    with client.session_transaction() as sess:
        assert sess["carrinho"][str(produto_id)] == 6


# ---------- US17 - Admin (controle de acesso) ----------
def test_admin_area_bloqueada_para_nao_admin(client, app):
    with app.app_context():
        c = Cliente(nome="Cliente Comum", email="comum@teste.com")
        c.set_senha("12345678")
        db.session.add(c)
        db.session.commit()

    client.post("/login", data={"email": "comum@teste.com", "senha": "12345678"})
    resp = client.get("/admin/produtos", follow_redirects=True)
    assert "restrito ao administrador".encode("utf-8") in resp.data


def test_admin_area_acessivel_para_admin(client, app):
    with app.app_context():
        c = Cliente(nome="Admin", email="admin2@teste.com", is_admin=True)
        c.set_senha("12345678")
        db.session.add(c)
        db.session.commit()

    client.post("/login", data={"email": "admin2@teste.com", "senha": "12345678"})
    resp = client.get("/admin/produtos")
    assert resp.status_code == 200
    assert "Gerenciar produtos".encode("utf-8") in resp.data
