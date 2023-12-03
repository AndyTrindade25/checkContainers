import paramiko
import psycopg2
import os

def execute_insert(host, ssh_username, ssh_password, db_username, db_password):
    ssh_port = 22

    # Conexão SSH para listar os nomes dos contêineres
    with paramiko.SSHClient() as ssh_client:
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(host, ssh_port, ssh_username, ssh_password)

        docker_command = 'docker ps --format "{{.Names}}" | grep -v -e "portainer_agent"'
        stdin, stdout, stderr = ssh_client.exec_command(docker_command)
        output = stdout.read().decode('utf-8')

    # Conexão ao banco de dados PostgreSQL
    with psycopg2.connect(
        host=db_host,
        user=db_username, 
        password=db_password,
        database=db_name
    ) as db_connection:
        cursor = db_connection.cursor()

        # Inserir os valores dos contêineres no banco de dados
        insert_query = "INSERT INTO tabela_containers (nome_container, nome_servidor) VALUES (%s, %s)"
        for container_name in output.split('\n'):
            if container_name:  # Certifique-se de que a linha não está vazia
                cursor.execute(insert_query, (container_name, host))

        db_connection.commit()

# Lista de hosts
hosts = [
    'artemis.hiperchat.com.br',
    'ares.hiperchat.com.br',
    'atena.hiperchat.com.br',
    'afrodite.hiperchat.com.br'
]

# Credenciais
ssh_username = 'root'
ssh_password = '0pt@fr4nch151ng!'
db_host = 'localhost'
db_username = 'anderson123'
db_password = 'anderson123'
db_name = 'checkcontainers'

# Iterar através da lista de hosts e inserir dados no banco de dados
for host in hosts:
    execute_insert(host, ssh_username, ssh_password, db_username, db_password)
