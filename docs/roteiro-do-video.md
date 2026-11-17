# Roteiro para gravar os vídeos

O PDF da disciplina pede **dois vídeos**:

| Vídeo | Onde é pedido | Conteúdo |
|---|---|---|
| **1. Demonstração da solução** | Situação 2 e Situação 3 | O sistema funcionando, narrado por você |
| **2. Mudanças adotadas** | Situação 3 ("vídeo que explicite quais mudanças foram adotadas") | O que mudou depois das revisões e das avaliações dos 5 colegas |

> ⚠️ **Duração:** o PDF se contradiz. A Situação 3 diz "**até** cinco minutos" e o
> "Problema em Foco" diz "**pelo menos** cinco minutos". Este roteiro tem **cerca de 5 minutos**,
> o que atende às duas leituras. Se puder, confirme com o tutor.

---

## Antes de gravar (checklist)

- [ ] Abra o site **2 minutos antes** e espere carregar (ele "dorme" quando ninguém acessa).
- [ ] Tenha uma conta de **cliente** criada e saiba a senha.
- [ ] Saiba a senha do **administrador**.
- [ ] Deixe pelo menos **um pedido** já feito, para mostrar o painel do admin.
- [ ] Carrinho vazio no início.
- [ ] Feche abas, notificações e programas que não vão aparecer (WhatsApp, e-mail).
- [ ] Aumente o zoom do navegador para **110% ou 125%** (`Ctrl` + `+`): fica mais legível no vídeo.
- [ ] Leia o roteiro em voz alta uma vez antes de gravar.

## Como gravar a tela no Windows 10 (sem instalar nada)

1. Abra o navegador com o site.
2. Aperte as teclas **`Windows` + `G`** ao mesmo tempo. Abre a "Xbox Game Bar".
3. Na janelinha **"Capturar"**, clique no ícone do **microfone** para ligá-lo (ele não pode ficar riscado).
4. Clique no botão **● (Iniciar gravação)**, ou aperte **`Windows` + `Alt` + `R`**.
5. Para parar: aperte **`Windows` + `Alt` + `R`** de novo.
6. O vídeo fica em **Este Computador → Vídeos → Capturas**.

> A Game Bar grava **só a janela do navegador**: é exatamente o que precisamos.
> Se ela não abrir, use o **Clipchamp** (vem no Windows) ou o **OBS Studio** (gratuito).

---

## Vídeo 1 — Demonstração (≈ 5 minutos)

O texto entre aspas é uma **sugestão de fala**: adapte com suas palavras.

### 0:00 – 0:30 · Apresentação
**Tela:** vitrine do site.
> "Olá, meu nome é *[seu nome]*, e este é o Doce Encanto Cupcakes, meu projeto do Projeto
> Integrador Transdisciplinar em Engenharia de Software II. É uma loja virtual de cupcakes,
> feita em Python com Flask, no padrão MVC, com banco de dados TiDB Cloud, compatível com MySQL,
> e publicada na internet pelo Render."

### 0:30 – 1:00 · Vitrine e filtros (US04, US05)
**Ações:** filtrar por uma categoria → digitar um sabor → clicar em Limpar.
> "Na vitrine o cliente vê os cupcakes com foto, sabor e preço. Dá para filtrar por categoria,
> por sabor e por preço máximo."

### 1:00 – 1:30 · Detalhe e carrinho (US06, US07)
**Ações:** abrir um produto → mostrar os alérgenos → digitar **2** e adicionar (aparece o aviso) → digitar **6** e adicionar.
> "No detalhe aparecem a descrição e os alérgenos em destaque. A loja tem uma regra de negócio:
> o mínimo é de 6 unidades por sabor. Se eu tento 2, o sistema avisa. Com 6, o item vai para o carrinho."

### 1:30 – 2:00 · Ajustar o carrinho (US09)
**Ações:** mudar a quantidade para 12 → Atualizar → adicionar um segundo sabor → remover um item.
> "No carrinho eu altero quantidades e removo itens. O sistema também não deixa colocar mais
> unidades do que existem em estoque."

### 2:00 – 2:20 · Login (US01, US02)
**Ações:** clicar em Finalizar compra → o sistema pede login → entrar com a conta de cliente.
> "Para finalizar, é preciso ter conta. O sistema me leva para o login e depois volta direto
> para o pagamento. As senhas são guardadas criptografadas."

### 2:20 – 3:10 · Checkout (US08, US10, US11, US14)
**Ações:** alternar entre **Retirada** e **Entrega** (mostrar a taxa e o total mudando) → digitar endereço → escrever mensagem de presente → escolher Pix → Confirmar e pagar.
> "Aqui escolho entre entrega e retirada. Na retirada, o campo de endereço some e a taxa de
> R$ 8,00 sai do total na hora: isso é feito em JavaScript. Posso escrever uma mensagem de presente
> e escolher a forma de pagamento, que neste projeto é simulada. Ao confirmar, o pedido é gravado
> e o estoque é atualizado."

### 3:10 – 3:30 · Meus pedidos (US15)
**Ações:** mostrar o detalhe do pedido → clicar em Meus pedidos.
> "Em 'Meus pedidos' o cliente acompanha o status. Cada cliente só vê os próprios pedidos."

### 3:30 – 4:20 · Administrador (US17, US18)
**Ações:** Sair → entrar como admin → **Admin: Produtos** → Editar um produto (mudar o estoque) → Salvar → **Admin: Pedidos** → mudar o pedido para **Em preparo**.
> "Agora como administrador. No painel de produtos eu cadastro, edito e removo cupcakes. Remover
> só tira da vitrine, para não perder o histórico. No painel de pedidos eu filtro por status e
> atualizo a etapa de cada pedido. Se eu cancelar, as unidades voltam para o estoque."

*(Opcional, se der tempo: entrar de novo como cliente e mostrar o status "Em preparo".)*

### 4:20 – 4:40 · Celular
**Ações:** apertar `F12` → clicar no ícone de celular (Toggle device toolbar) → mostrar o menu ☰. *(Ou gravar um trecho no celular.)*
> "O site é responsivo: no celular, o menu fica nesse botão."

### 4:40 – 5:00 · Qualidade e encerramento
**Ações:** mostrar o repositório no GitHub (pasta `docs/` e pasta `tests/`).
> "O projeto tem 119 testes automatizados, de back-end e de front-end, e toda a documentação
> fica no GitHub: requisitos, diagramas UML, banco de dados, manual e plano de testes.
> Obrigado!"

---

## Vídeo 2 — Mudanças adotadas (2 a 5 minutos)

Grave **depois** de receber os 5 formulários e fazer as correções.
Use o [relatório das avaliações](S3-testes-e-validacao/03-relatorio-das-avaliacoes.md) como guia.

### 1. Introdução (20 s)
> "Neste vídeo mostro o que mudou no Doce Encanto depois da revisão do projeto e dos testes
> feitos por cinco colegas."

### 2. Revisão técnica — melhoria contínua (1 a 1,5 min)
Mostre rapidamente **antes → depois** (já está feito):

| Mostrar | Fala sugerida |
|---|---|
| Menu ☰ no modo celular | "O menu sumia no celular. Agora tem o botão de menu." |
| Tentar adicionar mais que o estoque | "Era possível comprar mais do que o estoque. Agora o sistema bloqueia." |
| Admin: formulário com preço vazio | "Salvar um produto sem preço dava erro. Agora aparece uma mensagem clara." |
| Cancelar pedido | "Cancelar não devolvia o estoque. Agora devolve." |
| Datas e valores | "As datas aparecem no horário de Brasília e os valores no padrão R$ 0,00." |
| Terminal com os testes passando *(opcional)* | "Os testes passaram de 10 para 119." |

### 3. Feedback dos colegas (1 a 2 min)
Para cada item da tabela "Mudanças adotadas" do relatório:
> "O(a) colega *[nome]* apontou que *[problema]*. Eu corrigi assim: *[mostrar na tela]*."

E para o que **não** foi corrigido:
> "A sugestão de *[x]* ficou para uma próxima versão, porque *[motivo]*."

### 4. Encerramento (20 s)
> "Essas mudanças estão documentadas no GitHub, na pasta docs. Obrigado!"
