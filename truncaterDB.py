import psycopg2
from psycopg2 import sql

def conectar_banco(conexao_string):
    try:
        # Retorna um objeto de conexão
        return psycopg2.connect(conexao_string)
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def executar_sql(conexao, query):
    try:
        # Cria um objeto de cursor para executar comandos SQL
        with conexao.cursor() as cursor:
            # Executa a instrução SQL
            cursor.execute(query)
            # Confirma a transação
            conexao.commit()
            print("Consulta executada com sucesso.")
    except psycopg2.Error as e:
        print(f"Erro ao executar a consulta SQL: {e}")

def truncar_tabela(conexao, nome_tabela):
    # Constrói a instrução SQL para truncar a tabela
    truncate_query = sql.SQL("TRUNCATE TABLE {} RESTART IDENTITY;").format(
        sql.Identifier(nome_tabela)
    )
    executar_sql(conexao, truncate_query)
    print(f"Tabela {nome_tabela} truncada com sucesso.")

def fechar_conexao(conexao):
    if conexao:
        conexao.close()

def main():
    nome_tabela = "tabela_containers"
    conexao_banco = "dbname=checkcontainers user=anderson123 password=anderson123 host=localhost"

    # Conectar ao banco de dados
    conexao = conectar_banco(conexao_banco)
    
    if not conexao:
        return

    # Truncar a tabela
    truncar_tabela(conexao, nome_tabela)

    # Fechar a conexão
    fechar_conexao(conexao)

if __name__ == "__main__":
    main()
