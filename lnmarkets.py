import requests
import hmac
import hashlib
import time
import json
from config import Config
from utils.logger import log

class LNMarkets:
    def __init__(self):
        self.base_url = "https://api.lnmarkets.com/v2" if not Config.TESTNET else "https://api.testnet4.lnmarkets.com/v2"
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        log(f"Conectando à: {self.base_url}")

    def _generate_signature(self, method, endpoint, body=''):
        timestamp = str(int(time.time() * 1000))
        message = timestamp + method + endpoint + body
        signature = hmac.new(
            Config.LNMARKETS_SECRET.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return timestamp, signature

    def _request(self, method, endpoint, data=None):
        body = json.dumps(data) if data else ''
        timestamp, signature = self._generate_signature(method, endpoint, body)
        
        headers = {
            "LNM-ACCESS-KEY": Config.LNMARKETS_KEY,
            "LNM-ACCESS-SIGNATURE": signature,
            "LNM-ACCESS-TIMESTAMP": timestamp,
            "LNM-ACCESS-PASSPHRASE": Config.LNMARKETS_PASSPHRASE,
            "Content-Type": "application/json"
        }

        try:
            response = self.session.request(
                method,
                f"{self.base_url}{endpoint}",
                json=data,
                headers=headers
            )
            
            # Debug: Mostrar requisição completa
            log(f"Requisição para: {method} {endpoint}")
            log(f"Cabeçalhos: {headers}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_msg = f"Erro HTTP {e.response.status_code}: {e.response.text}"
            log(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            log(f"Erro na requisição: {str(e)}")
            raise

    def get_balance(self):
        return self._request("GET", "/user")['balance']['available']