# 1. Escopo revisado — Doce Encanto Cupcakes

> Situação-Problema 1 — "Verifique e adeque seu escopo/ideia e a prepare para a execução."
> Documento revisado em 16/11/2026 a partir do código efetivamente implementado
> (ciclo de melhoria contínua / *Kaizen*).

## 1.1 Visão do produto

A **Doce Encanto Cupcakes** é uma loja virtual de cupcakes gourmet (doces, salgados e
diet). O sistema permite que clientes escolham sabores na vitrine, montem um carrinho,
finalizem a compra com entrega ou retirada e acompanhem o pedido; e permite que o
administrador da loja mantenha o catálogo e gerencie os pedidos recebidos.

| Item | Definição |
|---|---|
| Problema | Pedidos de cupcakes feitos por telefone/mensagem geram erros de quantidade, sabor e endereço, e o cliente não sabe em que etapa o pedido está. |
| Solução | Aplicação web com vitrine, carrinho, checkout e acompanhamento de status. |
| Usuários | Visitante, Cliente cadastrado e Administrador da loja. |
| Plataforma | Web responsiva (computador e celular). |
| Endereço publicado | `https://doce-encanto-cupcakes.onrender.com` (Render, plano gratuito) |

## 1.2 Atores

| Ator | Descrição |
|---|---|
| **Visitante** | Pessoa não autenticada. Navega na vitrine, vê detalhes e monta o carrinho. |
| **Cliente** | Visitante com conta. Além do que o visitante faz, finaliza compras e acompanha seus pedidos. |
| **Administrador** | Funcionário da loja (`is_admin = verdadeiro`). Gerencia produtos e pedidos. |

## 1.3 Escopo — o que ESTÁ no sistema

| Módulo | Funcionalidades | User stories |
|---|---|---|
| Conta | Cadastro, login e logout | US01, US02 |
| Vitrine | Listagem, filtros (categoria, sabor, preço máximo), detalhe com alérgenos | US04, US05, US06 |
| Carrinho | Adicionar (mínimo 6 por sabor), alterar quantidade, remover, validação de estoque | US07, US09 |
| Checkout | Resumo, entrega ou retirada, mensagem de presente, forma de pagamento (simulada) | US08, US10, US11, US12, US14 |
| Pedidos | Lista e detalhe dos pedidos do cliente, com status atualizado pela loja | US15, US16 |
| Administração | Cadastro/edição/remoção lógica de produtos; painel de pedidos com filtro e mudança de status; cancelamento devolvendo estoque | US17, US18 |

## 1.4 Fora do escopo (limitações assumidas)

| Item | Situação | Justificativa |
|---|---|---|
| Pagamento real (gateway) | **Simulado**: todo pedido é gravado como "aprovado" | Projeto acadêmico; integrar gateway exige contrato e credenciais. |
| Notificação ao cliente (e-mail/WhatsApp) | **Não implementada**: o cliente acompanha o status em "Meus pedidos" | Exigiria serviço de e-mail/mensageria. Melhoria futura. |
| Recuperação de senha | Não implementada | Depende de envio de e-mail. |
| Cadastro de categorias pela tela | Não implementado: categorias criadas pelo `seed.py` | Categorias mudam raramente. |
| Upload de fotos | Não implementado: o admin informa a URL da imagem | Hospedagem gratuita não guarda arquivos enviados. |
| Cálculo de frete por distância | Taxa fixa de R$ 8,00 | Simplificação. |
| Edição de telefone/endereço no perfil | Campos existem na tabela `cliente`, mas não há tela | Endereço é informado no checkout. |

## 1.5 Regras de negócio

| Código | Regra | Onde é garantida |
|---|---|---|
| RN07 | Quantidade mínima de **6 unidades por sabor** | `app/models.py` (`QUANTIDADE_MINIMA_POR_SABOR`) e `app/routes/cart.py` |
| RN11 | Apenas administradores alteram catálogo e pedidos | `admin_required` em `app/routes/admin.py` |
| — | Não é possível comprar mais do que o estoque disponível; o estoque nunca fica negativo | `Produto.tem_estoque_para()` + revalidação com bloqueio de linha no checkout |
| — | Produto removido sai da vitrine, mas continua no banco (histórico de pedidos) | `remover_produto` (remoção lógica, campo `ativo`) |
| — | Cancelar pedido devolve os itens ao estoque; pedido cancelado não muda mais de status | `Pedido.cancelar()` |
| — | Entrega custa R$ 8,00; retirada na loja é grátis | `TAXA_ENTREGA_PADRAO` em `cart.py` |
| — | Senha com no mínimo 8 caracteres, armazenada com *hash* | `auth.py` + Werkzeug |

## 1.6 Requisitos não funcionais

| Código | Requisito | Como foi atendido |
|---|---|---|
| RNF01 – Arquitetura | Padrão MVC | Model `app/models.py`; View `app/templates/`; Controller `app/routes/` |
| RNF02 – Linguagem | Python (lista sugerida no PDF) | Python 3 + Flask 3 |
| RNF03 – Banco | SGBD popular e de fácil manutenção | TiDB Cloud (compatível com MySQL) em produção; SQLite local |
| RNF04 – Segurança | Proteção de dados e sessões | Senhas com hash, CSRF em todos os formulários, cookies HttpOnly/Secure, sem redirecionamento externo, segredos fora do código (`.env`) |
| RNF05 – Usabilidade | Interface clara, consistente e com feedback (princípios de IHC do material) | Mensagens para toda ação, valores em R$, datas no horário de Brasília, status com nomes legíveis |
| RNF06 – Responsividade | Uso no celular | Bootstrap 5 + menu recolhível |
| RNF07 – Testabilidade | Front-end e back-end testados | 106 testes automatizados (pytest + Node) |
| RNF08 – Disponibilidade | Acesso pela internet | Render (o plano gratuito "hiberna" após 15 min sem acesso; o primeiro acesso leva ~50 s) |

## 1.7 Revisão Kaizen — o que mudou em relação à primeira versão

| # | Problema encontrado na revisão | Melhoria aplicada |
|---|---|---|
| 1 | Configuração do banco dependia de uma pasta do computador do desenvolvedor | Caminho relativo `certs/`, arquivo `.env` e testes de configuração |
| 2 | Menu desaparecia no celular | Botão de menu (hambúrguer) |
| 3 | Página de pedidos do admin sem link | Links "Admin: Produtos" e "Admin: Pedidos" |
| 4 | Era possível colocar no carrinho mais que o estoque; estoque podia ficar negativo | Validação no carrinho e revalidação com bloqueio no checkout |
| 5 | Editar produto com preço vazio causava erro 500 | Validação completa dos campos com mensagens claras |
| 6 | Cancelamento não devolvia estoque | Regra `Pedido.cancelar()` |
| 7 | Falhas de segurança (CSRF, open redirect, chave secreta fixa, senha admin pública) | Corrigidas (ver RNF04) |
| 8 | Status técnicos (`em_preparo`), datas em UTC e valores com ponto | Textos legíveis, horário de Brasília e padrão R$ 0,00 |
| 9 | Apenas 10 testes, sem checkout e sem front-end | 106 testes, incluindo JavaScript |
| 10 | TiDB ignora restrições CHECK (`tidb_enable_check_constraint` desligado) | Todas as regras também validadas na aplicação |
