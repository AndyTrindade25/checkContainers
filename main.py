import paramiko
import requests
import json
import psycopg2

# Variável global para o comando Docker
docker_command = 'docker ps --format "{{.Names}}" | grep -v -e "portainer_agent"'

# Função para verificar e registrar informações dos contêineres em um servidor
def verificar_servidor(server, ssh_host, ssh_username, ssh_password):
    # Configurações de conexão SSH para o servidor específico
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    containers_info = []
    
    try:
        ssh_client.connect(ssh_host, port=ssh_port, username=ssh_username, password=ssh_password)

        # Executa o comando Docker para obter a lista de nomes de containers
        stdin, stdout, stderr = ssh_client.exec_command(docker_command)

        # Obtém a saída do comando como uma lista de nomes de containers
        docker_names = stdout.read().decode().strip().split('\n')

        # Loop através da lista de nomes de containers
        for docker_name in docker_names:
            # Construa a URL da requisição POST para obter o token (substitua pelo URL apropriado)
            token_url = f'https://{server}.hiperchat.com.br/api/{docker_name}/e7d80ffeefa212b7c5c55700e4f7193e/generate-token'

            # Dados a serem enviados no corpo da requisição POST (se necessário)
            data = {}  # Preencha com os dados apropriados

            # Realiza a requisição POST para obter o token
            response = requests.post(token_url, data=data)

            # Inicializa um dicionário para armazenar informações do contêiner
            container_info = {'Nome do Servidor': server, 'Nome do Container': docker_name}

            # Verifica o código de status da resposta
            if response.status_code == 201:
                # A requisição foi bem-sucedida e um novo recurso foi criado
                container_info['Status da Requisição'] = 'Requisição bem-sucedida'
                response_json = response.json()
                token = response_json.get('token')

                if token:
                    container_info['Token'] = token

                    get_url = f'https://{server}.hiperchat.com.br/api/{docker_name}/check-connection-session'

                    # Define o cabeçalho de autorização Bearer
                    headers = {'Authorization': f'Bearer {token}'}

                    # Realiza a requisição GET para verificar a conexão
                    response_get = requests.get(get_url, headers=headers)

                    # Verifica o código de status da resposta da segunda requisição
                    if response_get.status_code == 200:
                        # Acessa o corpo da resposta da segunda requisição como JSON
                        response_json_get = response_get.json()
                        # Extrai o valor do campo 'message'
                        message = response_json_get.get('message')
                        if message:
                            container_info['Mensagem'] = message
                        else:
                            container_info['Mensagem'] = 'Campo "message" não encontrado na resposta'
                    else:
                        container_info['Status da Conexão'] = f'Servidor {docker_name} não está conectado'
                else:
                    container_info['Token'] = 'Token não encontrado no corpo da resposta'
            else:
                container_info['Status da Requisição'] = f'Requisição falhou com o código de status {response.status_code}'

            # Adiciona as informações do contêiner à lista
            containers_info.append(container_info)

    except Exception as e:
        print(f"Erro ao conectar ao servidor SSH {server}: {str(e)}")
    finally:
        ssh_client.close()

    # Conexão com o banco de dados PostgreSQL
    db_connection = psycopg2.connect(
        database="checkcontainers",
        user="anderson123",
        password="anderson123",
        host="localhost",
        port="5432"

        #179.127.18.85
    )

    cursor = db_connection.cursor()

    # Inserir ou atualizar informações dos contêineres no banco de dados
    for container_info in containers_info:
        nome_servidor = container_info.get('Nome do Servidor', '')
        nome_container = container_info.get('Nome do Container', '')
        status_requisicao = container_info.get('Status da Requisição', '')
        token = container_info.get('Token', '')
        mensagem = container_info.get('Mensagem', '')

        # Verifica se o registro já existe na tabela com base em nome_container
        cursor.execute("SELECT * FROM tabela_containers WHERE nome_container = %s", (nome_container,))
        existing_record = cursor.fetchone()

        if existing_record:
            # Se o registro existe, atualize-o
            sql = "UPDATE tabela_containers SET status_requisicao = %s, token = %s, mensagem = %s WHERE nome_container = %s"
            cursor.execute(sql, (status_requisicao, token, mensagem, nome_container))
        else:
            # Se o registro não existe, insira um novo
            sql = "INSERT INTO tabela_containers (nome_servidor, nome_container, status_requisicao, token, mensagem) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (nome_servidor, nome_container, status_requisicao, token, mensagem))

    db_connection.commit()
    print("As informações dos contêineres foram inseridas ou atualizadas no banco de dados.")

    # Fecha a conexão com o banco de dados
    db_connection.close()

# Configurações de conexão SSH para o servidor Poseidon
server_poseidon = 'poseidon'
ssh_host_poseidon = f'poseidon.hiperchat.com.br'
ssh_port = 22
ssh_username = 'root'
ssh_password = '0pt@fr4nch151ng!'

# Configurações de conexão SSH para o servidor Hermes
server_hermes = 'hermes'
ssh_host_hermes = 'hermes.hiperchat.com.br'
ssh_username_hermes = 'root'
ssh_password_hermes = '0pt@fr4nch151ng!'

# Configurações de conexão SSH para o servidor Hefesto
server_hefesto = 'hefesto'
ssh_host_hefesto = 'hefesto.hiperchat.com.br'
ssh_username_hefesto = 'root'
ssh_password_hefesto = '0pt@fr4nch151ng!'

# Configurações de conexão SSH para o servidor Atena
server_atena = 'atena'
ssh_host_atena = 'atena.hiperchat.com.br'
ssh_username_atena = 'root'
ssh_password_atena = '0pt@fr4nch151ng!'

# Configurações de conexão SSH para o servidor Ares
server_ares = 'ares'
ssh_host_ares = 'ares.hiperchat.com.br'
ssh_username_ares = 'root'
ssh_password_ares = '0pt@fr4nch151ng!'

# Configurações de conexão SSH para o servidor Dionisio
server_dionisio = 'dionisio'
ssh_host_dionisio = 'dionisio.hiperchat.com.br'
ssh_username_dionisio = 'root'
ssh_password_dionisio = '0pt@fr4nch151ng!'

# Configurações de conexão SSH para o servidor Dionisio
server_artemis = 'artemis'
ssh_host_artemis = 'artemis.hiperchat.com.br'
ssh_username_artemis = 'root'
ssh_password_artemis = '0pt@fr4nch151ng!'

# Verificar o servidor Poseidon
verificar_servidor(server_poseidon, ssh_host_poseidon, ssh_username, ssh_password)

# Verificar o servidor Hermes
verificar_servidor(server_hermes, ssh_host_hermes, ssh_username_hermes, ssh_password_hermes)

# Verificar o servidor Hefesto
verificar_servidor(server_hefesto, ssh_host_hefesto, ssh_username_hefesto, ssh_password_hefesto)

# Verificar o servidor Atena
verificar_servidor(server_atena, ssh_host_atena, ssh_username_atena, ssh_password_atena)

# Verificar o servidor Ares
verificar_servidor(server_ares, ssh_host_ares, ssh_username_ares, ssh_password_ares)

# Verificar o servidor Dionisio
verificar_servidor(server_dionisio, ssh_host_dionisio, ssh_username_dionisio, ssh_password_dionisio)

# Verificar o servidor Artemis
verificar_servidor(server_artemis, ssh_host_artemis, ssh_username_artemis, ssh_password_artemis)
