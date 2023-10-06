import paramiko
from tokenContainers import generateToken

# Configurar informações de conexão SSH

port = 22
username = 'root'
password = '0pt@fr4nch151ng!'


servers = [
    {
        'hostname': 'artemis.hiperchat.com.br'
    },
    {
        'hostname': 'atena.hiperchat.com.br'
    }
]


# Comando que você deseja executar
command = 'docker ps --format "{{.Names}}" | grep -v -e "portainer_agent"'

for serverInfo in servers:

    hostname = serverInfo['hostname']

    # Inicializar uma conexão SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Conectar ao servidor SSH
        ssh.connect(hostname, port, username, password)

        # Executar o comando em um servidor SSH
        stdin, stdout, stderr = ssh.exec_command(command)

        #Listar nome dos containers
        listContainers = stdout.read().decode().strip().split('\n')

        for dockerName in listContainers:
            token = generateToken(hostname, dockerName)
            if token is not None:
                print(f'Token para {dockerName} em {hostname}: {token}')
            else:
                print(f'Falha ao gerar token para {dockerName} em {hostname}')

        print(f'Lista de nome dos containers do servidor {hostname}: {listContainers}')
        

    except paramiko.AuthenticationException:
        print(f'Falha na autenticação SSH para {hostname}')
    except paramiko.SSHException as e:
        print(f'Erro na conexão SSH para {hostname}: {str(e)}')
    except Exception as e:
        print(f'Erro ao conectar-se a {hostname}: {str(e)}')
    finally:
        # Fechar a conexão SSH
        ssh.close()
