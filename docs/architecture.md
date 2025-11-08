# Arquitetura do Projeto — Registro de Produtividade

Visão geral:
- Aplicação orientada a serviços leve para registro e análise de produtividade pessoal/equipe.
- Separação clara entre frontend (UI), backend (API) e persistência (database). Componentes comunicam por HTTP/REST e filas/opcionais para tarefas assíncronas.

Principais componentes:
- API Server
  - responsibility: expor endpoints REST para CRUD de registros, autenticação e relatórios.
  - suggested tech: Python + FastAPI / Node.js + Express (variáveis e rotas em English).
- Frontend
  - responsibility: interface para criar/editar registros, visualizar relatórios e dashboards.
  - suggested tech: React / Vue (state keys em English).
- Database
  - responsibility: armazenar users, entries, projects e metadados.
  - suggested tech: Postgres (relacional) com migrations.
- Worker (opcional)
  - responsibility: tarefas assíncronas como geração de relatórios, envio de e-mails, limpeza de dados.
  - suggested tech: Celery / RQ / Bull.

Comunicação e integrações:
- API ↔ Frontend: HTTP/JSON.
- API ↔ DB: pool de conexões (env var DATABASE_URL).
- Worker ↔ API/DB: broker (REDIS_URL) para filas.
- Observability: logs estruturados (JSON), métricas (Prometheus), tracing (optional).

Configuração e variáveis de ambiente (em English):
- DATABASE_URL — cadeia de conexão do banco de dados.
- TEST_DATABASE_URL — conexão do banco de testes.
- SECRET_KEY — segredo para signing tokens/sessions.
- JWT_ALGORITHM — algoritmo JWT (ex: HS256).
- REDIS_URL — broker/cache.
- SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD — envio de e-mail.
- SENTRY_DSN — integração de observability.
- APP_ENV — environment (development | staging | production).
- APP_PORT — porta do API server.

Recomendações operacionais:
- Migrations versionadas (Flyway / Alembic / Liquibase).
- Separar env vars por ambiente e não commitar segredos.
- Pipelines CI: lint → tests → build → deploy.
- Tenha testes unitários e testes de integração com DB isolado (docker-compose / testcontainers).

Diagrama lógico (resumo):
Frontend <--> API Server <--> Database
                      |
                      v
                   Worker (Redis Broker)

# API Endpoints — Registro de Produtividade

Notas:
- Descrições em pt-BR; nomes de campos e parâmetros em English.
- Base path: /api/v1

Autenticação
- POST /api/v1/auth/login
  - body: { "email": "string", "password": "string" }
  - response: { "access_token": "string", "token_type": "bearer" }
  - descrição: autentica o usuário e retorna token JWT.

- POST /api/v1/auth/register
  - body: { "email": "string", "password": "string", "name": "string" }
  - response: { "user_id": "uuid", "email": "string", "name": "string" }
  - descrição: cria novo usuário.

Users
- GET /api/v1/users/{user_id}
  - path: user_id (uuid)
  - response: { "user_id": "uuid", "email": "string", "name": "string", "created_at": "iso8601" }
  - descrição: obtém dados do usuário.

Entries (registros de produtividade)
- POST /api/v1/entries
  - body:
    {
      "user_id": "uuid",
      "project_id": "uuid | null",
      "date": "YYYY-MM-DD",
      "start_time": "HH:MM",
      "end_time": "HH:MM",
      "duration_minutes": "integer",
      "task": "string",
      "description": "string",
      "productivity_score": "number (0-100)"
    }
  - response: { "entry_id": "uuid", ...entry_fields }
  - descrição: cria um registro de tempo/atividade.

- GET /api/v1/entries?user_id={user_id}&start_date={YYYY-MM-DD}&end_date={YYYY-MM-DD}&project_id={project_id}
  - response: [ { entry }, ... ]
  - descrição: lista registros filtrando por usuário, período e projeto.

- GET /api/v1/entries/{entry_id}
  - response: { entry }
  - descrição: obtém registro específico.

- PUT /api/v1/entries/{entry_id}
  - body: fields a atualizar (mesmos nomes em English)
  - response: { entry }
  - descrição: atualiza registro.

- DELETE /api/v1/entries/{entry_id}
  - response: 204 No Content
  - descrição: remove registro.

Projects
- CRUD similar a Entries:
  - POST /api/v1/projects { "name": "string", "owner_id": "uuid", "description": "string | null" }
  - GET /api/v1/projects/{project_id}
  - GET /api/v1/projects?owner_id={owner_id}
  - PUT /api/v1/projects/{project_id}
  - DELETE /api/v1/projects/{project_id}

Reports
- GET /api/v1/reports/summary?user_id={user_id}&start_date={YYYY-MM-DD}&end_date={YYYY-MM-DD}
  - response:
    {
      "user_id": "uuid",
      "total_minutes": "integer",
      "average_productivity": "number",
      "by_project": [ { "project_id": "uuid", "total_minutes": "integer", "average_productivity": "number" } ]
    }
  - descrição: resumo agregado de produtividade.

Observações de segurança:
- Todas rotas que manipulam dados sensíveis devem exigir Authorization: Bearer {access_token}.
- Validação de input (schema validation) para evitar injeção e dados inválidos.

# Database Schema — Registro de Produtividade

Padronização:
- Nomes de tabelas e colunas em English (snake_case).
- Tipos e constraints mínimas descritas; adapte conforme o banco (Postgres recomendado).

Tabela: users
- id UUID PRIMARY KEY — Identificador do usuário (user_id).
- email VARCHAR UNIQUE NOT NULL — E-mail do usuário.
- password_hash VARCHAR NOT NULL — Hash da senha.
- name VARCHAR NOT NULL — Nome exibido (name).
- created_at TIMESTAMP WITH TIME ZONE DEFAULT now() — Data de criação.
- is_active BOOLEAN DEFAULT true — Usuário ativo.

Tabela: projects
- id UUID PRIMARY KEY — project_id.
- owner_id UUID REFERENCES users(id) ON DELETE CASCADE — Proprietário do projeto.
- name VARCHAR NOT NULL — Nome do projeto.
- description TEXT — Descrição opcional.
- created_at TIMESTAMP WITH TIME ZONE DEFAULT now().

Índice recomendado: idx_projects_owner_id (owner_id)

Tabela: entries
- id UUID PRIMARY KEY — entry_id.
- user_id UUID REFERENCES users(id) ON DELETE CASCADE — Dono do registro.
- project_id UUID REFERENCES projects(id) — Projeto relacionado (nullable).
- date DATE NOT NULL — Data da atividade.
- start_time TIME — Hora de início (opcional).
- end_time TIME — Hora de término (opcional).
- duration_minutes INTEGER NOT NULL — Duração em minutos.
- task VARCHAR NOT NULL — Tarefa resumida.
- description TEXT — Descrição detalhada.
- productivity_score NUMERIC(5,2) — Pontuação de produtividade (0-100).
- created_at TIMESTAMP WITH TIME ZONE DEFAULT now().
- updated_at TIMESTAMP WITH TIME ZONE DEFAULT now().

Índices recomendados:
- idx_entries_user_date (user_id, date)
- idx_entries_project (project_id)

Tabela: sessions (opcional para refresh tokens)
- id UUID PRIMARY KEY — session_id.
- user_id UUID REFERENCES users(id) ON DELETE CASCADE.
- refresh_token_hash VARCHAR NOT NULL.
- expires_at TIMESTAMP WITH TIME ZONE NOT NULL.
- created_at TIMESTAMP WITH TIME ZONE DEFAULT now().

Migrações:
- Use migrations versionadas (ex: Alembic, Flyway) para garantir histórico e reprodutibilidade.

Considerações:
- Armazenar apenas hashes de senha; usar salt e algoritmos adaptativos (bcrypt/argon2).
- Constraints adicionais (CHECK para productivity_score entre 0 e 100).
- Particionamento/retention policy para entries antigos se volume crescer muito.

# Guia de Testes — Registro de Produtividade

Objetivo:
- Garantir qualidade com testes unitários, testes de integração e testes end-to-end.

Ferramentas sugeridas:
- Backend: pytest (Python) ou Jest (Node).
- Banco de testes: usar Testcontainers / docker-compose com TEST_DATABASE_URL.
- Coverage: coverage.py / nyc.
- Linters: flake8 / eslint.

Variáveis de ambiente para testes (em English):
- TEST_DATABASE_URL — conexão para o banco de testes.
- TEST_REDIS_URL — broker/cache para testes se necessário.
- SKIP_INTEGRATION — flag opcional para pular testes que precisam de infra.

Comandos comuns (exemplo Python):
- Instalar deps:
  - pip install -r requirements-dev.txt
- Rodar todos os testes:
  - pytest
- Rodar com coverage:
  - coverage run -m pytest && coverage report
- Rodar testes de integração:
  - TEST_DATABASE_URL=postgres://... pytest tests/integration

Estrutura recomendada de pastas:
- tests/unit/  — testes unitários (isolados, sem DB).
- tests/integration/ — testes com DB e integrações reais.
- tests/e2e/ — testes ponta a ponta (opcional).

Práticas:
- Mockar dependências externas (email, APIs) em unit tests.
- Para endpoints, usar test client (FastAPI TestClient / supertest) para validar rotas.
- Limpar estado entre testes (fixtures que resetam DB).
- Criar fixtures para criar users/projects/entries reutilizáveis (names in English).

Exemplo rápido de fixture (pytest):
```python
# filepath: tests/conftest.py
import pytest
from app import create_app
from app.db import get_db, init_db

@pytest.fixture(scope="function")
def test_client():
    app = create_app(config={"DATABASE_URL": "sqlite:///:memory:"})
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client
```

Dicas de CI:
- Executar linter antes dos testes.
- Rodar testes paralelos quando possível (pytest-xdist).
- Gerar badge de coverage e falhar build se coverage < threshold.

Checklist antes do merge:
- Todos os testes unitários passam.
- Cobertura para novas features criada.
- No breaking changes: documentar no changelog.

