import os

from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Carrega variáveis do arquivo .env (se existir). O .env fica só no computador
# local e NUNCA vai para o GitHub (está no .gitignore). Variáveis já definidas
# no sistema (ex.: no painel do Render) têm prioridade sobre o .env.
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Certificado público (ISRG Root X1) usado para validar o TLS do TiDB Cloud.
# Pode ser sobrescrito pela variável DB_SSL_CA.
CA_PADRAO = os.path.join(BASE_DIR, "certs", "isrgrootx1.pem")

# O Render define automaticamente RENDER=true nos serviços dele.
EM_PRODUCAO = os.environ.get("RENDER", "").lower() == "true" or os.environ.get("APP_ENV") == "producao"


def normalizar_database_url(url):
    """Garante que URLs MySQL usem o driver PyMySQL (o único instalado)."""
    if not url:
        return url
    if url.startswith("mysql://"):
        return "mysql+pymysql://" + url[len("mysql://"):]
    return url


def montar_engine_options(url, caminho_ca=None):
    """Opções do SQLAlchemy conforme o banco usado.

    - SQLite (desenvolvimento/testes): nenhuma opção especial.
    - MySQL/TiDB: conexão TLS validando o certificado e reciclagem de conexões,
      pois o TiDB Cloud encerra conexões ociosas ("MySQL server has gone away").
    """
    if not url or not url.startswith("mysql"):
        return {}

    caminho_ca = caminho_ca or os.environ.get("DB_SSL_CA") or CA_PADRAO
    if not os.path.isfile(caminho_ca):
        raise RuntimeError(
            f"Certificado CA não encontrado em '{caminho_ca}'. "
            "Confira se o arquivo certs/isrgrootx1.pem existe ou defina DB_SSL_CA."
        )

    return {
        "connect_args": {"ssl": {"ca": caminho_ca}},
        "pool_pre_ping": True,
        "pool_recycle": 280,
    }


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or (
        None if EM_PRODUCAO else "chave-secreta-dev-somente-local"
    )

    SQLALCHEMY_DATABASE_URI = normalizar_database_url(os.environ.get("DATABASE_URL")) or (
        f"sqlite:///{os.path.join(BASE_DIR, 'cupcakes.db')}"
    )
    SQLALCHEMY_ENGINE_OPTIONS = montar_engine_options(SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cookies de sessão mais seguros (HTTPS obrigatório em produção).
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = EM_PRODUCAO
