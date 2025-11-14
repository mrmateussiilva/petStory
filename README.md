# PetStory - Histórias de Pets com IA

SaaS Django para criar histórias encantadoras de pets usando inteligência artificial.

## 🚀 Funcionalidades

- ✅ Sistema de autenticação (registro e login)
- ✅ Cadastro de pets com foto, nome, espécie e data de nascimento
- ✅ Adição de 2-5 momentos especiais do pet (texto + foto opcional)
- ✅ Geração de histórias com IA (função simulada, pronta para integração OpenAI)
- ✅ Visualização de histórias geradas
- ✅ Geração de PDF com marca d'água (versão FREE)
- ✅ Página pública do pet (/p/<slug>)
- ✅ Sistema Premium (placeholder - pronto para integração de pagamento)

## 📦 Instalação

### 1. Instalar dependências com uv

```bash
uv sync
```

### 2. Ativar ambiente virtual

```bash
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate  # Windows
```

### 3. Executar migrations

```bash
python manage.py migrate
```

### 4. Criar superusuário (opcional)

```bash
python manage.py createsuperuser
```

### 5. Executar servidor de desenvolvimento

```bash
python manage.py runserver
```

Acesse: http://127.0.0.1:8000/

## 🏗️ Estrutura do Projeto

```
petStory/
├── core/              # Configurações do Django
├── users/             # App de autenticação
├── pets/              # App de pets
├── moments/           # App de momentos
├── stories/           # App de histórias e IA
├── templates/         # Templates HTML
├── static/            # Arquivos estáticos
└── media/             # Uploads de imagens
```

## 🔧 Tecnologias

- Python 3.12+
- Django 5.0
- Bootstrap 5 (CDN)
- Pillow (processamento de imagens)
- WeasyPrint (geração de PDF)
- SQLite (banco de dados)

## 📝 Modelos

### Pet
- `user` (ForeignKey)
- `name` (CharField)
- `species` (CharField - choices)
- `birth_date` (DateField)
- `photo` (ImageField)
- `slug` (SlugField - único)

### Moment
- `pet` (ForeignKey)
- `title` (CharField)
- `text` (TextField)
- `image` (ImageField - opcional)

### Story
- `pet` (OneToOneField)
- `generated_text` (TextField)
- `is_premium` (BooleanField)
- `created_at` (DateTimeField)

## 🤖 Integração com IA

O arquivo `stories/services.py` contém a função `generate_story()` que atualmente simula a geração de histórias. 

Para integrar com OpenAI API, substitua o conteúdo da função por:

```python
from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_story(pet, moments):
    prompt = f"Crie uma história encantadora sobre {pet.name}..."
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
```

## 💳 Sistema Premium

O sistema Premium está preparado mas ainda não tem integração de pagamento. Para implementar:

1. Adicione um gateway de pagamento (Stripe, Mercado Pago, etc.)
2. Crie uma view para processar o pagamento
3. Atualize `Story.is_premium = True` após pagamento confirmado
4. Remova marca d'água para usuários premium

## 📄 Rotas Principais

- `/` - Landing page
- `/register/` - Registro
- `/login/` - Login
- `/pets/dashboard/` - Dashboard do usuário
- `/pets/create/` - Criar pet
- `/pets/<slug>/` - Detalhes do pet
- `/pets/<slug>/pdf/` - Download PDF
- `/moments/add/<slug>/` - Adicionar momentos
- `/stories/generate/<slug>/` - Gerar história
- `/stories/view/<slug>/` - Ver história
- `/p/<slug>/` - Página pública do pet

## 🎨 Templates

Todos os templates estão em `templates/` e usam Bootstrap 5 para estilização.

## 🔒 Segurança

- CSRF protection habilitado
- Autenticação requerida para ações sensíveis
- Validação de propriedade (usuário só acessa seus próprios pets)

## 📝 Próximos Passos

- [ ] Integrar OpenAI API
- [ ] Implementar sistema de pagamento
- [ ] Adicionar mais opções de personalização
- [ ] Sistema de compartilhamento em redes sociais
- [ ] Dashboard administrativo melhorado

## 📧 Suporte

Para dúvidas ou problemas, abra uma issue no repositório.

---

Desenvolvido com ❤️ usando Django

