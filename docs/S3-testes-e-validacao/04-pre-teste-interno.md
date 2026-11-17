# Pré-teste interno (exploratório, com apoio de IA)

> **Natureza deste teste:** teste exploratório feito pelo desenvolvedor **com apoio de uma
> ferramenta de IA**, que simulou 5 perfis de usuário no site publicado. **Não substitui** a
> validação com os 5 colegas exigida na Situação 3: os perfis abaixo são fictícios, e as
> avaliações dos colegas reais ficam em `03-relatorio-das-avaliacoes.md`.
>
> **Data:** 17/11/2026 · **Ambiente:** https://doce-encanto-cupcakes.onrender.com (produção, TiDB Cloud)
> **Objetivo:** encontrar e corrigir problemas antes de enviar o sistema aos testadores.

## Perfis simulados

| Perfil (fictício) | Foco | Como foi executado |
|---|---|---|
| P1 – iniciante no celular | Primeira impressão, layout em tela de 390 px, compra com retirada | Navegador (visão de celular) + script |
| P2 – comprando presente | Carrinho com 2 sabores, entrega, dedicatória, acompanhamento do status | Script com sessão própria |
| P3 – usuário apressado | Erros de preenchimento (13 entradas inválidas) | Script com sessão própria |
| P4 – usuário curioso | Limites e segurança (admin, pedido alheio, `<script>`, 404, CSRF, redirecionamento) | Script com sessão própria |
| P5 – acessibilidade | Leitor de tela, rótulos, contraste, sessão (carrinho antes do login, sair) | Script com sessão própria |

Dados criados no banco pelo pré-teste: contas `ana.perfil1…`, `bruno.perfil2…`, `diego.perfil4…`,
`fernanda.perfil5…@exemplo.com` e os pedidos **#30001** e **#30002**, cancelados ao final com o
estoque devolvido.

## Achados e tratamento

| ID | Achado | Perfil | Tratamento | Status |
|---|---|---|---|---|
| PT01 | Categorias trocadas nos dados: "Diet Baunilha" em *Salgados* e "Frango com Catupiry" em *Diet/Sem Açúcar* | P5 | Correção de dados pelo painel do admin (Editar produto) | ⏳ Pendente (manual) |
| PT02 | "Chocolate Belga" e "Diet Baunilha" com a mesma foto | P1 | Trocar a URL da foto pelo painel do admin | ⏳ Pendente (manual) |
| PT03 | No celular, a foto do produto ocupava a tela inteira e escondia o botão "Adicionar" | P1 | Foto limitada a 35% da altura da tela no celular | ✅ Corrigido |
| PT04 | No celular, os filtros ocupavam meia tela antes dos produtos | P1 | Filtros recolhidos atrás de um botão "🔍 Filtros" (abertos automaticamente quando há filtro ativo) | ✅ Corrigido |
| PT05 | Quantidade "1,5" mostrava "mínimo 6 unidades" | P3 | Mensagem específica: "Digite a quantidade como um número inteiro…" | ✅ Corrigido |
| PT06 | Leitor de tela lia "Ver detalhes" 5 vezes sem dizer o produto | P5 | Texto oculto visualmente: "Ver detalhes do *nome do cupcake*" | ✅ Corrigido |
| PT07 | Primeira visita mostra a tela do Render "SERVICE WAKING UP" (até ~1 min) | P1 | Limitação do plano gratuito; aviso incluído no formulário de teste e no manual | ℹ️ Documentado |
| PT08 | Números de pedido saltam de #1 para #30001 | P2 | Comportamento do TiDB (reserva de IDs em blocos); não afeta o funcionamento | ℹ️ Documentado |
| PT09 | Sem aviso ativo quando o status do pedido muda | P2 | Limitação conhecida (US16) | ℹ️ Melhoria futura |
| PT10 | Não existe "Esqueci minha senha" | P3, P5 | Depende de envio de e-mail | ℹ️ Melhoria futura |
| PT11 | Busca com texto de injeção SQL recebe página de bloqueio do Cloudflare (em inglês) | P4 | Proteção da hospedagem, anterior à aplicação; não controlável pelo sistema | ℹ️ Documentado |

## Falsos positivos (descartados após conferência)

| Achado inicial | Por que foi descartado |
|---|---|
| Filtros "retornando 0 produtos" | Erro na expressão regular do script de teste; o filtro funciona (Doces 3, Salgados 1, Diet 1) |
| Nome com 300 caracteres "aceito" | O perfil já estava logado e o cadastro redireciona usuários logados; deslogado, o site recusa corretamente |
| Contraste do texto cinza 4,46:1 | O script supôs a cor de versões antigas do Bootstrap; no Bootstrap 5.3.3 a cor é `rgba(33,37,41,.75)`, com contraste de ~6,6:1 |
| Sair via GET retornando 403 | Bloqueio temporário do Cloudflare após o teste de injeção; para visitante comum a resposta é 405 (correto) |

## O que funcionou (resumo)

- Compra completa com retirada e com entrega; total correto (6 × R$ 6,50 + R$ 8,00 = R$ 47,00).
- As 13 entradas inválidas do perfil P3 geraram mensagens claras, sem erro 500.
- Todas as proteções testadas pelo perfil P4 funcionaram.
- O carrinho é mantido após o login; ao sair, as páginas privadas voltam a exigir login.
- Mudança de status pelo admin aparece para o cliente; cancelamento devolve o estoque.
- Tempos com o site ativo: 0,8 a 1,7 s por página; ~2,8 s para concluir a compra.

## Testes automatizados adicionados após o pré-teste

`test_adicionar_quantidade_invalida_mostra_mensagem_especifica` (6 casos),
`test_atualizar_com_quantidade_decimal_pede_numero_inteiro`,
`test_filtros_recolhiveis_no_celular_e_abertos_quando_ativos`,
`test_link_ver_detalhes_informa_o_produto_para_leitor_de_tela`,
`test_foto_do_produto_limitada_no_celular`. Total da suíte: **119 testes, todos aprovados**.
