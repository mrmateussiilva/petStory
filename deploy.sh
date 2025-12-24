#!/bin/bash
# Script de deploy para PetStory API
# Uso: ./deploy.sh

set -e  # Parar em caso de erro

echo "🚀 Iniciando deploy da PetStory API..."

# Verificar se .env existe
if [ ! -f .env ]; then
    echo "❌ Arquivo .env não encontrado!"
    echo "📝 Copie env.example para .env e configure as variáveis"
    exit 1
fi

# Verificar se Caddyfile existe
if [ ! -f Caddyfile ]; then
    echo "❌ Arquivo Caddyfile não encontrado!"
    exit 1
fi

# Criar diretórios necessários
echo "📁 Criando diretórios..."
mkdir -p temp logs

# Construir imagem Docker
echo "🐳 Construindo imagem Docker..."
docker compose build

# Parar containers existentes
echo "🛑 Parando containers existentes..."
docker compose down

# Iniciar containers
echo "▶️  Iniciando containers..."
docker compose up -d

# Aguardar API ficar pronta
echo "⏳ Aguardando API ficar pronta..."
sleep 5

# Verificar saúde da API
echo "🏥 Verificando saúde da API..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ API está respondendo!"
else
    echo "⚠️  API pode não estar pronta ainda. Verifique os logs:"
    echo "   docker compose logs -f api"
fi

# Verificar se Caddyfile precisa ser copiado
if [ ! -L /etc/caddy/Caddyfile ] && [ ! -f /etc/caddy/Caddyfile ]; then
    echo "📋 Configurando Caddy..."
    echo "   Execute manualmente:"
    echo "   sudo cp Caddyfile /etc/caddy/Caddyfile"
    echo "   sudo caddy validate --config /etc/caddy/Caddyfile"
    echo "   sudo systemctl reload caddy"
else
    echo "✅ Caddyfile já configurado"
fi

echo ""
echo "✅ Deploy concluído!"
echo ""
echo "📊 Comandos úteis:"
echo "   Ver logs:        docker compose logs -f api"
echo "   Ver status:      docker compose ps"
echo "   Parar:           docker compose down"
echo "   Reiniciar:       docker compose restart"
echo ""
echo "🌐 Teste a API:"
echo "   http://localhost:8000/health"
echo ""

