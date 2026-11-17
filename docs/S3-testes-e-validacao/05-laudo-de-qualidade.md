# Laudo de Qualidade — Doce Encanto Cupcakes

> Seção "Laudo de Qualidade" do documento de entrega (`PIT_atividade.docx`):
> "Insira a seguir o laudo de qualidade do sistema, apontando os erros e as correções.
> Não esqueça de coletar as evidências para inseri-las no laudo."

| Item | Informação |
|---|---|
| Sistema | Doce Encanto Cupcakes — loja virtual de cupcakes (Python/Flask, MVC, TiDB Cloud, Render) |
| Versão avaliada | Publicada em https://doce-encanto-cupcakes.onrender.com (commit `41236cb`) |
| Data da avaliação | 17/11/2026 |
| Repositório | https://github.com/felipetforte012-commits/doce-encanto-cupcakes |

## 1. Atividades de verificação e validação realizadas

| Atividade | Tipo | Resultado | Detalhes |
|---|---|---|---|
| Revisão de código e de segurança | Verificação | 11 defeitos encontrados e corrigidos | `01-plano-de-testes.md`, seção 8 |
| Testes automatizados (pytest + Node) | Verificação | **119 de 119 aprovados** | Unitários, integração, segurança e front-end |
| Pré-teste interno exploratório (com apoio de IA, perfis simulados) | Verificação | 11 achados; 4 corrigidos no código | `04-pre-teste-interno.md` |
| **Teste de usabilidade moderado com 5 participantes** | **Validação** | **5 de 5 concluíram a compra**; 16 pontos registrados | `03-relatorio-das-avaliacoes.md` |

## 2. Resultado da validação com usuários

Todos os 5 participantes conseguiram concluir uma compra de ponta a ponta. Evidência: os
pedidos ficaram registrados no banco de dados com data e hora.

| Participante | Pedido | Data/hora | Entrega | Pagamento | Total |
|---|---|---|---|---|---|
| Maria das Graças Silva | #60001 | 17/11/2026 01:10 | Entrega | Pix | R$ 50,00 |
| Lucas Oliveira | #90001 | 17/11/2026 01:15 | Retirada | Cartão | R$ 90,00 |
| Ana Paula Costa | #120001 | 17/11/2026 01:21 | Entrega | Boleto | R$ 50,00 |
| Roberto Mendes | #120002 | 17/11/2026 01:25 | Entrega | Cartão | R$ 260,00 |
| Isabelle | #120003 | 17/11/2026 01:37 | Retirada | Pix | R$ 36,00 |

**Comportamentos aprovados pelos participantes:** bloqueio de campos vazios, de e-mail
inválido e de senha curta; aviso de e-mail já cadastrado, mantendo os dados digitados; login
sem diferenciar maiúsculas e minúsculas; mínimo de 6 unidades e limite de estoque, contando o
que já está no carrinho; baixa de estoque e selo "Esgotado" após a compra; carrinho mantido
após o login; bloqueio de acesso a pedido de outra pessoa; páginas privadas bloqueadas após
sair da conta; clique duplo em "Pagar" sem gerar pedido repetido; valor decimal na quantidade
bloqueado; layout adequado em tela grande.

## 3. Erros e pontos de melhoria encontrados

Gravidade: **Alta** = informação errada ao cliente; **Média** = atrapalha a tarefa;
**Baixa** = incômodo ou melhoria.

| ID | Problema | Quem encontrou | Gravidade | Evidência | Correção | Situação |
|---|---|---|---|---|---|---|
| F01 | Categorias trocadas: "Diet Baunilha" em *Salgados* e "Frango com Catupiry" em *Diet/Sem Açúcar* | Ana Paula Costa | Alta | E02 | Ajustar a categoria dos 2 produtos no painel do admin | ⏳ Pendente |
| F02 | Fotos erradas: Diet Baunilha igual à do Chocolate Belga; Frango com foto de cupcake doce | Teste moderado | Alta | E01 | Trocar as URLs das fotos no painel do admin | ⏳ Pendente |
| F03 | Busca não encontra palavra sem acento ("limao" ≠ "limão") | Teste moderado | Alta | E03, E04 | Comparar sem acentos na busca | ⏳ Pendente |
| F04 | Falta "Esqueci minha senha" (primeira conta da participante Maria ficou inacessível) | Maria das Graças Silva | Média | Contas registradas em 17/11 01:06 e 01:08 | Recuperação de senha (exige envio de e-mail) | 📌 Melhoria futura |
| F05 | Aviso de erro do cadastro continua na tela após corrigir o campo | Teste moderado | Baixa | — | Esconder o aviso ao editar o campo | ⏳ Pendente |
| F06 | Após criar a conta, não entra automaticamente e não volta ao pagamento | Lucas Oliveira | Média | Pedido #90001 | Login automático após cadastro e retorno à etapa anterior | ⏳ Pendente |
| F07 | Mensagem de presente cortada no 200º caractere sem aviso | Ana Paula Costa | Média | Pedido #120001 | Contador de caracteres no campo | ⏳ Pendente |
| F08 | Celular: botão "Remover" cortado no carrinho; total abaixo do botão de pagar | Teste moderado | Média | — | Ajustar o layout do carrinho e do checkout no celular | ⏳ Pendente |
| F09 | Retirada não mostra endereço e horário da loja | Teste moderado | Média | — | Exibir endereço e horário na opção de retirada | ⏳ Pendente |
| F10 | Entrega aceita endereço incompleto ("rua 5") e não tem CEP | Roberto Mendes | Média | Pedido #120002 | Campo de CEP e validação do endereço | ⏳ Pendente |
| F11 | Não é possível escolher data e horário da entrega | Roberto Mendes | Média | Pedido #120002 | Agendamento (exige nova coluna no banco) | 📌 Melhoria futura |
| F12 | Pix e boleto aparecem "Aprovado" na hora | Ana Paula Costa | Baixa | Pedido #120001 | Exibir "Aguardando pagamento" (pagamento é simulado) | 📌 Melhoria futura |
| F13 | Números de pedido saltam (#60001, #90001, #120001) | Teste moderado | Baixa | Seção 2 | Comportamento do TiDB (IDs reservados em blocos); sem impacto funcional | ℹ️ Documentado |
| F14 | Aviso de estoque é a mensagem padrão do navegador | Teste moderado | Baixa | — | Mensagem própria ("Só restam N unidades") | ⏳ Pendente |
| F15 | Produtos esgotados aparecem primeiro na vitrine | Teste moderado | Baixa | E01 | Ordenar os disponíveis primeiro | ⏳ Pendente |
| F16 | Primeira visita leva ~1 min (servidor gratuito em repouso) | Teste moderado | Baixa | — | Limitação do plano gratuito do Render; aviso no manual e no formulário | ℹ️ Documentado |

### Correções já aplicadas a partir do pré-teste interno (commit `171f938`)

| ID | Correção |
|---|---|
| PT03 | Foto do produto limitada no celular, para o botão "Adicionar" aparecer |
| PT04 | Filtros da vitrine recolhíveis no celular |
| PT05 | Quantidade decimal ou texto: mensagem pedindo número inteiro |
| PT06 | Link "Ver detalhes" informa o nome do produto ao leitor de tela |

## 4. Evidências

| ID | Arquivo | O que mostra |
|---|---|---|
| E01 | [`evidencias/E01-vitrine-fotos-repetidas-e-esgotados-primeiro.png`](evidencias/E01-vitrine-fotos-repetidas-e-esgotados-primeiro.png) | Chocolate Belga e Diet Baunilha com a mesma foto; Frango com foto de cupcake doce; esgotados em primeiro |
| E02 | [`evidencias/E02-filtro-diet-mostra-frango.png`](evidencias/E02-filtro-diet-mostra-frango.png) | Filtro "Diet/Sem Açúcar" exibindo o Cupcake Frango com Catupiry |
| E03 | [`evidencias/E03-busca-limao-sem-acento-sem-resultado.png`](evidencias/E03-busca-limao-sem-acento-sem-resultado.png) | Busca "limao" sem resultado |
| E04 | [`evidencias/E04-busca-limao-com-acento-funciona.png`](evidencias/E04-busca-limao-com-acento-funciona.png) | Busca "limão" encontra o Cupcake Limão Siciliano |
| — | Banco de dados (pedidos #60001 a #120003) | Realização das 5 compras, com data e hora |

Capturas feitas em 17/11/2026, no site publicado.

## 5. Parecer

O sistema **cumpre a sua finalidade**: os 5 participantes concluíram compras completas, e os
controles de segurança, de estoque e de validação funcionaram como especificado. A avaliação
encontrou **3 erros com informação errada ao cliente** (F01, F02 e F03). Dois deles são de dados
cadastrados (F01 e F02) e se corrigem pelo painel do administrador, sem alterar o código.

**Parecer: aprovado com ressalvas.** As ressalvas são a correção de F01, F02 e F03 e das
melhorias de usabilidade de gravidade média (F05 a F10, F14 e F15) antes da apresentação.
F04, F11 e F12 ficam registradas como melhorias futuras.
