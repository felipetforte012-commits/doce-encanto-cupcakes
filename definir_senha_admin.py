"""
Troca a senha do administrador da loja no banco configurado (.env).

Altera SOMENTE a senha do usuário admin@doceencanto.com. Não apaga nada.
A senha digitada não aparece na tela (isso é normal).

Uso:  python definir_senha_admin.py
"""
import getpass
import sys

from app import create_app, db
from app.models import Cliente

EMAIL_ADMIN = "admin@doceencanto.com"
TAMANHO_MINIMO = 8


def main():
    app = create_app()
    with app.app_context():
        url = db.engine.url
        print(f"Banco em uso: {url.get_backend_name()} | servidor: {url.host or '(arquivo local)'}")

        admin = Cliente.query.filter_by(email=EMAIL_ADMIN, is_admin=True).first()
        if admin is None:
            print(f"Administrador {EMAIL_ADMIN} não encontrado. Rode antes: python seed.py")
            return 1

        senha = getpass.getpass(f"Nova senha (mín. {TAMANHO_MINIMO} caracteres; não aparece ao digitar): ")
        confirmacao = getpass.getpass("Digite a nova senha de novo: ")

        if len(senha) < TAMANHO_MINIMO:
            print(f"Senha muito curta. Use pelo menos {TAMANHO_MINIMO} caracteres. Nada foi alterado.")
            return 1
        if senha != confirmacao:
            print("As duas senhas não são iguais. Nada foi alterado.")
            return 1

        admin.set_senha(senha)
        db.session.commit()
        print("Senha do administrador alterada com sucesso.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
