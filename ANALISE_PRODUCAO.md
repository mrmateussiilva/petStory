# 🔍 Análise: O que falta para colocar a API no ar

## ✅ O que já está pronto

1. **Estrutura da aplicação**
   - FastAPI configurada com endpoints principais
   - Serviços organizados (PDF, Email, Payment, Gemini)
   - Worker para processamento em background
   - Dockerfile funcional

2. **Funcionalidades implementadas**
   - Upload de fotos
   - Geração de arte com IA (Gemini)
   - Geração de PDF
   - Integração com Mercado Pago
   - Envio de emails via SMTP

## ❌ CRÍTICO - O que falta para produção

### 1. **Arquivo .env.example e Documentação de Variáveis**

**Status:** ❌ FALTANDO

**O que fazer:**
- Criar arquivo `.env.example` com todas as variáveis necessárias
- Documentar cada variável e como obtê-las

**Variáveis obrigatórias:**
```env
# API Keys (Obrigatórias)
GEMINI_API_KEY=sua_chave_gemini_aqui

# Email Configuration (Obrigatórias para produção)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=senha_de_app_ou_email
EMAIL_FROM=noreply@petstory.com
EMAIL_FROM_NAME=PetStory

# Mercado Pago (Obrigatórias se usar pagamentos)
MERCADOPAGO_ACCESS_TOKEN=seu_access_token
MERCADOPAGO_PUBLIC_KEY=seu_public_key
MERCADOPAGO_PRODUCT_PRICE=47.0

# Application (Obrigatórias)
API_BASE_URL=https://api.seudominio.com  # URL da API em produção
DEBUG=False
APP_NAME=PetStory API

# CORS (Obrigatórias)
CORS_ORIGINS=https://seu-frontend.com,https://www.seudominio.com

# Optional
MERCADOPAGO_WEBHOOK_SECRET=opcional
TEMP_DIR=temp
WORKER_SLEEP_SECONDS=2.0
```

---

### 2. **Banco de Dados para Persistência**

**Status:** ❌ CRÍTICO - Usando armazenamento em memória

**Problema atual:**
- `payment_storage.py` usa dicionário em memória
- Dados são perdidos quando o servidor reinicia
- Não há persistência de pedidos, usuários, etc.

**Solução necessária:**
- Implementar banco de dados (PostgreSQL recomendado)
- Criar modelos de dados (SQLAlchemy ou similar)
- Migrações de banco (Alembic)
- Tabelas necessárias:
  - `payments` - Status de pagamentos
  - `orders` - Pedidos de processamento
  - `users` - Usuários/clientes (opcional, mas recomendado)

**Alternativa rápida (MVP):**
- SQLite para começar (pode migrar depois)
- Adicionar dependências: `sqlalchemy`, `alembic`

---

### 3. **Gerenciamento de Arquivos Temporários**

**Status:** ⚠️ PARCIAL - Precisa melhorias

**Problemas:**
- Arquivos salvos em `temp/` podem acumular indefinidamente
- Não há limpeza automática
- Pode encher o disco do servidor

**Solução necessária:**
- Job de limpeza periódica de arquivos antigos (ex: mais de 7 dias)
- Limpeza após envio do email
- Monitoramento de espaço em disco
- Considerar storage externo (S3, etc.) para produção

---

### 4. **Configuração de Servidor Web (Reverse Proxy)**

**Status:** ❌ FALTANDO

**Necessário:**
- Nginx ou similar como reverse proxy
- Configuração SSL/HTTPS (Let's Encrypt)
- Rate limiting
- Compressão gzip
- Configuração de headers de segurança

**Exemplo de configuração Nginx:**
```nginx
server {
    listen 80;
    server_name api.seudominio.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.seudominio.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts para uploads grandes
        client_max_body_size 100M;
        proxy_read_timeout 300s;
    }
}
```

---

### 5. **Process Manager / Supervisor**

**Status:** ❌ FALTANDO

**Problema:**
- Aplicação precisa rodar em background
- Precisa reiniciar automaticamente em caso de crash
- Gerenciar logs

**Solução:**
- **Systemd** (Linux) - Recomendado para VPS/servidor dedicado
- **PM2** ou **supervisord** - Alternativas
- **Docker Compose** - Se usar containers

**Exemplo systemd service (`/etc/systemd/system/petstory-api.service`):**
```ini
[Unit]
Description=PetStory API
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/petstory-api
Environment="PATH=/var/www/petstory-api/.venv/bin"
ExecStart=/var/www/petstory-api/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

### 6. **Monitoramento e Logs**

**Status:** ⚠️ PARCIAL - Só logging básico

**Falta:**
- Agregação de logs (Sentry, Loggly, etc.)
- Monitoramento de saúde da API (health checks externos)
- Alertas para erros críticos
- Métricas de performance
- Dashboard de monitoramento

**Sugestões:**
- Integrar Sentry para tracking de erros
- Uptime monitoring (UptimeRobot, Pingdom)
- Logs estruturados (JSON)
- Métricas com Prometheus (opcional)

---

### 7. **Backup e Recuperação**

**Status:** ❌ FALTANDO

**Necessário:**
- Backup automático do banco de dados (se usar)
- Backup de arquivos temporários importantes
- Estratégia de recuperação de desastres
- Documentação do processo de restore

---

### 8. **Segurança**

**Status:** ⚠️ PARCIAL

**Melhorias necessárias:**

1. **Rate Limiting**
   - Limitar requisições por IP
   - Prevenir abuse de API
   - Biblioteca: `slowapi` ou middleware customizado

2. **Validação de Webhooks**
   - Validar assinatura dos webhooks do Mercado Pago
   - Prevenir chamadas falsas

3. **HTTPS obrigatório**
   - Redirecionar HTTP para HTTPS
   - Headers de segurança (HSTS, CSP)

4. **Sanitização de inputs**
   - Validação mais rigorosa de uploads
   - Proteção contra path traversal

5. **Secrets Management**
   - Não commitar `.env` no git
   - Usar gerenciador de secrets (secrets do provider, etc.)

---

### 9. **Testes em Produção**

**Status:** ❌ FALTANDO

**Necessário:**
- Ambiente de staging/teste
- Testes de carga (load testing)
- Testes end-to-end do fluxo completo
- Testes de integração com Mercado Pago sandbox

---

### 10. **Documentação de Deploy**

**Status:** ❌ FALTANDO

**Necessário:**
- Guia passo-a-passo de deploy
- Checklist pré-deploy
- Procedimentos de rollback
- Troubleshooting comum

---

### 11. **Docker Compose para Produção**

**Status:** ❌ FALTANDO

**Atual:**
- Dockerfile existe, mas não há docker-compose.yml
- Não há configuração para volumes persistentes
- Não há configuração de rede

**Solução:**
- Criar `docker-compose.prod.yml`
- Configurar volumes para logs, temp, banco de dados
- Configurar restart policies
- Health checks

---

### 12. **CI/CD Pipeline**

**Status:** ❌ FALTANDO (Opcional mas recomendado)

**Benefícios:**
- Deploy automatizado
- Testes automáticos antes de deploy
- Rollback fácil

**Opções:**
- GitHub Actions
- GitLab CI
- CircleCI

---

## 📊 Priorização

### 🔴 URGENTE (Para MVP funcional):
1. ✅ Arquivo `.env.example`
2. ✅ Banco de dados (SQLite mínimo)
3. ✅ Process manager (systemd)
4. ✅ Reverse proxy + SSL (Nginx)
5. ✅ Limpeza de arquivos temporários

### 🟡 IMPORTANTE (Para produção estável):
6. ✅ Monitoramento básico (Sentry)
7. ✅ Rate limiting
8. ✅ Backup automático
9. ✅ Testes de carga
10. ✅ Documentação de deploy

### 🟢 DESEJÁVEL (Melhorias):
11. ✅ CI/CD
12. ✅ Métricas avançadas
13. ✅ Storage externo (S3)
14. ✅ CDN para assets

---

## 🚀 Checklist Mínimo para Deploy

- [ ] Arquivo `.env` configurado com todas as variáveis
- [ ] Banco de dados configurado e migrado
- [ ] SSL/HTTPS configurado (Let's Encrypt)
- [ ] Nginx configurado como reverse proxy
- [ ] Aplicação rodando via systemd/PM2
- [ ] Logs configurados e rotacionando
- [ ] Limpeza automática de arquivos temp configurada
- [ ] Backup automático configurado
- [ ] Rate limiting implementado
- [ ] Monitoramento básico configurado (health checks)
- [ ] Testes funcionais realizados
- [ ] Documentação de deploy criada
- [ ] Procedimentos de rollback documentados

---

## 📝 Notas Adicionais

### Sobre o Armazenamento em Memória:
O `payment_storage.py` atual **não é adequado para produção** porque:
- Dados são perdidos no restart
- Não escala entre múltiplas instâncias
- Não há histórico de transações

**Solução rápida (1-2 horas):**
- Substituir por SQLite + SQLAlchemy
- Migrar dados em memória para banco
- Adicionar limpeza periódica

### Sobre Rate Limits:
A API pode ser abusada facilmente:
- Upload de múltiplas imagens sem limite de taxa
- Chamadas ao Gemini podem ser caras
- Falta de throttling por usuário/IP

**Solução:**
- Implementar rate limiting por IP
- Limitar uploads por email/hora
- Cache de respostas onde possível

---

## 🎯 Próximos Passos Sugeridos

1. **Criar `.env.example`** (15 min)
2. **Implementar banco de dados SQLite** (2-3 horas)
3. **Configurar systemd service** (30 min)
4. **Configurar Nginx + SSL** (1-2 horas)
5. **Implementar limpeza de arquivos** (1 hora)
6. **Adicionar rate limiting** (2 horas)
7. **Configurar monitoramento básico** (1 hora)
8. **Criar documentação de deploy** (1 hora)

**Tempo estimado total: 8-11 horas de trabalho**

