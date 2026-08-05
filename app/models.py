from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class Cliente(UserMixin, db.Model):
    __tablename__ = "cliente"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    pedidos = db.relationship("Pedido", backref="cliente", lazy=True)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def checar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)


@login_manager.user_loader
def load_user(user_id):
    return Cliente.query.get(int(user_id))


class Categoria(db.Model):
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)

    produtos = db.relationship("Produto", backref="categoria", lazy=True)


class Produto(db.Model):
    __tablename__ = "produto"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    sabor = db.Column(db.String(80), nullable=False)
    descricao = db.Column(db.Text)
    alergenos = db.Column(db.String(255))
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    foto_url = db.Column(db.String(255))
    estoque = db.Column(db.Integer, default=0, nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categoria.id"), nullable=False)

    itens_pedido = db.relationship("ItemPedido", backref="produto", lazy=True)

    def disponivel(self):
        return self.ativo and self.estoque > 0


class Pedido(db.Model):
    __tablename__ = "pedido"

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    status = db.Column(
        db.String(20), default="novo", nullable=False
    )  # novo, em_preparo, saiu_para_entrega, entregue, cancelado
    tipo_entrega = db.Column(db.String(20), default="entrega")  # entrega ou retirada
    endereco_entrega = db.Column(db.String(255))
    forma_pagamento = db.Column(db.String(20))  # cartao, pix, boleto
    status_pagamento = db.Column(db.String(20), default="pendente")  # pendente, aprovado, recusado
    subtotal = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    taxa_entrega = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    total = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    mensagem_presente = db.Column(db.String(200))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    itens = db.relationship("ItemPedido", backref="pedido", lazy=True, cascade="all, delete-orphan")


class ItemPedido(db.Model):
    __tablename__ = "item_pedido"

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedido.id"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)

    def subtotal_item(self):
        return self.quantidade * float(self.preco_unitario)
