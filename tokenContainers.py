import requests

def generateToken(hostname, containerName):
    tokenUrl = f'https://{hostname}/api/{containerName}/e7d80ffeefa212b7c5c55700e4f7193e/generate-token'
    
    data = {}
    response = requests.post(tokenUrl, data=data)

    if response.status_code == 201:
        print('Passando aqui')
        responseJson = response.json()
        tokenContainer = responseJson.get('token')
        print(tokenContainer)
        return tokenContainer
    else:
        print(f'Erro ao gerar token no container {containerName} no servidor {hostname}')
        return None