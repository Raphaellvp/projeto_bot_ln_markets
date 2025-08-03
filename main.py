import time
import requests  # Adicionado import faltante
from config import Config
from lnmarkets import LNMarkets
from strategies.btc_variation_strategy import BTCVariationStrategy
from utils.logger import log
from utils.risk_management import check_balance_protection

def main():
    log(f"Iniciando Bot LN Markets ({'TESTNET' if Config.TESTNET else 'MAINNET'})")
    
    ln = LNMarkets()
    strategy = BTCVariationStrategy(ln)
    
    try:
        while True:
            try:
                balance = ln.get_balance()
                current_price = ln.get_price()
                
                log(f"Saldo: ${balance:,.2f} | BTC: ${current_price:,.2f}", replace_previous=True)
                
                if not check_balance_protection(balance):
                    break
                    
                strategy.check_conditions(current_price)
                time.sleep(5)
                
            except requests.exceptions.RequestException as e:
                log(f"Erro de conexão: {str(e)}. Tentando novamente em 10s...")
                time.sleep(10)
            except Exception as e:
                log(f"Erro: {str(e)}")
                time.sleep(5)
                
    except KeyboardInterrupt:
        print()
        log("Bot interrompido pelo usuário")
    finally:
        log("Bot finalizado")

if __name__ == "__main__":
    main()