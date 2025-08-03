from utils.logger import log
from utils.risk_management import calculate_adjusted_target
from config import Config

class BTCVariationStrategy:
    def __init__(self, lnmarkets_client):
        self.ln = lnmarkets_client
        self.last_entry_price = None
        self.active_positions = []

    def check_conditions(self, current_price):
        log(f"Verificando condições - Preço: ${current_price:,.2f}")
        
        # Primeira entrada
        if self.last_entry_price is None:
            self._create_position(current_price, "buy")
            return
            
        # Verifica variação para nova entrada
        price_diff = abs(current_price - self.last_entry_price)
        if price_diff >= Config.PRICE_THRESHOLD:
            direction = "buy" if current_price > self.last_entry_price else "sell"
            self._create_position(current_price, direction)
            
        # Verifica posições abertas
        self._check_open_positions(current_price)

    def _create_position(self, entry_price, direction):
        try:
            log(f"Criando posição {direction.upper()} em ${entry_price:,.2f}")
            
            target_price = calculate_adjusted_target(
                entry_price, 
                Config.TARGET_PROFIT, 
                Config.ENTRY_AMOUNT
            )
            
            response = self.ln.create_position(
                amount=Config.ENTRY_AMOUNT,
                leverage=Config.LEVERAGE,
                direction=direction
            )
            
            position = {
                'id': response['id'],
                'entry': entry_price,
                'target': target_price,
                'direction': direction,
                'amount': Config.ENTRY_AMOUNT,
                'leverage': Config.LEVERAGE
            }
            
            self.active_positions.append(position)
            self.last_entry_price = entry_price
            
            log(f"Posição criada - ID: {position['id']} | Alvo: ${target_price:,.2f}")
            
        except Exception as e:
            log(f"Erro ao criar posição: {str(e)}")

    def _check_open_positions(self, current_price):
        for position in self.active_positions[:]:
            try:
                # Verifica se atingiu o alvo
                if ((position['direction'] == 'buy' and current_price >= position['target']) or
                    (position['direction'] == 'sell' and current_price <= position['target'])):
                    self.ln.close_position(position['id'])
                    self.active_positions.remove(position)
                    log(f"Posição {position['id']} fechada com lucro")
                
                # Verifica necessidade de margem adicional
                self._check_margin_requirement(position, current_price)
                
            except Exception as e:
                log(f"Erro ao verificar posição {position['id']}: {str(e)}")

    def _check_margin_requirement(self, position, current_price):
        entry = position['entry']
        price_diff = abs(entry - current_price)
        liquidation_diff = price_diff * position['leverage']
        
        if liquidation_diff >= Config.LIQUIDATION_BUFFER:
            log(f"Adicionando margem à posição {position['id']}")
            self.ln.add_margin(position['id'], Config.MARGIN_ADDITION)