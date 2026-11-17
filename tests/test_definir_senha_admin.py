"""Testes do script definir_senha_admin.py (sempre no banco de TESTE em memória)."""
import definir_senha_admin
from app.models import Cliente


def _respostas(*valores):
    fila = list(valores)
    return lambda _pergunta: fila.pop(0)


def _admin(app):
    with app.app_context():
        return Cliente.query.filter_by(email=definir_senha_admin.EMAIL_ADMIN).first()


def test_cria_admin_quando_nao_existe(app):
    assert definir_senha_admin.main(app, _respostas("senhaSegura1", "senhaSegura1")) == 0
    with app.app_context():
        admin = Cliente.query.filter_by(email=definir_senha_admin.EMAIL_ADMIN).one()
        assert admin.is_admin and admin.checar_senha("senhaSegura1")


def test_troca_senha_de_admin_existente(app, criar_cliente):
    criar_cliente(email=definir_senha_admin.EMAIL_ADMIN, senha="admin12345", admin=True)
    assert definir_senha_admin.main(app, _respostas("novaSenha99", "novaSenha99")) == 0
    with app.app_context():
        admin = Cliente.query.filter_by(email=definir_senha_admin.EMAIL_ADMIN).one()
        assert admin.checar_senha("novaSenha99") and not admin.checar_senha("admin12345")
        assert Cliente.query.count() == 1  # não duplica o usuário


def test_senhas_diferentes_nao_alteram_nada(app):
    assert definir_senha_admin.main(app, _respostas("senhaSegura1", "outraSenha2")) == 1
    assert _admin(app) is None


def test_senha_curta_nao_altera_nada(app):
    assert definir_senha_admin.main(app, _respostas("123", "123")) == 1
    assert _admin(app) is None
