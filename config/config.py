import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configuração com suas chaves de teste
    LNMARKETS_KEY = "U+eEBdZWF+wEfoNa7kIrjAL+fRSnfqcUOCANWXoKyTY="
    LNMARKETS_SECRET = "rymubEBdpjWffRI4usS/PeezZOFlq+O7kqBQnIURZg2TwMnZ7aRj5BlSG+5/S6xtltAXOPz5Oj71BmusxfLi7g=="
    LNMARKETS_PASSPHRASE = "Raphajo@02"
    TESTNET = True
    
    @classmethod
    def validate(cls):
        print("\n🔐 Validando credenciais:")
        print(f"Key: {cls.LNMARKETS_KEY[:5]}...{cls.LNMARKETS_KEY[-5:]}")
        print(f"Secret: {'*****' if cls.LNMARKETS_SECRET else 'NÃO CONFIGURADO'}")
        print(f"Passphrase: {'*****' if cls.LNMARKETS_PASSPHRASE else 'NÃO CONFIGURADO'}")
        if not all([cls.LNMARKETS_KEY, cls.LNMARKETS_SECRET, cls.LNMARKETS_PASSPHRASE]):
            raise ValueError("Credenciais incompletas!")import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configuração direta com suas chaves (removi o .env para testes)
    LNMARKETS_KEY = "U+eEBdZWF+wEfoNa7kIrjAL+fRSnfqcUOCANWXoKyTY="
    LNMARKETS_SECRET = "rymubEBdpjWffRI4usS/PeezZOFlq+O7kqBQnIURZg2TwMnZ7aRj5BlSG+5/S6xtltAXOPz5Oj71BmusxfLi7g=="
    LNMARKETS_PASSPHRASE = "Raphajo@02"
    TESTNET = True
    
    @classmethod
    def validate(cls):
        if not all([cls.LNMARKETS_KEY, cls.LNMARKETS_SECRET, cls.LNMARKETS_PASSPHRASE]):
            raise ValueError("Credenciais incompletas!")
        print("✔ Credenciais validadas com sucesso")