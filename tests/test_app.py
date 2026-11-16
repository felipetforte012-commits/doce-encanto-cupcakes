"""Testes de integração: vitrine, cadastro, login e acesso ao admin.
(Fixtures em tests/conftest.py)"""
from app import db
from app.models import Categoria, Cliente, Produto


# ---------- US04 / US05 - Vitrine e filtros ----------
def test_vitrine_lista_produtos(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Cupcake Teste" in resp.data


def test_vitrine_nao_mostra_produto_inativo(client, app, produto_id):
    with app.app_context():
        db.session.get(Produto, produto_id).ativo = False
        db.session.commit()
    assert b"Cupcake Teste" not in client.get("/").data


def test_vitrine_filtra_por_sabor_categoria_e_preco(client, app):
    with app.app_context():
        salgados = Categoria(nome="Salgados")
        db.session.add(salgados)
        db.session.commit()
        db.session.add(Produto(nome="Cupcake Frango", sabor="Frango", categoria_id=salgados.id,
                               preco=9.0, estoque=10, foto_url="http://x/y.png"))
        db.session.commit()
        salgados_id = salgados.id

    por_sabor = client.get("/?sabor=frang").get_data(as_text=True)
    assert "Cupcake Frango" in por_sabor and "Cupcake Teste" not in por_sabor

    por_categoria = client.get(f"/?categoria={salgados_id}").get_data(as_text=True)
    assert "Cupcake Frango" in por_categoria and "Cupcake Teste" not in por_categoria

    por_preco = client.get("/?preco_max=7").get_data(as_text=True)
    assert "Cupcake Teste" in por_preco and "Cupcake Frango" not in por_preco


def test_detalhe_produto_mostra_alergenos(client, app, produto_id):
    """US06 - Informações e alérgenos"""
    with app.app_context():
        db.session.get(Produto, produto_id).alergenos = "glúten, lactose"
        db.session.commit()
    html = client.get(f"/produto/{produto_id}").get_data(as_text=True)
    assert "Alérgenos" in html and "glúten, lactose" in html


def test_produto_inexistente_retorna_pagina_404_amigavel(client):
    resp = client.get("/produto/9999")
    assert resp.status_code == 404
    assert "Página não encontrada" in resp.get_data(as_text=True)


# ---------- US01 - Cadastro ----------
def test_cadastro_sucesso(client):
    resp = client.post("/cadastro", data={
        "nome": "Felipe Teste", "email": "felipe@teste.com", "senha": "12345678"
    }, follow_redirects=True)
    assert resp.status_code == 200
    with client.application.app_context():
        assert Cliente.query.filter_by(email="felipe@teste.com").first() is not None


def test_cadastro_guarda_senha_com_hash(client):
    client.post("/cadastro", data={"nome": "A", "email": "hash@teste.com", "senha": "12345678"})
    with client.application.app_context():
        cliente = Cliente.query.filter_by(email="hash@teste.com").first()
        assert cliente.senha_hash != "12345678"
        assert cliente.checar_senha("12345678")


def test_cadastro_senha_curta_e_rejeitado(client):
    resp = client.post("/cadastro", data={
        "nome": "Felipe Teste", "email": "felipe2@teste.com", "senha": "123"
    })
    assert b"m\xc3\xadnimo 8 caracteres" in resp.data
    with client.application.app_context():
        assert Cliente.query.filter_by(email="felipe2@teste.com").first() is None


def test_cadastro_email_invalido_e_rejeitado(client):
    resp = client.post("/cadastro", data={"nome": "A", "email": "sem-arroba", "senha": "12345678"})
    assert "e-mail válido" in resp.get_data(as_text=True)


def test_cadastro_email_duplicado_e_rejeitado(client, criar_cliente):
    criar_cliente(email="dup@teste.com")
    resp = client.post("/cadastro", data={
        "nome": "Outro", "email": "dup@teste.com", "senha": "12345678"
    })
    assert "já está cadastrado".encode("utf-8") in resp.data


def test_cadastro_email_duplicado_ignora_maiusculas(client, criar_cliente):
    criar_cliente(email="dup@teste.com")
    resp = client.post("/cadastro", data={"nome": "Outro", "email": "DUP@Teste.com", "senha": "12345678"})
    assert "já está cadastrado" in resp.get_data(as_text=True)


# ---------- US02 - Login / logout ----------
def test_login_sucesso(client, criar_cliente):
    criar_cliente(email="login@teste.com")
    resp = client.post("/login", data={"email": "login@teste.com", "senha": "12345678"}, follow_redirects=True)
    assert "Bem-vindo".encode("utf-8") in resp.data


def test_login_senha_invalida(client, criar_cliente):
    criar_cliente(email="login2@teste.com")
    resp = client.post("/login", data={"email": "login2@teste.com", "senha": "errada"})
    assert "inválidos" in resp.get_data(as_text=True)


def test_logout_encerra_sessao(client, cliente_logado):
    resp = client.post("/logout", follow_redirects=True)
    assert "Você saiu da sua conta" in resp.get_data(as_text=True)
    assert client.get("/pedidos").status_code == 302  # volta a exigir login


# ---------- US17 / RN11 - Admin (controle de acesso) ----------
def test_admin_area_bloqueada_para_nao_admin(client, cliente_logado):
    resp = client.get("/admin/produtos", follow_redirects=True)
    assert "restrito ao administrador".encode("utf-8") in resp.data


def test_admin_area_bloqueada_para_visitante(client):
    resp = client.get("/admin/pedidos")
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]


def test_admin_area_acessivel_para_admin(client, admin_logado):
    resp = client.get("/admin/produtos")
    assert resp.status_code == 200
    assert "Gerenciar produtos".encode("utf-8") in resp.data
