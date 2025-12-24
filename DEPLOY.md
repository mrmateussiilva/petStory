# 🚀 Guia de Deploy - PetStory API

Este guia explica como fazer o deploy da API PetStory em uma VPS usando Docker e Caddy como proxy reverso.

## 📋 Pré-requisitos

- VPS com Ubuntu/Debian (ou similar)
- Docker e Docker Compose instalados
- Caddy instalado
- Domínio configurado apontando para o IP da VPS
- Portas 80 e 443 abertas no firewall

## 🔧 Instalação Inicial

### 1. Instalar Docker e Docker Compose

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

### 2. Instalar Caddy

```bash
# Adicionar repositório Caddy
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list

# Instalar Caddy
sudo apt update
sudo apt install caddy -y
```

## 📁 Preparar o Projeto na VPS

### 1. Clonar o Repositório

```bash
# Criar diretório para o projeto
mkdir -p ~/petstory-api
cd ~/petstory-api

# Clonar repositório (ou fazer upload dos arquivos)
git clone https://github.com/seu-usuario/petStoryArt.git .
# OU fazer upload via SCP/SFTP
```

### 2. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp env.example .env

# Editar com suas configurações
nano .env
```

**Configurações importantes no `.env`:**

```env
# API Keys
GEMINI_API_KEY=sua_chave_gemini_aqui

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=sua_senha_de_app

# IMPORTANTE: URL da API em produção
API_BASE_URL=https://api.seudominio.com

# CORS - incluir domínio do frontend (GitHub Pages)
CORS_ORIGINS=https://seu-usuario.github.io,https://seudominio.com

# Debug desativado em produção
DEBUG=False
```

### 3. Configurar Caddyfile

```bash
# Editar Caddyfile
nano Caddyfile
```

**Substituir `api.seudominio.com` pelo seu domínio real.**

### 4. Criar Diretórios Necessários

```bash
# Criar diretórios para volumes
mkdir -p temp logs

# Criar diretório de logs do Caddy
sudo mkdir -p /var/log/caddy
sudo chown $USER:$USER /var/log/caddy
```

## 🐳 Deploy com Docker

### 1. Construir e Iniciar Container

```bash
# Construir imagem
docker compose build

# Iniciar em background
docker compose up -d

# Ver logs
docker compose logs -f
```

### 2. Verificar Status

```bash
# Ver status dos containers
docker compose ps

# Verificar saúde da API
curl http://localhost:8000/health
```

## 🔒 Configurar Caddy

### 1. Copiar Caddyfile

```bash
# Copiar Caddyfile para diretório do Caddy
sudo cp Caddyfile /etc/caddy/Caddyfile

# Ou criar link simbólico (recomendado)
sudo ln -s ~/petstory-api/Caddyfile /etc/caddy/Caddyfile
```

### 2. Testar Configuração

```bash
# Validar configuração
sudo caddy validate --config /etc/caddy/Caddyfile
```

### 3. Iniciar Caddy

```bash
# Recarregar Caddy
sudo systemctl reload caddy

# Ver status
sudo systemctl status caddy

# Ver logs
sudo journalctl -u caddy -f
```

### 4. Verificar SSL

O Caddy automaticamente:
- Obtém certificado SSL via Let's Encrypt
- Configura HTTPS
- Renova certificados automaticamente

Aguarde alguns minutos e acesse: `https://api.seudominio.com/health`

## 🔍 Verificação e Testes

### 1. Testar Endpoints

```bash
# Health check
curl https://api.seudominio.com/health

# Testar endpoint de homenagem (substitua {id} por um ID real)
curl https://api.seudominio.com/homenagem/a1b2c3d4e5f6
```

### 2. Verificar Logs

```bash
# Logs da API
docker compose logs -f api

# Logs do Caddy
sudo tail -f /var/log/caddy/petstory-api.log
```

## 🔄 Comandos Úteis

### Gerenciar Container

```bash
# Parar
docker compose down

# Reiniciar
docker compose restart

# Ver logs
docker compose logs -f api

# Entrar no container
docker compose exec api bash
```

### Gerenciar Caddy

```bash
# Recarregar configuração
sudo systemctl reload caddy

# Reiniciar
sudo systemctl restart caddy

# Ver status
sudo systemctl status caddy
```

### Atualizar Aplicação

```bash
# Fazer pull das mudanças
git pull

# Reconstruir e reiniciar
docker compose build
docker compose up -d

# Verificar se está funcionando
docker compose logs -f api
```

## 🛠️ Manutenção

### Limpar Arquivos Temporários

```bash
# Limpar arquivos antigos (mais de 7 dias)
find ~/petstory-api/temp -type f -mtime +7 -delete
find ~/petstory-api/temp -type d -empty -delete
```

### Backup do Banco de Dados

```bash
# Backup SQLite
cp ~/petstory-api/petstory.db ~/petstory-api/backups/petstory_$(date +%Y%m%d).db
```

### Monitorar Espaço em Disco

```bash
# Ver uso de disco
df -h
du -sh ~/petstory-api/temp
```

## 🚨 Troubleshooting

### API não inicia

```bash
# Verificar logs
docker compose logs api

# Verificar variáveis de ambiente
docker compose exec api env | grep GEMINI
```

### Caddy não obtém SSL

```bash
# Verificar DNS
dig api.seudominio.com

# Verificar logs do Caddy
sudo journalctl -u caddy -n 50

# Verificar firewall
sudo ufw status
```

### Erro 502 Bad Gateway

- Verificar se a API está rodando: `docker compose ps`
- Verificar se está escutando na porta 8000: `curl http://localhost:8000/health`
- Verificar logs do Caddy: `sudo journalctl -u caddy -f`

### Problemas de CORS

- Verificar `CORS_ORIGINS` no `.env`
- Verificar headers no Caddyfile
- Verificar se o frontend está usando a URL correta

## 📊 Monitoramento

### Health Check Automático

A API tem endpoint de health check:
- `GET /health` - Retorna status da API
- `GET /` - Informações básicas

Configure um monitoramento externo (UptimeRobot, Pingdom, etc.) para:
- `https://api.seudominio.com/health`

## 🔐 Segurança

### Firewall (UFW)

```bash
# Permitir apenas portas necessárias
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

### Atualizações

```bash
# Atualizar sistema regularmente
sudo apt update && sudo apt upgrade -y

# Atualizar Docker
sudo apt update && sudo apt install docker-ce docker-ce-cli containerd.io
```

## 📝 Notas Importantes

1. **API_BASE_URL**: Deve ser HTTPS em produção para que os QR codes funcionem corretamente
2. **CORS**: Configure corretamente para permitir requisições do frontend
3. **TEMP_DIR**: Monitore o espaço em disco, os arquivos temporários podem crescer
4. **Logs**: Configure rotação de logs para não encher o disco
5. **Backup**: Faça backup regular do banco de dados

## 🎯 Próximos Passos

- [ ] Configurar monitoramento (Sentry, etc.)
- [ ] Configurar backup automático
- [ ] Configurar rotação de logs
- [ ] Configurar alertas
- [ ] Migrar para PostgreSQL (opcional, para produção)

