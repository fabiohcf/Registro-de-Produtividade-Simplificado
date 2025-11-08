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