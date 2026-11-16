-- ============================================================
-- Projeto Físico do Banco de Dados — Doce Encanto Cupcakes
-- SGBD: MySQL 8+ / TiDB Cloud (compatível com MySQL)
--
-- ATENÇÃO (TiDB): com a variável tidb_enable_check_constraint = OFF
-- (padrão), o TiDB aceita as cláusulas CHECK abaixo mas NÃO as aplica.
-- Por isso todas essas regras também são validadas na aplicação
-- (app/routes/*.py e app/models.py), que é a garantia efetiva.
-- ============================================================

CREATE DATABASE IF NOT EXISTS doce_encanto CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE doce_encanto;

-- Tabela: cliente
CREATE TABLE cliente (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    nome          VARCHAR(120)  NOT NULL,
    email         VARCHAR(150)  NOT NULL,
    senha_hash    VARCHAR(255)  NOT NULL,
    telefone      VARCHAR(20),
    endereco      VARCHAR(255),
    is_admin      TINYINT(1)    NOT NULL DEFAULT 0,
    criado_em     DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_cliente_email UNIQUE (email)
) ENGINE=InnoDB;

-- Tabela: categoria
CREATE TABLE categoria (
    id      INT AUTO_INCREMENT PRIMARY KEY,
    nome    VARCHAR(50) NOT NULL,
    CONSTRAINT uq_categoria_nome UNIQUE (nome)
) ENGINE=InnoDB;

-- Tabela: produto
CREATE TABLE produto (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    nome          VARCHAR(120)   NOT NULL,
    sabor         VARCHAR(80)    NOT NULL,
    descricao     TEXT,
    alergenos     VARCHAR(255),
    preco         DECIMAL(10,2)  NOT NULL,
    foto_url      VARCHAR(255),
    estoque       INT            NOT NULL DEFAULT 0,
    ativo         TINYINT(1)     NOT NULL DEFAULT 1,
    categoria_id  INT            NOT NULL,
    CONSTRAINT fk_produto_categoria FOREIGN KEY (categoria_id) REFERENCES categoria(id),
    CONSTRAINT ck_produto_preco CHECK (preco >= 0),
    CONSTRAINT ck_produto_estoque CHECK (estoque >= 0)
) ENGINE=InnoDB;

-- Tabela: pedido
CREATE TABLE pedido (
    id                 INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id         INT            NOT NULL,
    status             VARCHAR(20)    NOT NULL DEFAULT 'novo',
    tipo_entrega       VARCHAR(20)    NOT NULL DEFAULT 'entrega',
    endereco_entrega   VARCHAR(255),
    forma_pagamento    VARCHAR(20),
    status_pagamento   VARCHAR(20)    NOT NULL DEFAULT 'pendente',
    subtotal           DECIMAL(10,2)  NOT NULL DEFAULT 0,
    taxa_entrega       DECIMAL(10,2)  NOT NULL DEFAULT 0,
    total              DECIMAL(10,2)  NOT NULL DEFAULT 0,
    mensagem_presente  VARCHAR(200),
    criado_em          DATETIME       NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pedido_cliente FOREIGN KEY (cliente_id) REFERENCES cliente(id),
    CONSTRAINT ck_pedido_status CHECK (status IN ('novo','em_preparo','saiu_para_entrega','entregue','cancelado')),
    CONSTRAINT ck_pedido_tipo_entrega CHECK (tipo_entrega IN ('entrega','retirada')),
    CONSTRAINT ck_pedido_status_pagamento CHECK (status_pagamento IN ('pendente','aprovado','recusado'))
) ENGINE=InnoDB;

-- Tabela: item_pedido
CREATE TABLE item_pedido (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id        INT            NOT NULL,
    produto_id       INT            NOT NULL,
    quantidade       INT            NOT NULL DEFAULT 1,
    preco_unitario   DECIMAL(10,2)  NOT NULL,
    CONSTRAINT fk_item_pedido_pedido FOREIGN KEY (pedido_id) REFERENCES pedido(id) ON DELETE CASCADE,
    CONSTRAINT fk_item_pedido_produto FOREIGN KEY (produto_id) REFERENCES produto(id),
    CONSTRAINT ck_item_pedido_quantidade CHECK (quantidade >= 6)
) ENGINE=InnoDB;

-- Índices adicionais para consultas frequentes
CREATE INDEX idx_produto_categoria ON produto(categoria_id);
CREATE INDEX idx_produto_ativo ON produto(ativo);
CREATE INDEX idx_pedido_cliente ON pedido(cliente_id);
CREATE INDEX idx_pedido_status ON pedido(status);
