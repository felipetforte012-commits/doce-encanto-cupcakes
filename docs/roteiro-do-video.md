# Roteiro para gravar os vídeos

O PDF da disciplina pede **dois vídeos**:

| Vídeo | Onde é pedido | Conteúdo |
|---|---|---|
| **1. Demonstração da solução** | Situação 2 e Situação 3 | O sistema funcionando, narrado por você |
| **2. Mudanças adotadas** | Situação 3 ("vídeo que explicite quais mudanças foram adotadas") | O que mudou depois das revisões e das avaliações dos 5 colegas |

> ✅ **Duração (definida no documento oficial `PIT_atividade.docx`):**
> - **Vídeo 1, narrado:** "no mínimo 5 min". Este roteiro tem **cerca de 6 minutos**, por segurança.
> - **Vídeo 2, solução atualizada:** "até 5 minutos".
>
> Os dois são entregues **como link** (veja "Como publicar o vídeo" no final).

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

## Vídeo 1 — Demonstração narrada (mínimo 5 minutos; alvo ≈ 6 minutos)

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

### 4:40 – 5:30 · Arquitetura e banco de dados
**Ações:** no GitHub, abrir `docs/S1-planejamento/03-diagramas-uml.md` (diagrama de classes) e
`04-der-e-modelo-logico.md` (DER).
> "A aplicação segue o padrão MVC: os models ficam em `app/models.py`, as telas em
> `templates` e as rotas em `routes`. Este é o diagrama de classes e este é o DER do banco,
> com as cinco tabelas: cliente, categoria, produto, pedido e item do pedido."

### 5:30 – 6:00 · Qualidade e encerramento
**Ações:** mostrar a pasta `tests/` e o `docs/S3-testes-e-validacao/05-laudo-de-qualidade.md`.
> "O projeto tem 119 testes automatizados, de back-end e de front-end. O sistema também foi
> testado por cinco pessoas, e todas concluíram a compra. O que elas encontraram está no laudo
> de qualidade. Toda a documentação está no GitHub. Obrigado!"

---

## Vídeo 2 — Solução atualizada / mudanças adotadas (até 5 minutos)

Mostra só o que **de fato mudou** (versão final, de acordo com o laudo). Alvo: 3 a 4 minutos.

| Tempo | O que FAZER na tela | O que FALAR |
|---|---|---|
| 0:00–0:20 | Mostre a vitrine | "Olá, sou *[seu nome]*, RGM *[seu RGM]*. Neste vídeo mostro as modificações feitas no Doce Encanto depois da revisão do projeto e dos testes com cinco usuários." |
| 0:20–0:50 | Escolha a categoria **Diet/Sem Açúcar** (aparece o Diet Baunilha) | "No teste, a Ana procurava um cupcake sem açúcar e, no filtro Diet, apareceu o cupcake de frango, porque as categorias estavam trocadas. Corrigi as categorias: agora o filtro Diet mostra o Diet Baunilha." |
| 0:50–1:10 | Escolha **Salgados** (aparece o Frango) | "E o Frango com Catupiry voltou para Salgados. Também repus o estoque que tinha zerado com as compras dos testes." |
| 1:10–1:50 | Aperte **F12** → ícone de celular → mostre o menu **☰** e o botão **🔍 Filtros** | "No celular, o menu não aparecia. Agora tem o botão de menu. Os filtros ocupavam meia tela, e agora ficam recolhidos neste botão, para os cupcakes aparecerem primeiro." |
| 1:50–2:10 | Ainda no celular, abra um produto | "A foto do produto ocupava a tela inteira e escondia o botão Adicionar. Agora a foto é menor e o botão aparece logo." |
| 2:10–2:40 | Volte ao computador (F12 de novo). Tente adicionar mais do que o estoque | "Antes era possível colocar no carrinho mais do que havia em estoque. Agora o sistema bloqueia e mostra quanto ainda existe." |
| 2:40–3:10 | Admin: Produtos → **Editar** → apague o **Preço** → **Salvar** → **Cancelar** | "Salvar um produto sem preço dava erro no sistema. Agora aparece uma mensagem clara e nada é alterado." |
| 3:10–3:30 | Mostre **Meus pedidos** ou **Admin: Pedidos** | "Os status aparecem com nomes claros e cores, as datas no horário de Brasília e os valores em reais." |
| 3:30–4:00 | Abra no GitHub o `docs/S3-testes-e-validacao/05-laudo-de-qualidade.md` | "Os outros pontos apontados pelos usuários, como recuperação de senha, agendamento de entrega e busca sem acento, ficaram registrados no laudo de qualidade para a próxima versão. Obrigado!" |

> ⚠️ Não diga que as **fotos** foram corrigidas: elas continuam pendentes (F02 no laudo).
> No passo do "Salvar sem preço", clique em **Cancelar** depois do aviso, para não alterar o produto.

---

## Como publicar o vídeo e pegar o link (YouTube, "Não listado")

"Não listado" significa que só quem tem o link consegue ver: o vídeo não aparece em buscas.

1. Abra **https://studio.youtube.com** e entre com sua conta Google.
2. Clique em **Criar** (canto superior direito) → **Enviar vídeos**.
3. Clique em **Selecionar arquivos** e escolha o vídeo (pasta **Vídeos → Capturas**).
4. Em **Título**, escreva, por exemplo: "Doce Encanto Cupcakes – Demonstração (PIT Engenharia de Software II)".
5. Em **Público**, marque **"Não, não é conteúdo para crianças"**. Clique em **Próxima** três vezes.
6. Em **Visibilidade**, escolha **Não listado**. Clique em **Salvar**.
7. Copie o **link do vídeo** que aparece na tela (começa com `https://youtu.be/`).
8. Cole o link no `PIT_atividade.docx`:
   - **Vídeo 1** → tabela "Codificação", linha "Link do vídeo narrado (no mínimo 5 min)".
   - **Vídeo 2** → tabela "Vídeo da Solução atualizada", linha "Link para o vídeo".
