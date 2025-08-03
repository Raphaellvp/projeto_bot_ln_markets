import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configurações de API
    LNMARKETS_KEY = os.getenv('LNMARKETS_KEY')
    LNMARKETS_SECRET = os.getenv('LNMARKETS_SECRET')
    LNMARKETS_PASSPHRASE = os.getenv('LNMARKETS_PASSPHRASE')
    TESTNET = os.getenv('TESTNET', 'false').lower() == 'true'
    
    # Parâmetros de trading
    ENTRY_AMOUNT = 1.0               # $1 por operação
    LEVERAGE = 10                    # 10x alavancagem
    PRICE_THRESHOLD = 200            # $200 variação para nova entrada
    TARGET_PROFIT = 1.0              # 1% de lucro
    MIN_BALANCE = 5.0                # Pausar abaixo de $5
    MARGIN_ADDITION = 5000           # Adicionar $5000 de margem
    LIQUIDATION_BUFFER = 1000        # Ativar proteção quando faltar $1000 para liquidação
    FEE_RATE = 0.00075               # Taxa de 0.075% por operação