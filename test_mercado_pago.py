#!/usr/bin/env python3
"""Script para testar a integração com Mercado Pago."""

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from app.services.payment_service import PaymentService

def test_configuration():
    """Testa a configuração do Mercado Pago."""
    print("=" * 60)
    print("🔍 TESTE DE CONFIGURAÇÃO DO MERCADO PAGO")
    print("=" * 60)
    print()
    
    # Verificar token
    token = settings.MERCADOPAGO_ACCESS_TOKEN
    if not token or token == "seu_token_aqui" or "seu_access_token_aqui" in token:
        print("❌ ERRO: MERCADOPAGO_ACCESS_TOKEN não está configurado!")
        print("   Configure o token no arquivo .env")
        return False
    
    print(f"✅ Token configurado: {token[:20]}...{token[-10:]}")
    print(f"   Tipo: {'TESTE (Sandbox)' if token.startswith('TEST-') else 'PRODUÇÃO'}")
    print()
    
    # Verificar preço
    print(f"✅ Preço configurado: R$ {settings.MERCADOPAGO_PRODUCT_PRICE}")
    print()
    
    # Verificar API Base URL
    print(f"✅ API Base URL: {settings.API_BASE_URL}")
    print()
    
    return True

def test_payment_service():
    """Testa a criação do serviço de pagamento."""
    print("=" * 60)
    print("🧪 TESTE DO SERVIÇO DE PAGAMENTO")
    print("=" * 60)
    print()
    
    try:
        service = PaymentService()
        print("✅ PaymentService inicializado com sucesso!")
        print()
        return service
    except Exception as e:
        print(f"❌ Erro ao inicializar PaymentService: {e}")
        print()
        return None

def test_create_preference(service):
    """Testa a criação de uma preferência de pagamento."""
    print("=" * 60)
    print("💳 TESTE DE CRIAÇÃO DE PREFERÊNCIA")
    print("=" * 60)
    print()
    
    try:
        result = service.create_payment_preference(
            email="teste@exemplo.com",
            pet_name="PetTeste",
            success_url=f"{settings.API_BASE_URL}/api/payment/success",
            failure_url=f"{settings.API_BASE_URL}/api/payment/failure",
            pending_url=f"{settings.API_BASE_URL}/api/payment/pending"
        )
        
        print("✅ Preferência criada com sucesso!")
        print(f"   ID: {result.get('id')}")
        checkout_url = result.get("sandbox_init_point") or result.get("init_point")
        print(f"   Checkout URL: {checkout_url}")
        print()
        print("🎉 Tudo funcionando! Você pode usar esta URL para testar o pagamento.")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar preferência: {e}")
        print()
        print("💡 Possíveis causas:")
        print("   - Token inválido ou expirado")
        print("   - Token de teste não está funcionando")
        print("   - Problema de conexão com Mercado Pago")
        print("   - Verifique os logs do servidor para mais detalhes")
        return False

def main():
    """Função principal."""
    # Testar configuração
    if not test_configuration():
        sys.exit(1)
    
    # Testar serviço
    service = test_payment_service()
    if not service:
        sys.exit(1)
    
    # Testar criação de preferência
    if not test_create_preference(service):
        sys.exit(1)
    
    print("=" * 60)
    print("✅ TODOS OS TESTES PASSARAM!")
    print("=" * 60)

if __name__ == "__main__":
    main()

