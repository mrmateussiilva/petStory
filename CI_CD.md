# 🚀 CI/CD - PetStory API

Documentação para implementação de CI/CD com GitHub Actions.

## 📦 Informações da Imagem

### Nome da Imagem
```
petstory-api:latest
```

### Build Local
```bash
docker compose build
```

### Build Manual
```bash
docker build -t petstory-api:latest .
```

## 🔧 Comandos de Build e Deploy

### Build
```bash
docker compose build
# ou
docker build -t petstory-api:latest .
```

### Deploy
```bash
docker compose up -d
```

### Verificação
```bash
docker compose ps
docker compose logs -f api
curl http://localhost:8000/health
```

## 🔐 Variáveis de Ambiente Necessárias

Todas as variáveis do `.env` devem ser configuradas como secrets no GitHub Actions:

### Obrigatórias
- `GEMINI_API_KEY`
- `SMTP_USER`
- `SMTP_PASSWORD`
- `EMAIL_FROM`
- `EMAIL_FROM_NAME`

### Opcionais (mas recomendadas)
- `MERCADOPAGO_ACCESS_TOKEN`
- `MERCADOPAGO_PUBLIC_KEY`
- `MERCADOPAGO_WEBHOOK_SECRET`

### Configuração da Aplicação
- `ENV=production`
- `DEBUG=False`
- `API_BASE_URL`
- `DATABASE_URL=sqlite:////app/data/database.sqlite`
- `TEMP_DIR=/app/data/temp`
- `CORS_ORIGINS`

## 📝 Exemplo de Workflow (GitHub Actions)

Crie `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build image
        run: docker compose build

      - name: Deploy to server
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.SSH_HOST }}
          username: ${{ secrets.SSH_USER }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd ~/petstory-api
            git pull
            docker compose build
            docker compose up -d
            docker compose logs -f api
```

## 🔑 Secrets Necessários no GitHub

Configure os seguintes secrets no GitHub (Settings > Secrets and variables > Actions):

### SSH (para deploy)
- `SSH_HOST` - IP ou domínio da VPS
- `SSH_USER` - Usuário SSH
- `SSH_KEY` - Chave privada SSH

### Variáveis de Ambiente
Adicione todas as variáveis do `.env` como secrets.

## 🎯 Próximos Passos

1. Configure os secrets no GitHub
2. Crie o workflow em `.github/workflows/deploy.yml`
3. Teste o workflow em uma branch de teste
4. Configure webhook ou push automático para produção

## ⚠️ Notas Importantes

- Nunca commite o arquivo `.env`
- Use secrets para todas as informações sensíveis
- Teste o workflow em staging antes de usar em produção
- Configure rollback automático em caso de falha

