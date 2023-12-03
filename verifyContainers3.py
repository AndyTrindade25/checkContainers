import psycopg2
import requests

# Configurações do banco de dados PostgreSQL
db_config = {
    'host': 'localhost',
    'database': 'checkcontainers',
    'user': 'anderson123',
    'password': 'anderson123',
}

# Conectar ao banco de dados
conn = psycopg2.connect(**db_config)
cursor = conn.cursor()

# Consultar dados do banco de dados
cursor.execute("SELECT nome_servidor, nome_container, token FROM tabela_containers")
rows = cursor.fetchall()

# Iterar sobre os resultados da consulta
for row in rows:
    nome_servidor, nome_container, token = row

    # Construir a URL da requisição
    url = f"https://{nome_servidor}/api/{nome_container}/check-connection-session"

    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        # Enviar a requisição HTTP
        response = requests.get(url, headers=headers)

        # Verificar se a requisição foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            # Extrair a mensagem do corpo da resposta (ajuste conforme a resposta real)
            mensagem = response.json().get('message')

            # Atualizar o banco de dados com a mensagem
            update_query = f"UPDATE tabela_containers SET mensagem = '{mensagem}' WHERE nome_servidor = '{nome_servidor}' AND nome_container = '{nome_container}'"
            cursor.execute(update_query)
            conn.commit()
        else:
            print(f"Falha ao obter mensagem para {nome_servidor}. Código de status: {response.status_code}")
            print(f"Resposta da API: {response.text}")  # Adicione esta linha para imprimir a resposta da API em caso de erro
    except Exception as e:
        print(f"Erro ao processar {nome_servidor}: {e}")

# Fechar a conexão com o banco de dados
cursor.close()
conn.close()
