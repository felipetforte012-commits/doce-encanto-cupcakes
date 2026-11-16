// Checkout: esconde o endereço e zera a taxa quando o cliente escolhe "Retirada na loja",
// atualizando o total na hora (feedback imediato ao usuário). Também evita clique duplo
// no botão de pagar. A validação definitiva continua sendo feita no servidor.
(function () {
  const dados = document.getElementById("dadosCheckout");
  if (!dados) return;

  const subtotal = parseFloat(dados.dataset.subtotal);
  const taxaPadrao = parseFloat(dados.dataset.taxa);
  const blocoEndereco = document.getElementById("blocoEndereco");
  const campoEndereco = document.getElementById("endereco");
  const valorTaxa = document.getElementById("valorTaxa");
  const valorTotal = document.getElementById("valorTotal");
  const formatar = (v) => v.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

  function atualizar() {
    const escolhido = document.querySelector('input[name="tipo_entrega"]:checked');
    const retirada = escolhido && escolhido.value === "retirada";
    const taxa = retirada ? 0 : taxaPadrao;

    blocoEndereco.hidden = retirada;
    campoEndereco.required = !retirada;
    valorTaxa.textContent = formatar(taxa);
    valorTotal.textContent = formatar(subtotal + taxa);
  }

  document.querySelectorAll('input[name="tipo_entrega"]').forEach((r) => r.addEventListener("change", atualizar));
  atualizar();

  document.getElementById("formCheckout").addEventListener("submit", function () {
    const botao = document.getElementById("btnConfirmar");
    botao.disabled = true;
    botao.textContent = "Processando pagamento...";
  });
})();
