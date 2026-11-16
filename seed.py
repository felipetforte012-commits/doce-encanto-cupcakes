"""
Script para popular o banco de dados com dados iniciais (categorias, produtos e um usuário admin).
Execute com: python seed.py
"""
import os

from app import create_app, db
from app.models import Cliente, Categoria, Produto

app = create_app()

with app.app_context():
    db.create_all()

    if not Categoria.query.first():
        doces = Categoria(nome="Doces")
        salgados = Categoria(nome="Salgados")
        diet = Categoria(nome="Diet/Sem Açúcar")
        db.session.add_all([doces, salgados, diet])
        db.session.commit()

        produtos = [
            Produto(nome="Cupcake Red Velvet", sabor="Red Velvet", categoria_id=doces.id,
                    preco=6.50, estoque=48, alergenos="glúten, ovo, lactose",
                    foto_url="https://images.unsplash.com/photo-1614707267537-b85aaf00c4b7?w=400",
                    descricao="Massa aveludada com cobertura de cream cheese."),
            Produto(nome="Cupcake Chocolate Belga", sabor="Chocolate", categoria_id=doces.id,
                    preco=7.00, estoque=36, alergenos="glúten, ovo, lactose",
                    foto_url="https://images.unsplash.com/photo-1587668178277-295251f900ce?w=400",
                    descricao="Chocolate belga 70% cacau com ganache."),
            Produto(nome="Cupcake Limão Siciliano", sabor="Limão", categoria_id=doces.id,
                    preco=6.00, estoque=24, alergenos="glúten, ovo, lactose",
                    foto_url="https://images.unsplash.com/photo-1519869325930-281384150729?w=400",
                    descricao="Massa cítrica com cobertura de merengue."),
            Produto(nome="Cupcake Frango com Catupiry", sabor="Frango c/ Catupiry", categoria_id=salgados.id,
                    preco=7.50, estoque=30, alergenos="glúten, lactose",
                    foto_url="https://images.unsplash.com/photo-1550617931-e17a7b70dce2?w=400",
                    descricao="Versão salgada, ideal para festas."),
            Produto(nome="Cupcake Diet Baunilha", sabor="Baunilha", categoria_id=diet.id,
                    preco=7.00, estoque=18, alergenos="glúten, ovo",
                    foto_url="https://images.unsplash.com/photo-1587668178277-295251f900ce?w=400",
                    descricao="Adoçado com xilitol, sem açúcar."),
        ]
        db.session.add_all(produtos)
        db.session.commit()
        print("Categorias e produtos de exemplo criados.")

    if not Cliente.query.filter_by(email="admin@doceencanto.com").first():
        # Em produção defina ADMIN_SENHA (ou troque depois com definir_senha_admin.py):
        # a senha padrão abaixo é pública no repositório e serve só para uso local.
        senha_admin = os.environ.get("ADMIN_SENHA") or "admin12345"
        admin = Cliente(nome="Administrador da Loja", email="admin@doceencanto.com", is_admin=True)
        admin.set_senha(senha_admin)
        db.session.add(admin)
        db.session.commit()
        if os.environ.get("ADMIN_SENHA"):
            print("Usuário admin criado -> email: admin@doceencanto.com (senha definida em ADMIN_SENHA)")
        else:
            print("Usuário admin criado -> email: admin@doceencanto.com | senha: admin12345 "
                  "(TROQUE com: python definir_senha_admin.py)")

    print("Banco de dados populado com sucesso.")
