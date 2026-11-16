"""
Verificação SOMENTE LEITURA do banco de dados configurado.

Executa apenas consultas SELECT / inspeção de metadados: não cria, altera nem
apaga nada. Útil para conferir a conexão com o TiDB Cloud.

Uso:  python verificar_banco.py
"""
from sqlalchemy import inspect, text

from app import create_app, db

TABELAS_ESPERADAS = ["cliente", "categoria", "produto", "pedido", "item_pedido"]


def main():
    app = create_app()
    with app.app_context():
        url = db.engine.url
        print(f"Banco: {url.get_backend_name()} | host: {url.host or '(arquivo local)'} | base: {url.database}")

        with db.engine.connect() as conn:
            print("Conexão: OK")
            if url.get_backend_name() == "mysql":
                versao = conn.execute(text("SELECT VERSION()")).scalar()
                print(f"Versão do servidor: {versao}")
                try:
                    check = conn.execute(text("SELECT @@tidb_enable_check_constraint")).scalar()
                    print(f"tidb_enable_check_constraint = {check} "
                          f"({'CHECKs aplicados' if str(check) in ('1', 'ON') else 'CHECKs IGNORADOS pelo banco'})")
                except Exception:
                    print("tidb_enable_check_constraint: não disponível (servidor não é TiDB)")

            inspetor = inspect(conn)
            existentes = inspetor.get_table_names()
            print("\nTabelas:")
            for tabela in TABELAS_ESPERADAS:
                if tabela not in existentes:
                    print(f"  {tabela:<12} FALTANDO")
                    continue
                total = conn.execute(text(f"SELECT COUNT(*) FROM {tabela}")).scalar()
                checks = len(inspetor.get_check_constraints(tabela))
                print(f"  {tabela:<12} {total:>5} registros | {checks} CHECK(s) declarados")

            # Compara colunas do banco com as colunas dos models (detecta divergências).
            print("\nColunas (banco x models):")
            divergencias = 0
            for tabela_model in db.metadata.sorted_tables:
                if tabela_model.name not in existentes:
                    continue
                no_banco = {c["name"] for c in inspetor.get_columns(tabela_model.name)}
                no_model = {c.name for c in tabela_model.columns}
                if no_model - no_banco:
                    divergencias += 1
                    print(f"  {tabela_model.name}: faltam no banco -> {sorted(no_model - no_banco)}")
            if not divergencias:
                print("  OK - todas as colunas dos models existem no banco")

            if "produto" in existentes:
                negativos = conn.execute(text("SELECT COUNT(*) FROM produto WHERE estoque < 0")).scalar()
                print(f"\nProdutos com estoque negativo: {negativos}")


if __name__ == "__main__":
    main()
