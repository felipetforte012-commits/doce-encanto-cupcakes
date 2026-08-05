import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "chave-secreta-dev-troque-em-producao"
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'cupcakes.db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if os.environ.get("DATABASE_URL"):
        SQLALCHEMY_ENGINE_OPTIONS = {
            "connect_args": {
                "ssl": {
                    "ca": r"C:\Users\SAMSUNG\Desktop\tidb-ca.pem\isrgrootx1.pem"
                }
            }
        }