# 5. Dicionário de dados

> Banco: `doce_encanto` — SGBD: TiDB Cloud (compatível com MySQL 8) — charset `utf8mb4`.
> Fonte: [`schema.sql`](../../schema.sql) e [`app/models.py`](../../app/models.py).
>
> Legenda: **PK** chave primária · **FK** chave estrangeira · **UK** valor único ·
> **NN** obrigatório (NOT NULL) · **AI** autoincremento.
> A coluna "Domínio / regra" descreve os valores válidos, que vão além do tipo de dado.

## Tabela `cliente`
Pessoas cadastradas na loja: clientes e administradores.

| Coluna | Tipo | Restrições | Padrão | Domínio / regra | Descrição |
|---|---|---|---|---|---|
| id | INT | PK, AI, NN | — | Inteiro positivo | Identificador do cliente |
| nome | VARCHAR(120) | NN | — | 1 a 120 caracteres | Nome exibido no menu e nos pedidos |
| email | VARCHAR(150) | NN, UK | — | Formato `nome@dominio.ext`, gravado em minúsculas | Login do usuário |
| senha_hash | VARCHAR(255) | NN | — | *Hash* gerado pelo Werkzeug (senha original com mínimo de 8 caracteres) | Senha protegida; a senha real nunca é gravada |
| telefone | VARCHAR(20) | — | NULL | Opcional (sem tela de edição nesta versão) | Telefone de contato |
| endereco | VARCHAR(255) | — | NULL | Opcional (sem tela de edição nesta versão) | Endereço cadastral |
| is_admin | TINYINT(1) | NN | 0 | 0 = cliente, 1 = administrador | Perfil de acesso (RN11) |
| criado_em | DATETIME | NN | CURRENT_TIMESTAMP | Data/hora em UTC (exibida em horário de Brasília) | Data do cadastro |

## Tabela `categoria`
Agrupamento dos produtos na vitrine.

| Coluna | Tipo | Restrições | Padrão | Domínio / regra | Descrição |
|---|---|---|---|---|---|
| id | INT | PK, AI, NN | — | Inteiro positivo | Identificador da categoria |
| nome | VARCHAR(50) | NN, UK | — | Valores atuais: "Doces", "Salgados", "Diet/Sem Açúcar" | Nome da categoria |

## Tabela `produto`
Cupcakes vendidos pela loja.

| Coluna | Tipo | Restrições | Padrão | Domínio / regra | Descrição |
|---|---|---|---|---|---|
| id | INT | PK, AI, NN | — | Inteiro positivo | Identificador do produto |
| nome | VARCHAR(120) | NN | — | 1 a 120 caracteres | Nome comercial |
| sabor | VARCHAR(80) | NN | — | 1 a 80 caracteres | Sabor (usado no filtro da vitrine) |
| descricao | TEXT | — | NULL | Texto livre | Descrição exibida no detalhe |
| alergenos | VARCHAR(255) | — | NULL | Lista separada por vírgulas (ex.: "glúten, ovo") | Alérgenos exibidos em destaque |
| preco | DECIMAL(10,2) | NN, CHECK ≥ 0 | — | Maior que 0 e até 99.999,99 (validado na aplicação) | Preço por unidade, em R$ |
| foto_url | VARCHAR(255) | — | NULL | URL iniciando com `http://` ou `https://` (obrigatória ao cadastrar) | Foto exibida na vitrine |
| estoque | INT | NN, CHECK ≥ 0 | 0 | Inteiro ≥ 0; nunca fica negativo | Unidades disponíveis |
| ativo | TINYINT(1) | NN | 1 | 1 = na vitrine, 0 = removido (remoção lógica) | Visibilidade na vitrine |
| categoria_id | INT | NN, FK → categoria.id | — | Categoria existente | Categoria do produto |

## Tabela `pedido`
Compra finalizada por um cliente.

| Coluna | Tipo | Restrições | Padrão | Domínio / regra | Descrição |
|---|---|---|---|---|---|
| id | INT | PK, AI, NN | — | Inteiro positivo | Número do pedido (#) |
| cliente_id | INT | NN, FK → cliente.id | — | Cliente existente | Quem fez o pedido |
| status | VARCHAR(20) | NN, CHECK | 'novo' | `novo` (Recebido), `em_preparo`, `saiu_para_entrega`, `entregue`, `cancelado` | Etapa do pedido; `cancelado` é final |
| tipo_entrega | VARCHAR(20) | NN, CHECK | 'entrega' | `entrega` ou `retirada` | Como o cliente recebe |
| endereco_entrega | VARCHAR(255) | — | NULL | Obrigatório se `tipo_entrega = entrega`; NULL na retirada | Endereço deste pedido |
| forma_pagamento | VARCHAR(20) | — | NULL | `cartao`, `pix` ou `boleto` | Forma escolhida no checkout |
| status_pagamento | VARCHAR(20) | NN, CHECK | 'pendente' | `pendente`, `aprovado`, `recusado` (hoje sempre `aprovado`: pagamento simulado) | Situação do pagamento |
| subtotal | DECIMAL(10,2) | NN | 0 | Soma de quantidade × preço dos itens | Valor dos produtos |
| taxa_entrega | DECIMAL(10,2) | NN | 0 | 8,00 para entrega; 0,00 para retirada | Taxa cobrada |
| total | DECIMAL(10,2) | NN | 0 | subtotal + taxa_entrega | Valor total cobrado |
| mensagem_presente | VARCHAR(200) | — | NULL | Até 200 caracteres (US08) | Dedicatória opcional |
| criado_em | DATETIME | NN | CURRENT_TIMESTAMP | UTC (exibido em horário de Brasília) | Data/hora da compra |

## Tabela `item_pedido`
Cada sabor comprado dentro de um pedido (entidade associativa pedido × produto).

| Coluna | Tipo | Restrições | Padrão | Domínio / regra | Descrição |
|---|---|---|---|---|---|
| id | INT | PK, AI, NN | — | Inteiro positivo | Identificador do item |
| pedido_id | INT | NN, FK → pedido.id (ON DELETE CASCADE) | — | Pedido existente | Pedido ao qual o item pertence |
| produto_id | INT | NN, FK → produto.id | — | Produto existente | Produto comprado |
| quantidade | INT | NN, CHECK ≥ 6 | 1* | Inteiro ≥ 6 (RN07) | Unidades deste sabor |
| preco_unitario | DECIMAL(10,2) | NN | — | Preço do produto no momento da compra | Mantém o histórico se o preço mudar depois |

\* O padrão `1` existe no script, mas nunca é usado: a aplicação sempre informa a quantidade (mínimo 6).

## Valores de domínio exibidos ao usuário

| Coluna | Valor gravado | Texto exibido |
|---|---|---|
| pedido.status | novo | Recebido |
| | em_preparo | Em preparo |
| | saiu_para_entrega | Saiu para entrega |
| | entregue | Entregue |
| | cancelado | Cancelado |
| pedido.tipo_entrega | entrega | Entrega no endereço |
| | retirada | Retirada na loja |
| pedido.forma_pagamento | cartao | Cartão de crédito |
| | pix | Pix |
| | boleto | Boleto |
| pedido.status_pagamento | pendente / aprovado / recusado | Pendente / Aprovado / Recusado |
