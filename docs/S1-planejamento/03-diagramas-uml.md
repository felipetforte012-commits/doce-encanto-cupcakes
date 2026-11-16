# 3. Diagramas UML

> Diagramas escritos em **Mermaid**: o GitHub os desenha automaticamente ao abrir este arquivo.
> Para exportar como imagem, cole cada bloco em <https://mermaid.live> e use "Download PNG".
> Todos foram feitos a partir do código atual (`app/models.py` e `app/routes/`).

## 3.1 Diagrama de casos de uso

O Mermaid não tem um tipo próprio para casos de uso; a notação abaixo segue a UML:
atores à esquerda/direita, casos de uso em elipses e relações `<<include>>`.
O **Cliente** herda tudo o que o **Visitante** faz (generalização).

```mermaid
flowchart LR
    V["👤 Visitante"]
    C["👤 Cliente"]
    A["👤 Administrador"]

    subgraph Sistema["Sistema Doce Encanto Cupcakes"]
        UC01(["US01 Criar conta"])
        UC02(["US02 Efetuar login"])
        UC04(["US04 Navegar pela vitrine"])
        UC05(["US05 Filtrar produtos"])
        UC06(["US06 Ver detalhes e alérgenos"])
        UC07(["US07 Adicionar ao carrinho"])
        UC09(["US09 Editar/remover itens"])
        UC10(["US10 Finalizar compra"])
        UC14(["US14 Escolher entrega ou retirada"])
        UC11(["US11 Escolher pagamento"])
        UC08(["US08 Mensagem de presente"])
        UC15(["US15 Acompanhar pedidos"])
        UC17(["US17 Gerenciar produtos"])
        UC18(["US18 Gerenciar pedidos"])
        UC16(["US16 Atualizar status"])
    end

    V --- UC01
    V --- UC04
    V --- UC05
    V --- UC06
    V --- UC07
    V --- UC09
    C -. "generalização (herda Visitante)" .-> V
    C --- UC02
    C --- UC10
    C --- UC15
    UC10 -. "<<include>>" .-> UC14
    UC10 -. "<<include>>" .-> UC11
    UC08 -. "<<extend>>" .-> UC10
    UC10 -. "<<include>> login" .-> UC02
    A --- UC02
    A --- UC17
    A --- UC18
    UC18 -. "<<include>>" .-> UC16
```

## 3.2 Diagrama de classes (persistência)

Classes do Model (`app/models.py`). Atributos com tipo; métodos com as regras de negócio.

```mermaid
classDiagram
    direction LR

    class Cliente {
        +int id
        +str nome
        +str email
        -str senha_hash
        +str telefone
        +str endereco
        +bool is_admin
        +datetime criado_em
        +set_senha(senha)
        +checar_senha(senha) bool
    }

    class Categoria {
        +int id
        +str nome
    }

    class Produto {
        +int id
        +str nome
        +str sabor
        +str descricao
        +str alergenos
        +Decimal preco
        +str foto_url
        +int estoque
        +bool ativo
        +disponivel() bool
        +tem_estoque_para(quantidade) bool
    }

    class Pedido {
        +int id
        +str status
        +str tipo_entrega
        +str endereco_entrega
        +str forma_pagamento
        +str status_pagamento
        +Decimal subtotal
        +Decimal taxa_entrega
        +Decimal total
        +str mensagem_presente
        +datetime criado_em
        +status_rotulo() str
        +pode_mudar_status() bool
        +cancelar()
    }

    class ItemPedido {
        +int id
        +int quantidade
        +Decimal preco_unitario
        +subtotal_item() float
    }

    Cliente "1" --> "0..*" Pedido : faz
    Categoria "1" --> "0..*" Produto : agrupa
    Pedido "1" *-- "1..*" ItemPedido : contém
    Produto "1" --> "0..*" ItemPedido : é vendido em
```

- **Composição** Pedido ◆— ItemPedido: o item não existe sem o pedido (no banco: `ON DELETE CASCADE`).
- **Associação** Produto — ItemPedido: o produto continua existindo mesmo que o pedido acabe; por isso a remoção de produto é lógica (`ativo = falso`).

## 3.3 Diagrama de sequência — Finalizar compra (US10, US11, US12, US14)

```mermaid
sequenceDiagram
    autonumber
    actor Cli as Cliente
    participant V as View (checkout.html + checkout.js)
    participant C as Controller (cart.checkout)
    participant M as Model (Produto, Pedido, ItemPedido)
    participant BD as Banco (TiDB / MySQL)

    Cli->>V: Abre "Finalizar compra"
    V->>C: GET /checkout
    C->>C: Exige login e monta itens do carrinho (sessão)
    C->>M: Confere disponibilidade de cada item
    alt Item indisponível ou sem estoque
        C-->>Cli: Volta ao carrinho com aviso
    else Tudo disponível
        C-->>V: Renderiza resumo (subtotal, taxa, total)
    end
    Cli->>V: Escolhe entrega/retirada e pagamento
    V->>V: JavaScript recalcula taxa e total
    Cli->>V: Clica "Confirmar e pagar"
    V->>C: POST /checkout (+ token CSRF)
    C->>C: Valida tipo de entrega, pagamento e endereço
    alt Dados inválidos
        C-->>V: Formulário com mensagem de erro (dados mantidos)
    else Dados válidos
        C->>BD: SELECT produtos ... FOR UPDATE (bloqueia as linhas)
        BD-->>C: Estoque atual
        alt Estoque mudou
            C->>BD: ROLLBACK
            C-->>Cli: Volta ao carrinho com aviso
        else Estoque suficiente
            C->>M: Cria Pedido + ItemPedido e baixa o estoque
            M->>BD: INSERT pedido, INSERT item_pedido, UPDATE produto
            C->>BD: COMMIT
            C->>C: Esvazia o carrinho da sessão
            C-->>Cli: "Pagamento aprovado! Pedido confirmado" + detalhe do pedido
        end
    end
```

## 3.4 Diagrama de sequência — Administrador cancela um pedido (US18)

```mermaid
sequenceDiagram
    autonumber
    actor Adm as Administrador
    participant V as View (admin/pedidos.html)
    participant C as Controller (admin.atualizar_status_pedido)
    participant P as Model (Pedido)
    participant BD as Banco

    Adm->>V: Escolhe "Cancelado" e clica "Atualizar"
    V->>Adm: Pede confirmação (o cancelamento não pode ser desfeito)
    Adm->>V: Confirma
    V->>C: POST /admin/pedidos/{id}/status (+ token CSRF)
    C->>C: Verifica perfil de administrador (RN11)
    C->>P: pode_mudar_status()?
    alt Já cancelado
        C-->>Adm: "O pedido está cancelado e não pode mudar de status."
    else Pode mudar
        C->>P: cancelar()
        P->>P: Devolve a quantidade de cada item ao estoque
        C->>BD: COMMIT
        C-->>Adm: "Status atualizado para 'Cancelado'. Os itens voltaram para o estoque."
    end
```

## 3.5 Diagrama de atividades — Jornada de compra do cliente

```mermaid
flowchart TD
    I((Início)) --> A[Acessar a vitrine]
    A --> B{Usar filtros?}
    B -- Sim --> B1[Filtrar por categoria, sabor ou preço] --> C
    B -- Não --> C[Abrir detalhe do cupcake]
    C --> D[Informar quantidade]
    D --> E{"Quantidade de 6 ou mais<br/>e dentro do estoque?"}
    E -- Não --> E1[Mostrar aviso] --> D
    E -- Sim --> F[Item vai para o carrinho]
    F --> G{Comprar mais sabores?}
    G -- Sim --> A
    G -- Não --> H[Abrir carrinho e ajustar itens]
    H --> J{Está logado?}
    J -- Não --> J1[Entrar ou criar conta] --> K
    J -- Sim --> K[Tela de finalizar compra]
    K --> L{Entrega ou retirada?}
    L -- Entrega --> L1["Informar endereço<br/>taxa de R$ 8,00"] --> M
    L -- Retirada --> L2[Sem taxa] --> M
    M["Escolher pagamento e<br/>mensagem de presente (opcional)"] --> N[Confirmar e pagar]
    N --> O{Estoque ainda disponível?}
    O -- Não --> H
    O -- Sim --> P[Pedido criado com status Recebido]
    P --> Q[Acompanhar em Meus pedidos]
    Q --> F2((Fim))
```

## 3.6 Diagrama de estados — Pedido

Complementa os demais: mostra as transições permitidas pela regra do sistema.
O administrador pode mudar livremente entre os estados ativos; **Cancelado é final**.

```mermaid
stateDiagram-v2
    state "Em preparo" as EmPreparo
    state "Saiu para entrega" as SaiuParaEntrega

    [*] --> Recebido: cliente confirma a compra
    Recebido --> EmPreparo: admin
    EmPreparo --> SaiuParaEntrega: admin
    SaiuParaEntrega --> Entregue: admin
    Recebido --> Cancelado: admin (devolve estoque)
    EmPreparo --> Cancelado: admin (devolve estoque)
    SaiuParaEntrega --> Cancelado: admin (devolve estoque)
    Entregue --> Cancelado: admin (devolve estoque)
    Entregue --> [*]
    Cancelado --> [*]
```

> Observação: o sistema também permite ao administrador **voltar** um pedido ativo para
> um status anterior (ex.: corrigir um clique errado). Só o estado Cancelado é definitivo.
