# 🔧 Configuração do GitHub Actions para Deploy Automático

Este guia explica como configurar o deploy automático via GitHub Actions.

## 📋 Pré-requisitos

1. VPS com Debian 12 (ou similar) configurada
2. Docker e Docker Compose instalados na VPS
3. Acesso SSH à VPS
4. Repositório GitHub configurado

## 🔑 Configurar Secrets no GitHub

### 1. Acesse as configurações do repositório

1. Vá para: **Settings** > **Secrets and variables** > **Actions**
2. Clique em **New repository secret**

### 2. Adicione os seguintes secrets:

#### SSH_HOST
- **Nome:** `SSH_HOST`
- **Valor:** IP ou domínio da sua VPS
- **Exemplo:** `123.456.789.0` ou `api.seudominio.com`

#### SSH_USER
- **Nome:** `SSH_USER`
- **Valor:** Usuário SSH da VPS
- **Exemplo:** `root` ou `debian`

#### SSH_KEY
- **Nome:** `SSH_KEY`
- **Valor:** Chave privada SSH completa

### 3. Gerar chave SSH (se necessário)

#### Na sua máquina local:

```bash
# Gerar nova chave SSH (se não tiver)
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_actions_deploy

# Ver a chave privada (adicione como SSH_KEY no GitHub)
cat ~/.ssh/github_actions_deploy

# Ver a chave pública (adicione na VPS)
cat ~/.ssh/github_actions_deploy.pub
```

#### Na VPS:

```bash
# Adicionar chave pública ao authorized_keys
echo "sua_chave_publica_aqui" >> ~/.ssh/authorized_keys

# Ajustar permissões
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

### 4. Testar conexão SSH

```bash
# Da sua máquina local, teste a conexão
ssh -i ~/.ssh/github_actions_deploy seu_usuario@seu_ip
```

## 🚀 Como Funciona

### Deploy Automático

O workflow é executado automaticamente quando:
- Você faz `git push` para a branch `main`
- Alguém faz merge de PR para `main`

### Deploy Manual

Você também pode executar manualmente:
1. Vá para **Actions** no GitHub
2. Selecione **Deploy to Production**
3. Clique em **Run workflow**
4. Escolha a branch e clique em **Run workflow**

## 📝 Checklist Antes do Primeiro Deploy

- [ ] Secrets configurados no GitHub (`SSH_HOST`, `SSH_USER`, `SSH_KEY`)
- [ ] Chave SSH pública adicionada na VPS
- [ ] Docker e Docker Compose instalados na VPS
- [ ] Diretório `~/petstory-api` existe na VPS
- [ ] Arquivo `.env` configurado na VPS (ou o workflow criará a partir do `env.example`)
- [ ] Repositório clonado na VPS: `git clone <seu-repo> ~/petstory-api`

## 🔍 Verificar Deploy

Após o deploy, você pode verificar:

```bash
# Na VPS
cd ~/petstory-api
docker compose ps
docker compose logs -f api
curl http://localhost:8000/health
```

## 🐛 Troubleshooting

### Erro: "Permission denied (publickey)"

- Verifique se a chave SSH está correta no GitHub
- Verifique se a chave pública está no `authorized_keys` da VPS
- Teste a conexão manualmente

### Erro: "Directory not found"

- Certifique-se de que o diretório `~/petstory-api` existe na VPS
- Verifique o caminho no workflow

### Erro: "docker compose: command not found"

- Instale Docker Compose na VPS
- Verifique se está usando `docker compose` (v2) e não `docker-compose` (v1)

### Erro: "Health check failed"

- Verifique os logs: `docker compose logs api`
- Verifique se todas as variáveis do `.env` estão configuradas
- Verifique se a porta 8000 está acessível

## 📚 Recursos

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [SSH Agent Action](https://github.com/webfactory/ssh-agent)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

