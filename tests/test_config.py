"""Testes da configuração (conexão com banco, certificado e SECRET_KEY)."""
import os

import pytest

from app import create_app
from config import CA_PADRAO, montar_engine_options, normalizar_database_url


def test_url_mysql_usa_driver_pymysql():
    assert normalizar_database_url("mysql://u:s@host:4000/db") == "mysql+pymysql://u:s@host:4000/db"
    assert normalizar_database_url("mysql+pymysql://u:s@h/db") == "mysql+pymysql://u:s@h/db"
    assert normalizar_database_url("sqlite:///x.db") == "sqlite:///x.db"
    assert normalizar_database_url(None) is None


def test_sqlite_nao_usa_ssl():
    assert montar_engine_options("sqlite:///x.db") == {}


def test_certificado_do_tidb_esta_no_projeto():
    assert os.path.isfile(CA_PADRAO), "certs/isrgrootx1.pem precisa existir para conectar ao TiDB"


def test_mysql_usa_ssl_com_certificado_e_reciclagem_de_conexao():
    opcoes = montar_engine_options("mysql+pymysql://u:s@host:4000/db")
    assert opcoes["connect_args"]["ssl"]["ca"] == CA_PADRAO
    assert opcoes["pool_pre_ping"] is True
    assert opcoes["pool_recycle"] < 300


def test_mysql_sem_certificado_falha_com_mensagem_clara(tmp_path):
    with pytest.raises(RuntimeError, match="Certificado CA não encontrado"):
        montar_engine_options("mysql+pymysql://u:s@h/db", caminho_ca=str(tmp_path / "nao_existe.pem"))


def test_app_nao_sobe_sem_secret_key():
    class SemChave:
        SECRET_KEY = None
        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        create_app(SemChave)
