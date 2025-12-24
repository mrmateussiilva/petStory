# 🚀 Guia de Deploy - PetStory API

Guia completo para deploy em produção usando Docker e Docker Compose.

## 📋 Pré-requisitos

- VPS com Debian 12 (ou similar)
- Docker e Docker Compose instalados
- Domínio configurado (opcional, para HTTPS)
- Portas 80 e 443 abertas no firewall (se usar proxy reverso)

## 🐳 Deploy Local (Desenvolvimento)

### 1. Clonar o repositório

```bash
git clone <seu-repositorio> petstory-api
cd petstory-api
```

### 2. Configurar variáveis de ambiente

```bash
cp env.example .env
nano .env  # Edite com suas configurações
```

**Configurações mínimas necessárias:**
- `GEMINI_API_KEY` - Chave da API do Gemini (obrigatória)
- `SMTP_USER` e `SMTP_PASSWORD` - Para envio de emails
- `DATABASE_URL` - Para local: `sqlite:///./database.sqlite`

### 3. Subir os serviços

```bash
docker compose up -d
```

### 4. Verificar status

```bash
# Ver logs
docker compose logs -f api

# Verificar saúde
curl http://localhost:8000/health
```

### 5. Parar os serviços

```bash
docker compose down
```

## 🏭 Deploy em Produção (VPS)

### 1. Preparar o servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo apt install docker-compose-plugin -y

# Adicionar usuário ao grupo docker (opcional)
sudo usermod -aG docker $USER
newgrp docker
```

### 2. Clonar e configurar o projeto

```bash
# Criar diretório
mkdir -p ~/petstory-api
cd ~/petstory-api

# Clonar repositório
git clone <seu-repositorio> .

# Configurar variáveis
cp env.example .env
nano .env
```

### 3. Configurar `.env` para produção

**Configurações importantes:**

```env
# Ambiente
ENV=production
DEBUG=False

# Database (usar caminho absoluto para Docker)
DATABASE_URL=sqlite:////app/data/database.sqlite

# Diretório temporário
TEMP_DIR=/app/data/temp

# URL da API (HTTPS em produção)
API_BASE_URL=https://api.seudominio.com

# CORS - incluir domínio do frontend
CORS_ORIGINS=https://seu-usuario.github.io,https://seudominio.com
```

### 4. Criar diretórios de dados

```bash
# Criar diretórios que serão montados como volumes
mkdir -p data logs

# Garantir permissões corretas
chmod 755 data logs
```

### 5. Subir a aplicação

```bash
# Construir e iniciar
docker compose build
docker compose up -d

# Verificar status
docker compose ps
docker compose logs -f api
```

### 6. Verificar funcionamento

```bash
# Health check local
curl http://localhost:8000/health

# Se estiver usando proxy reverso (Caddy/Nginx)
curl https://api.seudominio.com/health
```

## 🔄 Comandos Úteis

### Gerenciar containers

```bash
# Ver status
docker compose ps

# Ver logs
docker compose logs -f api

# Reiniciar
docker compose restart api

# Parar
docker compose down

# Parar e remover volumes (CUIDADO: apaga dados!)
docker compose down -v
```

### Atualizar aplicação

```bash
# Fazer pull das mudanças
git pull

# Reconstruir e reiniciar
docker compose build
docker compose up -d

# Verificar logs
docker compose logs -f api
```

### Backup

```bash
# Backup do banco de dados
cp data/database.sqlite backups/database_$(date +%Y%m%d_%H%M%S).sqlite

# Backup completo dos dados
tar -czf backups/petstory_data_$(date +%Y%m%d_%H%M%S).tar.gz data/ logs/
```

## 📊 Estrutura de Dados

Os dados são persistidos nos seguintes diretórios:

```
petstory-api/
├── data/              # Dados persistentes
│   ├── database.sqlite    # Banco de dados SQLite
│   └── temp/              # Arquivos temporários
└── logs/              # Logs da aplicação
```

## 🔒 Segurança

### Firewall (UFW)

```bash
# Permitir apenas portas necessárias
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP (se usar proxy)
sudo ufw allow 443/tcp   # HTTPS (se usar proxy)
sudo ufw enable
```

### Permissões

O container roda como usuário não-root (`appuser`) por padrão, garantindo maior segurança.

## 🐛 Troubleshooting

### Container não inicia

```bash
# Ver logs detalhados
docker compose logs api

# Verificar variáveis de ambiente
docker compose exec api env | grep GEMINI
```

### Erro de permissão

```bash
# Ajustar permissões dos diretórios
sudo chown -R $USER:$USER data logs
chmod 755 data logs
```

### Banco de dados não encontrado

Verifique se o `DATABASE_URL` está correto:
- Docker: `sqlite:////app/data/database.sqlite` (4 barras)
- Local: `sqlite:///./database.sqlite` (3 barras)

### Porta já em uso

```bash
# Verificar o que está usando a porta 8000
sudo lsof -i :8000

# Ou mudar a porta no docker-compose.yml
ports:
  - "127.0.0.1:8001:8000"
```

## 📈 Monitoramento

### Health Check

A aplicação expõe um endpoint de health check:

```bash
curl http://localhost:8000/health
```

Configure um monitoramento externo (UptimeRobot, Pingdom, etc.) para verificar este endpoint.

### Logs

Os logs são salvos em:
- Container: `/app/logs/`
- Host: `./logs/`

Para ver logs em tempo real:

```bash
docker compose logs -f api
```

## 🔄 CI/CD (Preparação)

O projeto está preparado para CI/CD. Para implementar:

### Nome da imagem
```
petstory-api:latest
```

### Comandos de build
```bash
docker compose build
```

### Comandos de deploy
```bash
docker compose up -d
```

### Variáveis necessárias no CI/CD
- Todas as variáveis do `.env` devem ser configuradas como secrets no GitHub Actions (ou similar)

## 📝 Notas Importantes

1. **Persistência**: Os dados são salvos em `./data` e `./logs` no host
2. **Backup**: Faça backup regular de `data/database.sqlite`
3. **Atualizações**: Sempre teste em desenvolvimento antes de fazer deploy
4. **Logs**: Monitore os logs regularmente para detectar problemas
5. **Segurança**: Nunca commite o arquivo `.env`

## 🆘 Suporte

Em caso de problemas:
1. Verifique os logs: `docker compose logs -f api`
2. Verifique o health check: `curl http://localhost:8000/health`
3. Verifique as variáveis de ambiente no `.env`
4. Consulte a documentação completa em `DEPLOY.md`

