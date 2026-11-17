"""
Define a senha do administrador da loja no banco configurado (.env).

- Se o administrador admin@doceencanto.com já existe: troca a senha dele.
- Se ainda não existe: cria esse administrador com a senha digitada.

Não apaga nada. A senha digitada não aparece na tela (isso é normal).

Uso:  python definir_senha_admin.py
"""
import getpass
import sys

from app import create_app, db
from app.models import Cliente

EMAIL_ADMIN = "admin@doceencanto.com"
NOME_ADMIN = "Administrador da Loja"
TAMANHO_MINIMO = 8


def main(app=None, ler_senha=getpass.getpass):
    app = app or create_app()
    with app.app_context():
        url = db.engine.url
        print(f"Banco em uso: {url.get_backend_name()} | servidor: {url.host or '(arquivo local)'}")

        admin = Cliente.query.filter_by(email=EMAIL_ADMIN).first()
        if admin is None:
            print(f"O administrador {EMAIL_ADMIN} ainda não existe: ele será criado.")
        else:
            print(f"Trocando a senha de {EMAIL_ADMIN}.")

        senha = ler_senha(f"Nova senha (mín. {TAMANHO_MINIMO} caracteres; não aparece ao digitar): ")
        confirmacao = ler_senha("Digite a nova senha de novo: ")

        if len(senha) < TAMANHO_MINIMO:
            print(f"Senha muito curta. Use pelo menos {TAMANHO_MINIMO} caracteres. Nada foi alterado.")
            return 1
        if senha != confirmacao:
            print("As duas senhas não são iguais. Nada foi alterado.")
            return 1

        if admin is None:
            admin = Cliente(nome=NOME_ADMIN, email=EMAIL_ADMIN, is_admin=True)
            db.session.add(admin)
        admin.is_admin = True
        admin.set_senha(senha)
        db.session.commit()
        print(f"Pronto! Entre no site com o e-mail {EMAIL_ADMIN} e a senha que você digitou.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
