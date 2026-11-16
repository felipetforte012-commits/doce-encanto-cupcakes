"""Filtros de exibição usados nos templates (camada View)."""
from datetime import timedelta, timezone

# O Brasil não usa horário de verão desde 2019: Brasília = UTC-3 fixo.
FUSO_BRASILIA = timezone(timedelta(hours=-3))


def moeda_brl(valor):
    """6.5 -> 'R$ 6,50' | 1234.5 -> 'R$ 1.234,50'"""
    if valor is None:
        valor = 0
    texto = f"{float(valor):,.2f}"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def data_br(data_utc):
    """Converte data/hora gravada em UTC para o horário de Brasília."""
    if data_utc is None:
        return ""
    return data_utc.replace(tzinfo=timezone.utc).astimezone(FUSO_BRASILIA).strftime("%d/%m/%Y %H:%M")
