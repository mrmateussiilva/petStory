# 🧪 Guia de Teste - Mercado Pago

## ✅ O que já está funcionando:

1. **Endpoint de Pricing** - ✅ Funcionando
   ```bash
   curl http://localhost:8000/api/pricing
   ```
   Retorna: preços, desconto e nome da promoção

## 🔍 Verificações Necessárias:

### 1. Verificar se o PaymentService foi inicializado

**O que fazer:**
- Olhe os logs do servidor quando ele iniciou
- Deve aparecer: `"Payment service initialized successfully"`
- Se aparecer erro, o token pode estar inválido

### 2. Testar criação de pagamento

```bash
curl -X POST http://localhost:8000/api/payment/create \
  -F "email=teste@exemplo.com" \
  -F "pet_name=TestePet"
```

**Resposta esperada (sucesso):**
```json
{
  "status": "success",
  "checkout_url": "https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=...",
  "preference_id": "1234567890"
}
```

**Resposta de erro:**
```json
{
  "detail": "Erro ao criar pagamento: ..."
}
```

### 3. Possíveis problemas e soluções:

#### ❌ Erro: "Payment service not configured"
- **Causa:** Token não configurado ou vazio
- **Solução:** Verifique se `MERCADOPAGO_ACCESS_TOKEN` está no `.env`

#### ❌ Erro: "Failed to create payment preference"
- **Causa 1:** Token inválido ou expirado
  - **Solução:** Gere um novo token no Mercado Pago Developers
  
- **Causa 2:** Token de teste não está funcionando
  - **Solução:** Verifique se o token começa com `TEST-` para sandbox
  
- **Causa 3:** Problema de conexão
  - **Solução:** Verifique sua conexão com a internet

#### ❌ Erro: "Unknown error"
- **Causa:** Resposta do Mercado Pago não está no formato esperado
- **Solução:** Verifique os logs do servidor para mais detalhes

### 4. Verificar logs detalhados

O código foi atualizado para mostrar mais detalhes nos logs. Verifique:
- Logs do servidor (terminal onde está rodando)
- Mensagens de erro detalhadas
- Resposta completa do Mercado Pago

### 5. Testar com cartão de teste (Sandbox)

Se estiver usando token de teste (`TEST-...`):

1. Use a URL retornada em `checkout_url` ou `sandbox_init_point`
2. Cartão de teste aprovado:
   - Número: `5031 4332 1540 6351`
   - CVV: `123`
   - Vencimento: `11/25`
   - Nome: Qualquer nome

## 📝 Checklist de Teste:

- [ ] Servidor está rodando
- [ ] Endpoint `/api/pricing` funciona
- [ ] PaymentService foi inicializado (ver logs)
- [ ] Token está configurado no `.env`
- [ ] Token começa com `TEST-` (para sandbox)
- [ ] Teste de criação de pagamento funciona
- [ ] Checkout URL é retornada corretamente
- [ ] É possível acessar a URL do checkout

## 🚀 Próximos Passos:

1. Se tudo funcionar, teste o fluxo completo:
   - Criar pagamento
   - Redirecionar para checkout
   - Fazer pagamento de teste
   - Verificar webhook
   - Fazer upload de fotos

2. Para produção:
   - Use token de produção (sem `TEST-`)
   - Configure webhook no painel do Mercado Pago
   - Atualize `API_BASE_URL` para URL de produção

