// Teste unitário do front-end: app/static/js/checkout.js
// Executar: node --test tests/js/checkout.test.mjs   (Node.js 18+; sem dependências)
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";

const codigo = readFileSync(new URL("../../app/static/js/checkout.js", import.meta.url), "utf8");
const normalizar = (t) => t.replace(/\s/g, " "); // toLocaleString usa espaço não separável

// Página simulada com apenas os elementos que o script usa.
function montarPagina({ subtotal = "36.0", taxa = "8.0", tipoInicial = "entrega" } = {}) {
  const ouvintes = {};
  const el = (props = {}) => ({
    hidden: false, required: false, disabled: false, textContent: "", ...props,
    addEventListener(evento, fn) { (ouvintes[props.id + ":" + evento] ||= []).push(fn); },
  });
  const radios = ["entrega", "retirada"].map((valor) =>
    el({ id: "tipo_" + valor, value: valor, checked: valor === tipoInicial }));
  const elementos = {
    dadosCheckout: el({ id: "dadosCheckout", dataset: { subtotal, taxa } }),
    blocoEndereco: el({ id: "blocoEndereco" }),
    endereco: el({ id: "endereco" }),
    valorTaxa: el({ id: "valorTaxa" }),
    valorTotal: el({ id: "valorTotal" }),
    formCheckout: el({ id: "formCheckout" }),
    btnConfirmar: el({ id: "btnConfirmar", textContent: "Confirmar e pagar" }),
  };
  const document = {
    getElementById: (id) => elementos[id] || null,
    querySelector: () => radios.find((r) => r.checked) || null,
    querySelectorAll: () => radios,
  };
  const escolher = (valor) => {
    radios.forEach((r) => { r.checked = r.value === valor; });
    (ouvintes["tipo_" + valor + ":change"] || []).forEach((fn) => fn());
  };
  const enviar = () => (ouvintes["formCheckout:submit"] || []).forEach((fn) => fn());
  new Function("document", codigo)(document);
  return { elementos, escolher, enviar };
}

test("entrega: mostra endereço obrigatório e soma a taxa", () => {
  const { elementos } = montarPagina();
  assert.equal(elementos.blocoEndereco.hidden, false);
  assert.equal(elementos.endereco.required, true);
  assert.equal(normalizar(elementos.valorTaxa.textContent), "R$ 8,00");
  assert.equal(normalizar(elementos.valorTotal.textContent), "R$ 44,00");
});

test("retirada: esconde endereço e zera a taxa", () => {
  const { elementos, escolher } = montarPagina();
  escolher("retirada");
  assert.equal(elementos.blocoEndereco.hidden, true);
  assert.equal(elementos.endereco.required, false);
  assert.equal(normalizar(elementos.valorTaxa.textContent), "R$ 0,00");
  assert.equal(normalizar(elementos.valorTotal.textContent), "R$ 36,00");
});

test("voltar para entrega recoloca a taxa", () => {
  const { elementos, escolher } = montarPagina({ tipoInicial: "retirada" });
  escolher("entrega");
  assert.equal(normalizar(elementos.valorTotal.textContent), "R$ 44,00");
});

test("enviar o formulário desativa o botão (evita pedido duplicado)", () => {
  const { elementos, enviar } = montarPagina();
  enviar();
  assert.equal(elementos.btnConfirmar.disabled, true);
  assert.match(elementos.btnConfirmar.textContent, /Processando/);
});

test("valores com centavos são formatados corretamente", () => {
  const { elementos } = montarPagina({ subtotal: "1234.5", taxa: "8.0" });
  assert.equal(normalizar(elementos.valorTotal.textContent), "R$ 1.242,50");
});
