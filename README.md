# PetStory Backend

Backend SaaS para transformar fotos de pets em desenhos de colorir estilo "Bobbie Goods" usando IA (Gemini Imagen 3).

## 🚀 Tecnologias

- **Python 3.12+**
- **FastAPI** - Framework web assíncrono
- **uv** - Gerenciador de pacotes moderno
- **Google Generative AI (Gemini Imagen 3)** - Geração de imagens
- **FPDF2** - Geração de PDFs
- **Resend** - Envio de emails

## 📋 Pré-requisitos

- Python 3.12 ou superior
- [uv](https://github.com/astral-sh/uv) instalado
- Chave de API do Gemini (obrigatória)
- Chave de API do Resend (opcional - se não fornecida, emails serão apenas logados)

## ⚙️ Configuração

1. Clone o repositório e entre no diretório:
```bash
cd petStoryArt
```

2. Copie o arquivo de exemplo de variáveis de ambiente:
```bash
cp .env.example .env
```

3. Edite o arquivo `.env` e adicione suas chaves de API:
```env
GEMINI_API_KEY=sua_chave_gemini_aqui
RESEND_API_KEY=sua_chave_resend_aqui  # Opcional
EMAIL_FROM=noreply@petstory.com
EMAIL_FROM_NAME=PetStory
```

## 🏃 Como Executar

### Desenvolvimento Local

1. Instale as dependências usando `uv`:
```bash
uv sync
```

2. Execute o servidor:
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

O servidor estará disponível em `http://localhost:8000`

### Documentação da API

Após iniciar o servidor, acesse:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🐳 Docker

### Build da imagem:
```bash
docker build -t petstory-backend .
```

### Executar container:
```bash
docker run -p 8000:8000 --env-file .env petstory-backend
```

## 📡 Endpoints

### `POST /upload`

Envia múltiplas fotos de pets para processamento.

**Parâmetros:**
- `email` (query): Email do destinatário
- `files` (form-data): Lista de arquivos de imagem (JPEG, PNG, WebP)

**Exemplo com curl:**
```bash
curl -X POST "http://localhost:8000/upload?email=usuario@example.com" \
  -F "files=@pet1.jpg" \
  -F "files=@pet2.jpg" \
  -F "files=@pet3.jpg"
```

**Resposta:**
```json
{
  "status": "accepted",
  "message": "Processing 3 image(s). You will receive an email at usuario@example.com when ready.",
  "images_count": 3,
  "email": "usuario@example.com"
}
```

### `GET /health`

Verifica o status da API.

**Resposta:**
```json
{
  "status": "healthy"
}
```

## 🏗️ Arquitetura

O projeto segue o padrão **Strategy/Adapter** para geração de imagens:

- **`app/interfaces/image_generator.py`**: Interface abstrata `ImageGenerator`
- **`app/services/gemini_service.py`**: Implementação concreta `GeminiGenerator`
- **Injeção de Dependência**: O `main.py` injeta a abstração, não a implementação

Isso permite fácil substituição do provedor de IA no futuro.

## 📦 Estrutura do Projeto

```
petStoryArt/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py          # Configurações via Pydantic Settings
│   ├── interfaces/
│   │   ├── __init__.py
│   │   └── image_generator.py # Interface abstrata (Strategy pattern)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gemini_service.py  # Implementação Gemini
│   │   ├── pdf_service.py     # Geração de PDFs
│   │   └── email_service.py   # Envio de emails
│   ├── worker.py              # Processamento em background
│   ├── main.py                # FastAPI app e endpoints
│   └── __init__.py
├── pyproject.toml             # Dependências e configuração uv
├── Dockerfile                 # Imagem Docker otimizada
├── .env.example              # Exemplo de variáveis de ambiente
└── README.md
```

## 🔄 Fluxo de Processamento

1. Cliente envia múltiplas fotos via `POST /upload`
2. API valida arquivos e retorna status 202 (Accepted)
3. Worker processa em background:
   - Para cada foto: gera desenho estilo "Bobbie Goods" via Gemini
   - Compila todas as imagens geradas em um PDF A4
   - Envia PDF por email via Resend
4. Cliente recebe email com PDF anexado

## ⚠️ Tratamento de Erros

- Se uma imagem falhar na geração, o processamento continua com as outras
- Erros são registrados em logs e incluídos na resposta final
- Se o email falhar, o PDF ainda é gerado (erro é logado)

## 🔧 Desenvolvimento

### Instalar dependências de desenvolvimento:
```bash
uv sync --dev
```

### Formatação de código:
```bash
uv run black app/
uv run ruff check app/
```

## 📝 Notas

- O worker adiciona um delay de 2 segundos entre gerações para evitar rate limits
- Sem chave do Resend, os emails são apenas logados (modo simulação)
- O prompt usado é otimizado para estilo "Bobbie Goods" (linhas grossas, sem sombreamento, fundo branco)

