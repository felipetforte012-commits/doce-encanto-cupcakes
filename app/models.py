from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login_manager

QUANTIDADE_MINIMA_POR_SABOR = 6  # RN07


def agora_utc():
    """Data/hora atual em UTC (sem fuso), padrão de armazenamento do banco.
    A conversão para o horário de Brasília é feita só na exibição."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Cliente(UserMixin, db.Model):
    __tablename__ = "cliente"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    criado_em = db.Column(db.DateTime, default=agora_utc)

    pedidos = db.relationship("Pedido", backref="cliente", lazy=True)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def checar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Cliente, int(user_id))


class Categoria(db.Model):
    __tablename__ = "categoria"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)

    produtos = db.relationship("Produto", backref="categoria", lazy=True)


class Produto(db.Model):
    __tablename__ = "produto"
    __table_args__ = (
        db.CheckConstraint("preco >= 0", name="ck_produto_preco"),
        db.CheckConstraint("estoque >= 0", name="ck_produto_estoque"),
        db.Index("idx_produto_categoria", "categoria_id"),
        db.Index("idx_produto_ativo", "ativo"),
    )

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

    def tem_estoque_para(self, quantidade):
        return self.disponivel() and quantidade <= self.estoque


class Pedido(db.Model):
    __tablename__ = "pedido"
    __table_args__ = (
        db.CheckConstraint(
            "status IN ('novo','em_preparo','saiu_para_entrega','entregue','cancelado')",
            name="ck_pedido_status",
        ),
        db.CheckConstraint("tipo_entrega IN ('entrega','retirada')", name="ck_pedido_tipo_entrega"),
        db.CheckConstraint(
            "status_pagamento IN ('pendente','aprovado','recusado')", name="ck_pedido_status_pagamento"
        ),
        db.Index("idx_pedido_cliente", "cliente_id"),
        db.Index("idx_pedido_status", "status"),
    )

    # valor gravado -> (texto exibido ao usuário, cor do selo Bootstrap)
    STATUS = {
        "novo": ("Recebido", "secondary"),
        "em_preparo": ("Em preparo", "warning"),
        "saiu_para_entrega": ("Saiu para entrega", "primary"),
        "entregue": ("Entregue", "success"),
        "cancelado": ("Cancelado", "danger"),
    }
    TIPOS_ENTREGA = {"entrega": "Entrega no endereço", "retirada": "Retirada na loja"}
    FORMAS_PAGAMENTO = {"cartao": "Cartão de crédito", "pix": "Pix", "boleto": "Boleto"}
    STATUS_PAGAMENTO = {"pendente": "Pendente", "aprovado": "Aprovado", "recusado": "Recusado"}

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    status = db.Column(db.String(20), default="novo", nullable=False)
    tipo_entrega = db.Column(db.String(20), default="entrega")
    endereco_entrega = db.Column(db.String(255))
    forma_pagamento = db.Column(db.String(20))
    status_pagamento = db.Column(db.String(20), default="pendente")
    subtotal = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    taxa_entrega = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    total = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    mensagem_presente = db.Column(db.String(200))
    criado_em = db.Column(db.DateTime, default=agora_utc)

    itens = db.relationship("ItemPedido", backref="pedido", lazy=True, cascade="all, delete-orphan")

    @property
    def status_rotulo(self):
        return self.STATUS.get(self.status, (self.status, "secondary"))[0]

    @property
    def status_cor(self):
        return self.STATUS.get(self.status, (self.status, "secondary"))[1]

    @property
    def tipo_entrega_rotulo(self):
        return self.TIPOS_ENTREGA.get(self.tipo_entrega, self.tipo_entrega)

    @property
    def forma_pagamento_rotulo(self):
        return self.FORMAS_PAGAMENTO.get(self.forma_pagamento, self.forma_pagamento)

    @property
    def status_pagamento_rotulo(self):
        return self.STATUS_PAGAMENTO.get(self.status_pagamento, self.status_pagamento)

    def pode_mudar_status(self):
        """Pedido cancelado é estado final (o estoque já foi devolvido)."""
        return self.status != "cancelado"

    def cancelar(self):
        """Cancela o pedido e devolve ao estoque as unidades reservadas."""
        if self.status == "cancelado":
            return
        for item in self.itens:
            item.produto.estoque += item.quantidade
        self.status = "cancelado"


class ItemPedido(db.Model):
    __tablename__ = "item_pedido"
    __table_args__ = (
        db.CheckConstraint(f"quantidade >= {QUANTIDADE_MINIMA_POR_SABOR}", name="ck_item_pedido_quantidade"),
    )

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey("pedido.id", ondelete="CASCADE"), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)

    def subtotal_item(self):
        return self.quantidade * float(self.preco_unitario)
