# 🚀 Quick Start - PetStory

## Passos Rápidos para Começar

### 1. Instalar dependências
```bash
uv sync
```

### 2. Ativar ambiente virtual
```bash
source .venv/bin/activate
```

### 3. Executar migrations
```bash
uv run python manage.py migrate
```

### 4. Criar superusuário (opcional, para acessar /admin/)
```bash
uv run python manage.py createsuperuser
```

### 5. Iniciar servidor
```bash
uv run python manage.py runserver
```

### 6. Acessar a aplicação
- Landing: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## 📋 Fluxo de Uso

1. **Criar conta** em `/register/`
2. **Fazer login** em `/login/`
3. **Criar um pet** em `/pets/create/`
4. **Adicionar 2-5 momentos** em `/moments/add/<slug>/`
5. **Gerar história** clicando em "Gerar História com IA"
6. **Visualizar história** e baixar PDF
7. **Compartilhar** link público em `/p/<slug>/`

## 🎯 Funcionalidades Testadas

✅ Autenticação completa
✅ CRUD de pets
✅ Adição de momentos (2-5)
✅ Geração de histórias (simulada)
✅ Download de PDF
✅ Página pública
✅ Marca d'água em versão FREE

## 🔧 Troubleshooting

### Erro ao gerar PDF
- Certifique-se de que o WeasyPrint está instalado
- No Linux, pode ser necessário instalar: `sudo apt-get install python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0`

### Erro ao processar imagens
- Certifique-se de que o Pillow está instalado
- Verifique permissões da pasta `media/`

### Erro de migrations
```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

