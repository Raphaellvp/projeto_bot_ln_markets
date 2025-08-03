import requests
import hmac
import hashlib
import time
import json
from config.config import Config

class LNMarkets:
    def __init__(self):
        self.base_url = "https://api.testnet4.lnmarkets.com/v2"
        self.session = requests.Session()
        Config.validate()
        
    def _generate_signature(self, method, endpoint, body=''):
        timestamp = str(int(time.time() * 1000))
        message = timestamp + method.upper() + endpoint + body
        signature = hmac.new(
            Config.LNMARKETS_SECRET.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return timestamp, signature

    def _request(self, method, endpoint, data=None):
        try:
            body = json.dumps(data) if data else ''
            timestamp, signature = self._generate_signature(method, endpoint, body)
            
            headers = {
                "LNM-ACCESS-KEY": Config.LNMARKETS_KEY,
                "LNM-ACCESS-SIGNATURE": signature,
                "LNM-ACCESS-TIMESTAMP": timestamp,
                "LNM-ACCESS-PASSPHRASE": Config.LNMARKETS_PASSPHRASE,
                "Content-Type": "application/json"
            }
            
            print(f"\n🔧 Requisição para {method} {endpoint}")
            print(f"Timestamp: {timestamp}")
            print(f"Signature: {signature[:10]}...")
            
            response = self.session.request(
                method,
                f"{self.base_url}{endpoint}",
                json=data,
                headers=headers
            )
            
            print(f"Resposta: {response.status_code} {response.text[:100]}...")
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            print(f"\n❌ Erro HTTP {e.response.status_code}: {e.response.text}")
            raise
        except Exception as e:
            print(f"\n⚠️ Erro inesperado: {str(e)}")
            raise

    def get_account(self):
        """Obtém informações da conta"""
        return self._request("GET", "/account")

    def get_balance(self):
        """Obtém saldo do futures"""
        account = self.get_account()
        account_id = account['id']
        balance = self._request("GET", f"/futures/{account_id}/balance")
        return float(balance['available'])

    def get_price(self):
        """Obtém preço de mercado"""
        return self._request("GET", "/market/price")['last']