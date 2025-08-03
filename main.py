from lnmarkets import LNMarkets
import time

def main():
    print("\n🚀 Iniciando Teste de Conexão com LN Markets API v2")
    
    try:
        # 1. Testar conexão
        ln = LNMarkets()
        print("\n✅ Conexão estabelecida com sucesso!")
        
        # 2. Testar conta
        print("\n📋 Obtendo informações da conta...")
        account = ln.get_account()
        print(f"ID da Conta: {account['id']}")
        print(f"Username: {account.get('username', 'N/A')}")
        
        # 3. Testar saldo
        print("\n💵 Obtendo saldo disponível...")
        balance = ln.get_balance()
        print(f"Saldo disponível: ${balance:.2f}")
        
        # 4. Testar preço
        print("\n📈 Obtendo preço de mercado...")
        price = ln.get_price()
        print(f"Preço atual do BTC: ${price:.2f}")
        
    except Exception as e:
        print(f"\n❌ Falha crítica: {str(e)}")
    finally:
        print("\n🔚 Teste concluído")

if __name__ == "__main__":
    main()