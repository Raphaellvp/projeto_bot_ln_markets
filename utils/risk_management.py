from config import Config
from utils.logger import log

def calculate_adjusted_target(entry_price, target_profit, amount):
    """Calcula preço alvo ajustado para taxas"""
    fees = amount * Config.FEE_RATE
    gross_target = entry_price * (1 + target_profit/100)
    adjusted_target = gross_target + (fees / amount)
    return round(adjusted_target, 2)

def check_balance_protection(balance):
    if balance <= Config.MIN_BALANCE:
        log(f"ALERTA: Saldo abaixo de ${Config.MIN_BALANCE}. Operações pausadas!")
        return False
    return True