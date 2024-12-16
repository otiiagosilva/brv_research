import requests

# Substitua por suas chaves API e segredo
api_key = "YOUR_API_KEY"
api_secret = "YOUR_API_SECRET"

# Endpoint para obter todos os produtos
url = "https://api.pro.coinbase.com/products"

# Headers da requisição
headers = {
    'Content-Type': 'application/json',
    'CB-ACCESS-KEY': api_key,
    'CB-ACCESS-SIGN': 'YOUR_SIGNATURE',  # Assinatura da requisição
    'CB-ACCESS-TIMESTAMP': str(int(time.time()))  # Timestamp da requisição
}

# Realizar a requisição
response = requests.get(url, headers=headers)

# Verificar se a requisição foi bem-sucedida
if response.status_code == 200:
    data = response.json()
    for product in data:
        print(product['id'], product['price'])
else:
    print("Erro ao obter os dados:", response.text)
