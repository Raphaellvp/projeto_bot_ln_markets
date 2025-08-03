import requests
import hmac
import hashlib
import time
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def test_autenticacao_api():
    """
    Testa a autenticação com a API da LN Markets (testnet)
    """
    # Obtém as credenciais do arquivo .env
    chave_api = os.getenv('LNMARKETS_KEY')
    segredo_api = os.getenv('LNMARKETS_SECRET')
    passphrase = os.getenv('LNMARKETS_PASSPHRASE')
    
    # Configuração do endpoint
    endpoint = "/user"
    url_base = "https://api.testnet4.lnmarkets.com/v2"
    url_completa = f"{url_base}{endpoint}"
    
    # Gera a assinatura necessária para autenticação
    timestamp = str(int(time.time() * 1000))
    mensagem = timestamp + "GET" + endpoint
    assinatura = hmac.new(
        segredo_api.encode('utf-8'),
        mensagem.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # Cabeçalhos da requisição
    headers = {
        "LNM-ACCESS-KEY": chave_api,
        "LNM-ACCESS-SIGNATURE": assinatura,
        "LNM-ACCESS-TIMESTAMP": timestamp,
        "LNM-ACCESS-PASSPHRASE": passphrase,
        "Accept": "application/json"
    }
    
    # Faz a requisição
    try:
        resposta = requests.get(url_completa, headers=headers)
        print("\nResultado do Teste de Autenticação:")
        print(f"Status Code: {resposta.status_code}")
        print(f"Resposta: {resposta.text}")
        
        if resposta.status_code == 200:
            saldo = resposta.json().get('balance', {}).get('available', 'N/A')
            print(f"\n✅ Autenticação bem-sucedida! Saldo disponível: {saldo} USD")
        else:
            print("\n❌ Falha na autenticação. Verifique suas credenciais.")
            
    except Exception as erro:
        print(f"\n⚠️ Erro durante o teste: {str(erro)}")

if __name__ == "__main__":
    print("Iniciando teste de autenticação com a API LN Markets...")
    test_autenticacao_api()