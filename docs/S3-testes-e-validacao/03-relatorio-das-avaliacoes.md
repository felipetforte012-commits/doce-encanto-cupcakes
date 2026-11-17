# Relatório das avaliações de usuários — Doce Encanto Cupcakes

> Situação-Problema 3: "entregue, em um arquivo PDF, as cinco opiniões/testes sobre seu
> software [...] além de um vídeo que explicite quais mudanças foram adotadas".
> Os campos de cada avaliação seguem o modelo oficial `PIT_atividade.docx` (seção "Testes da Solução").
>
> ⚠️ Itens marcados **(a confirmar)** não constam no registro do teste: confirme com a
> participante ou o participante antes da entrega (ou remova).

| Item | Informação |
|---|---|
| Projeto | Doce Encanto Cupcakes — Projeto Integrador Transdisciplinar em Engenharia de Software II |
| Aluno(a) | *(preencher)* |
| Endereço testado | https://doce-encanto-cupcakes.onrender.com |
| Repositório | https://github.com/felipetforte012-commits/doce-encanto-cupcakes |
| Data dos testes | **17/11/2026** (entre 01:06 e 01:37, conforme registros do banco de dados) |

## 1. Metodologia
Teste de usabilidade **moderado**: cinco pessoas com perfis diferentes usaram o sistema
publicado, cada uma com um objetivo de compra, enquanto o teste era conduzido e anotado.
As ações ficaram registradas no banco de dados do sistema (contas e pedidos com data e hora),
o que serve de evidência da realização dos testes.

## 2. Resumo

| # | Participante | Perfil | O que fez | Pedido (evidência) |
|---|---|---|---|---|
| 1 | Maria das Graças Silva, 58 anos | Avó, compra presente | 6 Chocolate Belga, entrega, Pix, mensagem para a neta | #60001 – R$ 50,00 – 17/11/2026 01:10 |
| 2 | Lucas Oliveira, 22 anos | Estudante com pressa | Carrinho sem conta, criou conta no meio da compra, retirada, cartão | #90001 – R$ 90,00 – 17/11/2026 01:15 |
| 3 | Ana Paula Costa | Procura cupcake sem açúcar para a mãe | Filtro Diet, removeu 6 Red Velvet, comprou 6 Diet Baunilha, mensagem longa, boleto | #120001 – R$ 50,00 – 17/11/2026 01:21 |
| 4 | Roberto Mendes | Compra para uma festa | 36 cupcakes, limite de estoque, endereço incompleto | #120002 – R$ 260,00 – 17/11/2026 01:25 |
| 5 | Isabelle *(sobrenome a confirmar)* | Usuária no computador (tela grande) | Quantidade 6.5 (bloqueada), clique duplo em "Pagar", carrinho vazio, sair da conta | #120003 – R$ 36,00 – 17/11/2026 01:37 |

## 3. Avaliações individuais (campos do modelo oficial)

### Avaliação 1
| Campo | Registro |
|---|---|
| **Nome** | Maria das Graças Silva |
| **Data do teste** | 17/11/2026 |
| **O que testou e funcionou** | Compra completa de 6 Cupcakes Chocolate Belga com entrega no endereço e pagamento por Pix, com mensagem de presente para a neta (pedido #60001, R$ 50,00). |
| **O que testou e não funcionou – O que deve ser corrigido** | Esqueceu a senha da primeira conta criada e não encontrou opção de recuperação, precisando criar outra conta. Corrigir: incluir "Esqueci minha senha". |
| **Funcionalidade não testada (faltou ou não foi implementada)** | Recuperação de senha (não implementada). Retirada na loja, cartão e boleto não foram usados por ela. |

### Avaliação 2
| Campo | Registro |
|---|---|
| **Nome** | Lucas Oliveira |
| **Data do teste** | 17/11/2026 |
| **O que testou e funcionou** | Montou o carrinho sem ter conta e o carrinho foi mantido depois de criar a conta; compra com retirada na loja e cartão (pedido #90001, R$ 90,00). Tentou abrir o pedido de outra pessoa e foi bloqueado. |
| **O que testou e não funcionou – O que deve ser corrigido** | Ao criar a conta no meio da compra, o site o levou para a vitrine em vez de voltar ao pagamento, e foi preciso digitar e-mail e senha de novo. Corrigir: entrar automaticamente após o cadastro e voltar para a etapa em que estava. |
| **Funcionalidade não testada (faltou ou não foi implementada)** | Entrega no endereço, Pix e boleto não foram usados por ele. |

### Avaliação 3
| Campo | Registro |
|---|---|
| **Nome** | Ana Paula Costa |
| **Data do teste** | 17/11/2026 |
| **O que testou e funcionou** | Colocou 6 Red Velvet no carrinho e depois removeu o item; concluiu um único pedido de 6 Cupcakes Diet Baunilha, com entrega no endereço e pagamento por boleto (pedido #120001, R$ 50,00 com a taxa de entrega). |
| **O que testou e não funcionou – O que deve ser corrigido** | (1) O filtro "Diet/Sem Açúcar" mostrou o Cupcake Frango com Catupiry, e o Diet Baunilha aparece como "Salgados": corrigir as categorias. (2) A mensagem de presente foi cortada no 200º caractere sem aviso (terminou em "…pelos n"): incluir contador de caracteres. (3) O boleto aparece como "Aprovado" na hora: mostrar "Aguardando pagamento". |
| **Funcionalidade não testada (faltou ou não foi implementada)** | Retirada na loja, Pix e cartão não foram usados por ela. |

### Avaliação 4
| Campo | Registro |
|---|---|
| **Nome** | Roberto Mendes |
| **Data do teste** | 17/11/2026 |
| **O que testou e funcionou** | Comprou 36 cupcakes para uma festa (pedido #120002, R$ 260,00); o site respeitou o limite de estoque, contando também o que já estava no carrinho. |
| **O que testou e não funcionou – O que deve ser corrigido** | O site aceitou um endereço incompleto e não pede CEP: validar o endereço e incluir CEP. Não foi possível escolher data e horário da entrega para a festa: incluir agendamento. |
| **Funcionalidade não testada (faltou ou não foi implementada)** | Agendamento de data/horário (não implementado). Retirada na loja não foi usada por ele. |

### Avaliação 5
| Campo | Registro |
|---|---|
| **Nome** | Isabelle *(sobrenome a confirmar)* |
| **Data do teste** | 17/11/2026 |
| **O que testou e funcionou** | Digitou 6.5 na quantidade do Cupcake Limão Siciliano e o sistema bloqueou o valor decimal (nada foi para o carrinho); com 6, o item entrou normalmente. O clique duplo em "Pagar" não criou pedido repetido; com o carrinho vazio, o site impede a finalização; depois de sair da conta, não é possível ver pedidos; o layout ficou bom na tela grande do computador. Compra com retirada e Pix (pedido #120003, R$ 36,00). |
| **O que testou e não funcionou – O que deve ser corrigido** | Nenhuma falha registrada nas funcionalidades testadas. |
| **Funcionalidade não testada (faltou ou não foi implementada)** | Login com senha errada (o login salvo foi usado). Uso no celular. |

## 4. Problemas consolidados e decisão

| ID | Relatado por | Problema | Tipo | Gravidade | Decisão |
|---|---|---|---|---|---|
| F01 | Ana | Categorias trocadas (Diet Baunilha em Salgados; Frango em Diet) | Bug (dados) | Alta | ✅ Corrigido pelo painel do admin (17/11/2026) |
| F02 | Teste geral | Fotos erradas (Diet Baunilha igual ao Chocolate Belga; Frango com foto de cupcake doce) | Bug (dados) | Alta | Corrigir pelo painel do admin |
| F03 | Teste geral | Busca sem acento não encontra ("limao" ≠ "limão") | Bug | Alta | Corrigir no código |
| F04 | Maria | Falta "Esqueci minha senha" | Melhoria | Média | Avaliar (depende de envio de e-mail) |
| F05 | Teste geral | Aviso de erro do cadastro permanece após corrigir o campo | Usabilidade | Baixa | Corrigir no código |
| F06 | Lucas | Após o cadastro não entra direto e não volta ao pagamento | Usabilidade | Média | Corrigir no código |
| F07 | Ana | Mensagem de presente cortada sem aviso | Usabilidade | Média | Corrigir no código (contador) |
| F08 | Teste geral | Celular: "Remover" cortado no carrinho; total abaixo do botão de pagar | Usabilidade | Média | Corrigir no código |
| F09 | Teste geral | Retirada sem endereço/horário da loja | Usabilidade | Média | Corrigir no código |
| F10 | Roberto | Endereço sem CEP e aceita "rua 5" | Usabilidade | Média | Corrigir no código |
| F11 | Roberto | Sem escolha de data/horário | Melhoria | Média | Avaliar (exige nova coluna no banco) |
| F12 | Ana | Pix/boleto "Aprovado" na hora | Melhoria | Baixa | Avaliar (muda fluxo do admin) |
| F13 | Teste geral | Números de pedido pulam (#60001, #90001, #120001) | Comportamento do TiDB | Baixa | Documentar |
| F14 | Teste geral | Mensagem de estoque é a padrão do navegador | Usabilidade | Baixa | Corrigir no código |
| F15 | Teste geral | Produtos esgotados aparecem primeiro na vitrine | Usabilidade | Baixa | Corrigir no código |
| F16 | Teste geral | Primeira visita demora ~1 min (Render gratuito) | Infraestrutura | Baixa | Documentar |

## 5. Mudanças adotadas

| ID | O que foi alterado | Onde | Registro |
|---|---|---|---|
| F01 | Categorias corrigidas: Diet Baunilha → Diet/Sem Açúcar; Frango com Catupiry → Salgados; Chocolate Belga → Doces | Painel do administrador (dados) | 17/11/2026 – evidência E05 no laudo |
| — | Estoque reposto (Chocolate Belga e Diet Baunilha, zerados pelas compras dos testes) | Painel do administrador (dados) | 17/11/2026 |
| PT03–PT06 | Correções do pré-teste interno publicadas: foto do produto menor e filtros recolhíveis no celular, mensagem de número inteiro na quantidade, link "Ver detalhes" acessível | `app/templates`, `app/static/css`, `app/routes/cart.py` | Commit `171f938` |

Os demais pontos (F02 a F16) estão registrados no [Laudo de Qualidade](05-laudo-de-qualidade.md)
com a situação de cada um: pendente, melhoria futura ou documentado.

## 6. Conclusão
Os 5 participantes concluíram compras completas, com perfis e objetivos diferentes (presente,
compra rápida, produto sem açúcar, festa e uso no computador). Isso valida o fluxo principal da
loja: vitrine, carrinho, cadastro, pagamento simulado, entrega ou retirada e acompanhamento do pedido.
Os controles de segurança e de estoque funcionaram em todos os casos testados.

Os testes mostraram principalmente **problemas de dados e de clareza**, e não falhas de
funcionamento. O erro mais grave (categorias trocadas, que levaria uma cliente que procura
produto sem açúcar a um cupcake de frango) foi corrigido logo após os testes. As sugestões de
recuperação de senha, agendamento de entrega e pagamento pendente para Pix e boleto ficaram
registradas como melhorias para uma próxima versão.
