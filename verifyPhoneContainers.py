import requests
import psycopg2

# Configurações do banco de dados PostgreSQL
db_config = {
    'host': 'localhost',
    'database': 'checkcontainers',
    'user': 'anderson123',
    'password': 'anderson123',
}

# Conecta ao banco de dados
conn = psycopg2.connect(**db_config)
cursor = conn.cursor()

# Consulta para obter as informações necessárias
query = "SELECT nome_servidor, nome_container, token FROM tabela_containers WHERE mensagem IS NOT NULL"
cursor.execute(query)
rows = cursor.fetchall()

# Itera sobre os resultados da consulta
for row in rows:
    nome_servidor, nome_container, token = row

    # Substitua 'sua_api' pela parte específica da URL da sua API
    base_url = f"https://{nome_servidor}/api/{nome_container}/host-device"

    # Define o cabeçalho da requisição
    headers = {
        'Authorization': f'Bearer {token}',
    }

    # Faz a requisição
    response = requests.get(base_url, headers=headers)

    # Verifica se a requisição foi bem-sucedida (código 200)
    if response.status_code == 200:
        data = response.json()
        telefone = data.get('response', {}).get('phoneNumber')

        # Atualiza o banco de dados com o número de telefone na coluna 'Phone'
        update_query = f"UPDATE tabela_containers SET Phone = '{telefone}' WHERE nome_container = '{nome_container}'"
        cursor.execute(update_query)
        conn.commit()
    else:
        print(f"Falha ao obter número de telefone para {nome_container}. Código de status: {response.status_code}")

# Fecha a conexão com o banco de dados
cursor.close()
conn.close()
