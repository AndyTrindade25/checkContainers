import paramiko
import psycopg2

def execute_insert(host):
    ssh_port = 22
    ssh_username = 'root'
    ssh_password = '0pt@fr4nch151ng!'

    # Conexão SSH para listar os nomes dos contêineres
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(host, ssh_port, ssh_username, ssh_password)

    docker_command = 'docker ps --format "{{.Names}}" | grep -v -e "portainer_agent"'
    stdin, stdout, stderr = ssh_client.exec_command(docker_command)
    output = stdout.read().decode('utf-8')

    # Feche a conexão SSH
    ssh_client.close()

    # Conexão ao banco de dados PostgreSQL
    db_connection = psycopg2.connect(
        host='localhost',
        user='anderson123', 
        password='anderson123',
        database='checkcontainers'
    )

    cursor = db_connection.cursor()

    # Inserir os valores dos contêineres no banco de dados
    insert_query = "INSERT INTO tabela_containers (nome_container, nome_servidor) VALUES (%s, %s)"
    for container_name in output.split('\n'):
        if container_name:  # Certifique-se de que a linha não está vazia
            cursor.execute(insert_query, (container_name, host))

    db_connection.commit()

    # Fechar a conexão com o banco de dados
    db_connection.close()

# Lista de hosts
hosts = [
    'artemis.hiperchat.com.br',
    'ares.hiperchat.com.br',
    'atena.hiperchat.com.br',
    'afrodite.hiperchat.com.br'
]

# Iterar através da lista de hosts e inserir dados no banco de dados
for host in hosts:
    execute_insert(host)
