# 2. User stories (backlog)

> **Como este documento foi feito:** as histórias foram **reconstruídas a partir do código**,
> que cita os identificadores `US01`…`US18`, `RN07`, `RN11` e `CA1`…`CA3` nas rotas.
> O ator e a ação vêm do que o código faz; o "para quê" (benefício) é uma interpretação.
> **US03 e US13 não aparecem em nenhum ponto do código**: devem ser conferidas no
> documento original do Projeto Integrador I.
>
> Status: ✅ implementada · ⚠️ parcial · ❓ não identificada

## Resumo

| ID | História | Ator | Status | Onde está no código |
|---|---|---|---|---|
| US01 | Criar conta | Visitante | ✅ | `auth.cadastro` |
| US02 | Efetuar login | Cliente | ✅ | `auth.login` / `auth.logout` |
| US03 | *(não identificada no código)* | — | ❓ | — |
| US04 | Navegar pela vitrine | Visitante | ✅ | `main.index` |
| US05 | Filtrar produtos | Visitante | ✅ | `main.index` |
| US06 | Ver detalhes e alérgenos | Visitante | ✅ | `main.produto_detalhe` |
| US07 | Adicionar ao carrinho | Visitante | ✅ | `cart.adicionar_ao_carrinho` |
| US08 | Mensagem de presente | Cliente | ✅ | `cart.checkout` |
| US09 | Editar/remover itens do carrinho | Visitante | ✅ | `cart.atualizar_carrinho`, `cart.remover_do_carrinho` |
| US10 | Ver resumo do pedido | Cliente | ✅ | `cart.checkout` |
| US11 | Escolher forma de pagamento | Cliente | ✅ | `cart.checkout` |
| US12 | Confirmação de pagamento | Cliente | ⚠️ simulado | `cart.checkout` |
| US13 | *(não identificada no código)* | — | ❓ | — |
| US14 | Escolher entrega ou retirada | Cliente | ✅ | `cart.checkout` |
| US15 | Acompanhar status do pedido | Cliente | ✅ | `cart.meus_pedidos`, `cart.detalhe_pedido` |
| US16 | Ser informado da mudança de status | Cliente | ⚠️ sem notificação ativa | `admin.atualizar_status_pedido` |
| US17 | Gerenciar catálogo | Administrador | ✅ | `admin.*_produto` |
| US18 | Painel de pedidos recebidos | Administrador | ✅ | `admin.listar_pedidos` |

## Detalhamento

### US01 — Criar conta
**Como** visitante, **quero** criar uma conta com nome, e-mail e senha, **para** poder finalizar compras e acompanhar meus pedidos.

Critérios de aceitação:
- CA1: nome, e-mail e senha são obrigatórios; o e-mail precisa ter formato válido.
- CA2: a senha deve ter no mínimo 8 caracteres.
- CA3: não é possível cadastrar um e-mail que já existe (sem diferenciar maiúsculas de minúsculas).
- A senha é guardada com *hash*, nunca em texto puro.

### US02 — Efetuar login
**Como** cliente, **quero** entrar com e-mail e senha, **para** acessar minha conta.
- Login válido mostra "Bem-vindo(a), <nome>!".
- CA3: e-mail ou senha errados mostram a mensagem genérica "E-mail ou senha inválidos." (não revela qual dos dois está errado).
- Ao entrar a partir de uma página protegida, o cliente volta para ela (apenas endereços internos).
- O cliente pode sair da conta ("Sair").

### US03 — ❓ Não identificada
O código não faz referência à US03. **Ação:** consultar o backlog do PI I. Hipóteses comuns
nesse tipo de sistema (recuperar senha, editar perfil) estão listadas no escopo como *fora do escopo*.

### US04 — Navegar pela vitrine
**Como** visitante, **quero** ver os cupcakes disponíveis com foto, sabor e preço, **para** escolher o que comprar.
- Apenas produtos ativos aparecem; produtos sem estoque aparecem com o selo "Esgotado".

### US05 — Filtrar produtos
**Como** visitante, **quero** filtrar por categoria, sabor e preço máximo, **para** encontrar rápido o que procuro.
- Filtros podem ser combinados; há opção "Limpar".

### US06 — Ver detalhes e alérgenos
**Como** visitante, **quero** ver descrição, categoria e alérgenos de um cupcake, **para** comprar com segurança.
- Alérgenos aparecem em destaque (caixa amarela).

### US07 — Adicionar ao carrinho
**Como** visitante, **quero** adicionar uma quantidade de um sabor ao carrinho, **para** montar meu pedido.
- RN07: mínimo de 6 unidades por sabor.
- CA1: não é possível adicionar mais do que o estoque, somando o que já está no carrinho.
- Produto inativo ou esgotado não pode ser adicionado.

### US08 — Mensagem de presente
**Como** cliente, **quero** escrever uma dedicatória no pedido, **para** enviar os cupcakes como presente.
- CA2: limite de 200 caracteres.

### US09 — Editar ou remover itens do carrinho
**Como** visitante, **quero** alterar a quantidade ou remover itens, **para** ajustar meu pedido antes de pagar.
- As mesmas regras de mínimo e estoque da US07 valem na alteração.
- Itens que ficaram indisponíveis são destacados e impedem a finalização até serem ajustados.

### US10 — Resumo do pedido
**Como** cliente, **quero** ver itens, subtotal, taxa e total antes de pagar, **para** conferir o pedido.
- A finalização exige login.
- O total é atualizado na hora ao trocar entre entrega e retirada.

### US11 — Forma de pagamento
**Como** cliente, **quero** escolher cartão, Pix ou boleto, **para** pagar do meu jeito.
- Só as três opções são aceitas (validação no servidor).

### US12 — Confirmação de pagamento ⚠️
**Como** cliente, **quero** receber a confirmação do pagamento, **para** ter certeza de que o pedido foi feito.
- Mensagem "Pagamento aprovado! Pedido confirmado com sucesso." e abertura do detalhe do pedido.
- **Limitação:** o pagamento é simulado (sempre aprovado); não há gateway real.

### US13 — ❓ Não identificada
O código não faz referência à US13. **Ação:** consultar o backlog do PI I.

### US14 — Entrega ou retirada
**Como** cliente, **quero** escolher receber em casa ou retirar na loja, **para** economizar a taxa quando for conveniente.
- Entrega exige endereço e custa R$ 8,00; retirada é gratuita e esconde o campo de endereço.

### US15 — Acompanhar status do pedido
**Como** cliente, **quero** ver meus pedidos e o status de cada um, **para** saber quando vão chegar.
- O cliente só vê os próprios pedidos.
- Status exibidos: Recebido, Em preparo, Saiu para entrega, Entregue, Cancelado.

### US16 — Ser informado da mudança de status ⚠️
**Como** cliente, **quero** saber quando a loja muda o status do meu pedido, **para** me organizar.
- O status alterado pelo administrador aparece imediatamente em "Meus pedidos".
- **Limitação:** não há envio de e-mail/mensagem (notificação ativa), registrado como melhoria futura.

### US17 — Gerenciar catálogo
**Como** administrador, **quero** cadastrar, editar e remover produtos, **para** manter a vitrine atualizada.
- RN11: só administradores acessam.
- CA1: nome, sabor, preço (> 0), foto (URL http/https) e categoria são obrigatórios.
- CA2: remover tira o produto da vitrine sem apagar o histórico (remoção lógica); pode ser reativado em "Editar".

### US18 — Painel de pedidos
**Como** administrador, **quero** ver os pedidos recebidos, filtrar por status e alterar o status, **para** organizar a produção e as entregas.
- Cancelar devolve os itens ao estoque e pede confirmação; pedido cancelado não pode mais mudar de status.

## Rastreabilidade história → testes automatizados

| História | Arquivo de teste | Exemplos de testes |
|---|---|---|
| US01 | `tests/test_app.py` | `test_cadastro_sucesso`, `test_cadastro_senha_curta_e_rejeitado`, `test_cadastro_email_duplicado_e_rejeitado` |
| US02 | `tests/test_app.py`, `tests/test_seguranca.py` | `test_login_sucesso`, `test_login_senha_invalida`, `test_login_ignora_next_externo` |
| US04/05/06 | `tests/test_app.py` | `test_vitrine_lista_produtos`, `test_vitrine_filtra_por_sabor_categoria_e_preco`, `test_detalhe_produto_mostra_alergenos` |
| US07/09 | `tests/test_carrinho_checkout.py` | `test_adicionar_ao_carrinho_respeita_minimo`, `test_adicionar_duas_vezes_considera_o_que_ja_esta_no_carrinho`, `test_atualizar_acima_do_estoque_e_rejeitado` |
| US08/10/11/12/14 | `tests/test_carrinho_checkout.py`, `tests/test_frontend.py` | `test_checkout_entrega_cria_pedido_baixa_estoque_e_limpa_carrinho`, `test_checkout_retirada_nao_cobra_taxa`, `test_javascript_do_checkout_com_node` |
| US15/16 | `tests/test_carrinho_checkout.py`, `tests/test_admin.py` | `test_meus_pedidos_lista_apenas_pedidos_do_cliente`, `test_cliente_acompanha_mudanca_de_status` |
| US17 | `tests/test_admin.py` | `test_admin_cadastra_produto_com_preco_em_formato_brasileiro`, `test_admin_cadastro_invalido_mostra_mensagem_sem_erro_500` |
| US18 | `tests/test_admin.py` | `test_admin_lista_e_filtra_pedidos`, `test_admin_cancelar_pedido_devolve_estoque` |
