"""Fixtures compartilhadas pelos testes.

Cada teste roda em um banco SQLite EM MEMÓRIA, criado e destruído a cada teste:
os testes nunca tocam no banco real (cupcakes.db) nem no TiDB Cloud.
"""
import pytest

from app import create_app, db
from app.models import Categoria, Cliente, Produto


class TestConfig:
    SECRET_KEY = "teste"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False  # o CSRF tem testes próprios em test_seguranca.py
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

    # O contexto é fechado ANTES dos testes: assim cada requisição abre a sua
    # própria sessão do banco, exatamente como acontece no site real (senão
    # todas as requisições compartilhariam objetos em cache e veriam dados antigos).
    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def produto_id(app):
    with app.app_context():
        return Produto.query.first().id


@pytest.fixture
def criar_cliente(app):
    """Cria um cliente no banco. Uso: criar_cliente("a@b.com", admin=True)."""
    def _criar(email="cliente@teste.com", senha="12345678", nome="Cliente Teste", admin=False):
        with app.app_context():
            c = Cliente(nome=nome, email=email, is_admin=admin)
            c.set_senha(senha)
            db.session.add(c)
            db.session.commit()
            return c.id
    return _criar


@pytest.fixture
def login(client):
    def _login(email="cliente@teste.com", senha="12345678"):
        return client.post("/login", data={"email": email, "senha": senha}, follow_redirects=True)
    return _login


@pytest.fixture
def cliente_logado(criar_cliente, login):
    cliente_id = criar_cliente()
    login()
    return cliente_id


@pytest.fixture
def admin_logado(criar_cliente, login):
    admin_id = criar_cliente(email="admin@teste.com", nome="Admin", admin=True)
    login(email="admin@teste.com")
    return admin_id
