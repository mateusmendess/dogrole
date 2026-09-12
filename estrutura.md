# Estrutura do projeto — DogRolê

Documento gerado na Fase 1 (Estrutura), antes de qualquer implementação de funcionalidade. Descreve a árvore de pastas/arquivos do projeto e o papel de cada parte.

```
dogrole/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── estrutura.md
│
├── core/                          # Configuração central do projeto Django
│   ├── __init__.py
│   ├── settings.py                # Configurações gerais (apps instaladas, banco, templates, idioma/fuso, etc.)
│   ├── urls.py                    # Roteamento raiz do projeto
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/                      # Cadastro/login e perfil do dono
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── migrations/
│   │   └── __init__.py
│   └── templates/accounts/        # Templates específicos desta app
│
├── dogs/                          # Perfil do cão (raça, porte, energia, sociabilidade, fotos, intenção)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── migrations/
│   │   └── __init__.py
│   └── templates/dogs/
│
├── matching/                      # Feed de swipe, algoritmo de compatibilidade, matches
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── services.py                # Lógica do algoritmo de compatibilidade (isolada de models/views)
│   ├── tests.py
│   ├── views.py
│   ├── migrations/
│   │   └── __init__.py
│   └── templates/matching/
│
├── events/                        # Criação/participação em encontros (playdate marcado)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── migrations/
│   │   └── __init__.py
│   └── templates/events/
│
├── subscriptions/                 # Planos gratuito/pago e integração com Mercado Pago
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── services.py                # Integração com a API do Mercado Pago
│   ├── tests.py
│   ├── views.py
│   ├── migrations/
│   │   └── __init__.py
│   └── templates/subscriptions/
│
├── templates/                     # Templates globais (base.html com o esqueleto HTML compartilhado)
│   └── base.html
│
├── static/                        # CSS, JS e imagens do projeto
│   ├── css/
│   ├── js/
│   └── img/
│
└── venv/                          # Ambiente virtual Python (fora do controle de versão)
```

## Decisões tomadas nesta fase

- Nome do projeto: **DogRolê**
- Framework: Django 6.1.1, com o pacote de configuração renomeado para `core` (em vez do padrão `dogrole`, que gera confusão de nome duplicado)
- Cinco apps, uma por funcionalidade principal: `accounts`, `dogs`, `matching`, `events`, `subscriptions`
- Testes: cada app usa o `tests.py` padrão do Django por enquanto; será dividido em uma pasta `tests/` (com `test_models.py`, `test_views.py`, `test_services.py`, etc.) só quando um arquivo específico ficar grande demais — provavelmente `matching` ou `subscriptions` primeiro
- `TEMPLATES.DIRS` aponta para uma pasta `templates/` global (compartilhada entre apps), além dos templates internos de cada app
- `STATICFILES_DIRS` aponta para uma pasta `static/` global; `MEDIA_ROOT`/`MEDIA_URL` configurados para uploads dos usuários (fotos de cães), fora do controle de versão
- `LANGUAGE_CODE = 'pt-br'` e `TIME_ZONE = 'America/Sao_Paulo'`, ajustados para o público brasileiro
- Escopo do MVP: matching de playdate entre donos de cachorro, com um filtro adicional e autodeclarado de interesse em cruzamento (sem verificação, sem marketplace); adoção fora do escopo
- `.gitignore` já configurado para excluir `venv/`, cache do Python, `db.sqlite3`, `media/`, `.env` e configs de editor
