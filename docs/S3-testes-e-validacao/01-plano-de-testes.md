# Plano e relatório de testes: verificação e validação

> Situação-Problema 3: "Realizar e documentar os testes (verificação e validação) mostrando
> que o comportamento esperado foi realizado".

## 1. Objetivo
Demonstrar que o sistema Doce Encanto Cupcakes:
- **foi construído corretamente** (*verificação*: está de acordo com as especificações e o código não tem defeitos conhecidos);
- **é o produto certo** (*validação*: atende às necessidades de quem usa, confirmado por usuários reais).

## 2. Estratégia: Modelo V

Cada etapa de construção (lado esquerdo) tem um nível de teste correspondente (lado direito),
como na Figura 1 do material da disciplina.

| Etapa de desenvolvimento | Nível de teste | Como foi feito neste projeto | Onde está |
|---|---|---|---|
| Requisitos (user stories) | **Teste de aceitação** | 5 colegas usam o sistema publicado e preenchem o formulário | `02-formulario-de-teste.md` e `03-relatorio-das-avaliacoes.md` |
| Análise (casos de uso, telas) | **Teste de sistema** | Roteiro manual executado pelo desenvolvedor no site publicado (seção 7) | Este documento |
| Arquitetura (MVC, banco) | **Teste de integração** | Requisições HTTP simuladas passando por Controller → Model → banco → View | `tests/test_app.py`, `test_carrinho_checkout.py`, `test_admin.py`, `test_seguranca.py`, `test_frontend.py` |
| Código | **Teste unitário** | Regras do Model, formatação, configuração e JavaScript isolados | `tests/test_models.py`, `test_config.py`, `tests/js/checkout.test.mjs` |

## 3. Verificação (atividades sem executar o sistema)

| Atividade | Resultado |
|---|---|
| **Revisão de código** de todos os arquivos (`app/`, `config.py`, templates) | 11 defeitos encontrados; todos corrigidos (seção 8) |
| **Inspeção de rastreabilidade** requisito ↔ código ↔ teste | Matriz em `S1-planejamento/02-user-stories.md`. US03 e US13 não aparecem no código (pendência registrada) |
| **Inspeção do banco** (`schema.sql` × models) | Models alinhados ao script (mesmos CHECKs e índices). Detectado que o TiDB ignora CHECK: regras replicadas na aplicação |
| **Auditoria de segurança do repositório** (histórico do Git) | Nenhuma senha ou credencial real em commits. Certificado versionado é público. `.env` fora do Git |

## 4. Ambiente de testes

| Item | Testes automatizados | Testes de sistema e aceitação |
|---|---|---|
| Banco | SQLite **em memória**, recriado a cada teste (nunca toca nos dados reais) | TiDB Cloud (produção) |
| Servidor | Cliente de teste do Flask | Render — `https://doce-encanto-cupcakes.onrender.com` |
| Ferramentas | Python 3.14, pytest 8.2.2, Node.js 20 (`node --test`) | Navegadores dos testadores (computador e celular) |

## 5. Como executar os testes automatizados

```powershell
# na pasta do projeto, com o ambiente virtual .venv
.venv\Scripts\python.exe -m pytest tests -v
```
O teste de JavaScript roda automaticamente dentro do pytest (se o Node.js estiver instalado).
Para rodá-lo sozinho: `node --test tests/js/checkout.test.mjs`.

## 6. Resultado da execução automatizada

**Data:** 16/11/2026 · **Resultado: 119 testes executados, 119 aprovados, 0 falhas.**

| Arquivo | Nível | Qtd. | O que cobre |
|---|---|---|---|
| `test_app.py` | Integração | 17 | Vitrine, filtros, detalhe, 404, cadastro, login, logout, acesso ao admin |
| `test_carrinho_checkout.py` | Integração | 27 | Carrinho, estoque, checkout completo, entrega/retirada, validações, pedidos do cliente |
| `test_admin.py` | Integração | 23 | Cadastro/edição/remoção de produtos (10 entradas inválidas), status e cancelamento de pedidos |
| `test_seguranca.py` | Integração / unitário | 19 | CSRF, open redirect, logout por POST, cookie HttpOnly |
| `test_frontend.py` | Integração (View) | 16 | Menu no celular, CSRF em todos os formulários, acessibilidade, R$, imagem padrão, execução do teste JS |
| `test_models.py` | Unitário | 7 | Disponibilidade, estoque, cancelamento, rótulos, R$, horário de Brasília |
| `test_config.py` | Unitário | 6 | URL do banco, certificado TLS do TiDB, SECRET_KEY obrigatória |
| `test_definir_senha_admin.py` | Integração | 4 | Criação/troca da senha do administrador, sem duplicar usuário; senha curta ou diferente não altera nada |
| `js/checkout.test.mjs` | Unitário (front-end) | 5* | Taxa/total ao trocar entrega↔retirada, campo endereço, botão contra clique duplo |
| **Total** | | **119** | |

\* Os 5 casos de JavaScript são executados por 1 teste do pytest (`test_javascript_do_checkout_com_node`), já contado em `test_frontend.py`.

## 7. Casos de teste (sistema)

Os casos abaixo têm **teste automatizado** correspondente (coluna "Automatizado") e também
devem ser executados **manualmente no site publicado** antes da entrega (coluna "Manual").
Preencha a coluna "Manual" com ✅/❌ e a data.

| ID | US | Cenário | Entrada / passos | Resultado esperado | Automatizado | Manual |
|---|---|---|---|---|---|---|
| CT01 | US04 | Vitrine | Abrir `/` | Lista produtos ativos com foto, sabor e preço em R$ | ✅ `test_vitrine_lista_produtos` | |
| CT02 | US05 | Filtros | Filtrar sabor "choco", categoria e preço máx. | Só aparecem produtos compatíveis | ✅ `test_vitrine_filtra_por_sabor_categoria_e_preco` | |
| CT03 | US06 | Alérgenos | Abrir detalhe de produto com alérgenos | Caixa amarela com alérgenos | ✅ `test_detalhe_produto_mostra_alergenos` | |
| CT04 | US01 | Cadastro válido | Nome, e-mail novo, senha 8+ | "Conta criada com sucesso!" | ✅ `test_cadastro_sucesso` | |
| CT05 | US01 | Senha curta | Senha "123" | "mínimo 8 caracteres"; conta não criada | ✅ `test_cadastro_senha_curta_e_rejeitado` | |
| CT06 | US01 | E-mail repetido | E-mail já usado (com maiúsculas) | "Este e-mail já está cadastrado." | ✅ `test_cadastro_email_duplicado_ignora_maiusculas` | |
| CT07 | US02 | Login inválido | Senha errada | "E-mail ou senha inválidos." | ✅ `test_login_senha_invalida` | |
| CT08 | US07 | Mínimo por sabor | Quantidade 2 | "Quantidade mínima por sabor é 6 unidades." | ✅ `test_adicionar_ao_carrinho_respeita_minimo` | |
| CT09 | US07 | Estoque acumulado | Estoque 6; adicionar 6 duas vezes | Segunda vez recusada; carrinho fica com 6 | ✅ `test_adicionar_duas_vezes_considera_o_que_ja_esta_no_carrinho` | |
| CT10 | US09 | Editar acima do estoque | Atualizar para 50 com estoque 8 | "Estoque insuficiente"; quantidade mantida | ✅ `test_atualizar_acima_do_estoque_e_rejeitado` | |
| CT11 | US10 | Checkout sem login | Visitante clica "Finalizar compra" | Vai para o login e volta ao checkout depois | ✅ `test_checkout_exige_login` | |
| CT12 | US14 | Compra com entrega | 6 un. × R$ 6,00, entrega, Pix | Total R$ 44,00; estoque −6; carrinho vazio | ✅ `test_checkout_entrega_cria_pedido_baixa_estoque_e_limpa_carrinho` | |
| CT13 | US14 | Compra com retirada | Retirada | Taxa R$ 0,00; endereço vazio | ✅ `test_checkout_retirada_nao_cobra_taxa` | |
| CT14 | US14 | Entrega sem endereço | Entrega, endereço vazio | Aviso; pedido não criado | ✅ `test_checkout_entrega_sem_endereco_e_rejeitado` | |
| CT15 | US14 | Total na tela (JS) | Alternar entrega/retirada | Taxa e total mudam na hora; endereço some | ✅ `checkout.test.mjs` | |
| CT16 | — | Estoque acabou antes de pagar | Estoque cai para 3 com 6 no carrinho | Compra bloqueada; estoque não fica negativo | ✅ `test_checkout_bloqueia_se_estoque_acabou_depois_de_adicionar` | |
| CT17 | US08 | Dedicatória longa | 300 caracteres | Gravados apenas 200 | ✅ `test_checkout_limita_mensagem_de_presente_a_200_caracteres` | |
| CT18 | US15 | Privacidade | Cliente abre pedido de outro | "Você não tem permissão para ver este pedido." | ✅ `test_cliente_nao_ve_pedido_de_outro_cliente` | |
| CT19 | RN11 | Admin bloqueado | Cliente comum abre `/admin/produtos` | "Acesso restrito ao administrador da loja." | ✅ `test_admin_area_bloqueada_para_nao_admin` | |
| CT20 | US17 | Cadastro de produto | Preço "7,50" | Produto salvo com R$ 7,50 | ✅ `test_admin_cadastra_produto_com_preco_em_formato_brasileiro` | |
| CT21 | US17 | Produto inválido | Preço vazio/0/negativo, sem foto, URL `javascript:` etc. | Mensagem clara, sem erro 500, dados mantidos | ✅ `test_admin_cadastro_invalido_mostra_mensagem_sem_erro_500` (10 casos) | |
| CT22 | US17 | Remoção lógica | Remover produto | Some da vitrine; continua no banco | ✅ `test_admin_remove_produto_sem_apagar_do_banco` | |
| CT23 | US18 | Mudar status | "Em preparo" | Cliente vê "Em preparo" | ✅ `test_admin_atualiza_status`, `test_cliente_acompanha_mudanca_de_status` | |
| CT24 | US18 | Cancelar pedido | Cancelar pedido de 6 un. | Estoque volta; pedido encerrado | ✅ `test_admin_cancelar_pedido_devolve_estoque` | |
| CT25 | — | Celular | Abrir em tela pequena | Menu acessível pelo botão ☰ | ✅ `test_menu_tem_botao_para_celular` | |
| CT26 | — | Segurança CSRF | Enviar formulário sem token | Bloqueado com aviso | ✅ `test_post_sem_token_csrf_e_bloqueado` | |
| CT27 | — | Open redirect | `/login?next=https://site-falso.com` | Fica no próprio site | ✅ `test_login_ignora_next_externo` | |

## 8. Defeitos encontrados na verificação e corrigidos

| ID | Defeito | Severidade | Correção (commit) | Teste de regressão |
|---|---|---|---|---|
| D01 | Conexão com TiDB dependia de pasta do PC do desenvolvedor (já apagada) | Alta | Fase 1 | `test_certificado_do_tidb_esta_no_projeto` |
| D02 | Chave secreta padrão pública permitia forjar sessão de admin | Alta | Fase 1 | `test_app_nao_sobe_sem_secret_key` |
| D03 | Senha padrão do admin pública no README; banco de produção sem nenhum administrador | Alta | Fase 4 (`definir_senha_admin.py` cria/troca o admin com senha privada) | `test_cria_admin_quando_nao_existe`, `test_troca_senha_de_admin_existente` |
| D04 | Menu inacessível no celular | Alta | Fase 2 | `test_menu_tem_botao_para_celular` |
| D05 | Estoque podia ficar negativo | Alta | Fase 2 | CT09, CT10, CT16 |
| D06 | Erro 500 ao editar produto com preço vazio | Média | Fase 2 | `test_admin_editar_com_preco_vazio_nao_quebra_e_nao_altera` |
| D07 | Sem proteção CSRF | Média | Fase 2 | CT26 |
| D08 | Redirecionamento aberto no login | Média | Fase 2 | CT27 |
| D09 | Tela de pedidos do admin sem link | Média | Fase 2 | `test_menu_do_admin_tem_links_de_produtos_e_pedidos` |
| D10 | Cancelamento não devolvia estoque | Média | Fase 2 | CT24 |
| D11 | Datas em UTC (3 h adiantadas), status técnicos, taxa errada na retirada (tela), imagem padrão fora do ar | Baixa | Fase 2 | `test_data_convertida_para_horario_de_brasilia`, CT15 |

## 9. Pré-teste interno (antes da validação)

Em 17/11/2026 foi feito um teste exploratório no site publicado, com apoio de IA simulando
5 perfis de usuário. Os achados e as correções estão em
[`04-pre-teste-interno.md`](04-pre-teste-interno.md). Esse pré-teste é uma atividade de
**verificação** e **não substitui** a validação com usuários reais descrita a seguir.

## 10. Validação com usuários (aceitação)

- **Quem:** 5 colegas de curso ou profissionais da área ("dublês de usuário").
- **Como:** cada um recebe o link do site e o [formulário de teste](02-formulario-de-teste.md),
  executa as tarefas e devolve o formulário preenchido, com prints das telas com erro.
- **Registro:** as 5 avaliações, as decisões tomadas e as correções feitas vão para o
  [relatório das avaliações](03-relatorio-das-avaliacoes.md), entregue em PDF.

## 11. Critérios de aceite da entrega

- 100% dos testes automatizados aprovados. ✅ (119/119)
- Nenhum defeito de severidade alta em aberto.
- Casos CT01–CT27 executados manualmente no site publicado.
- 5 avaliações recebidas e analisadas; cada problema relatado com decisão registrada (corrigido, não reproduzido ou adiado com justificativa).
