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