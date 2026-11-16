from urllib.parse import urlsplit


def destino_seguro(alvo):
    """Aceita apenas caminhos internos do próprio site (ex.: "/checkout").

    Impede o "open redirect": sem esta checagem, um link como
    /login?next=https://site-falso.com levaria o usuário, já logado,
    para um site malicioso que imita a loja.
    """
    if not alvo:
        return False
    alvo = alvo.strip()
    if not alvo.startswith("/") or alvo.startswith("//") or "\\" in alvo:
        return False
    partes = urlsplit(alvo)
    return not partes.scheme and not partes.netloc


def caminho_interno_do_referer(referer, host_atual):
    """Converte o cabeçalho Referer em caminho interno, se for do próprio site."""
    if not referer:
        return None
    partes = urlsplit(referer)
    if partes.netloc != host_atual:
        return None
    caminho = partes.path + (f"?{partes.query}" if partes.query else "")
    return caminho if destino_seguro(caminho) else None
