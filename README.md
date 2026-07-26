# Registro de Produtividade

Aplicação web para gerenciamento de produtividade pessoal, permitindo registrar sessões de estudo, acompanhar metas semanais e analisar evolução de desempenho.

Este projeto iniciou como uma atividade acadêmica do curso de **Análise e Desenvolvimento de Sistemas (UNIASSELVI)** e evoluiu para uma aplicação pessoal com arquitetura profissional, API REST, autenticação segura, persistência em banco relacional e suíte de testes automatizados.

O objetivo principal é transformar o acompanhamento de produtividade em dados estruturados, permitindo ao usuário controlar tempo dedicado, metas semanais e histórico de desempenho.

---

# 🚀 Funcionalidades

## 👤 Gestão de usuários

- Cadastro de usuários
- Consulta e gerenciamento de usuários
- Autenticação utilizando JWT
- Controle seguro de credenciais

---

## 🎯 Metas semanais

Sistema de metas baseado em semanas do calendário.

Cada usuário pode possuir uma meta semanal contendo:

- Ano (`year`)
- Número da semana (`week_number`)
- Meta de horas (`target_hours`)
- Meta de questões (`target_questions`)

Regras implementadas:

- Apenas uma meta por usuário em cada semana
- Validação de dados obrigatórios
- Atualização de metas existentes
- Remoção automática quando os objetivos são zerados

---

## ⏱️ Sessões de produtividade (Backend V2)

O módulo de sessões foi totalmente reformulado utilizando uma abordagem baseada em estados.

Estados disponíveis:

```
running
paused
finished
cancelled
```

Fluxo permitido:

```
START
  |
  v
RUNNING
  |
  v
PAUSE
  |
  v
PAUSED
  |
  v
RESUME
  |
  v
RUNNING
  |
  v
FINISH
  |
  v
FINISHED
```

Funcionalidades:

- Início de sessão
- Pausa temporária
- Retomada da sessão
- Finalização
- Cancelamento
- Controle de tempo líquido
- Associação com metas semanais
- Validação de sessões duplicadas ou inválidas

O cálculo de produtividade considera:

```
Tempo líquido =
Tempo total da sessão - períodos pausados
```

---

# 🏗️ Arquitetura

O projeto utiliza uma arquitetura modular baseada em:

- App Factory Pattern
- Flask Blueprints
- Service Layer
- ORM com SQLAlchemy
- Separação entre rotas, regras de negócio e modelos

Estrutura:

```
Request
   |
   v
Blueprints (Routes)
   |
   v
Services
   |
   v
SQLAlchemy Models
   |
   v
Database
```

---

# 🛠️ Tecnologias utilizadas

## Backend

- Python 3.12
- Flask
- SQLAlchemy ORM
- Flask-JWT-Extended
- Alembic
- Pytest
- Werkzeug Security

---

## Banco de dados

Produção:

- PostgreSQL

Desenvolvimento/Testes:

- SQLite

---

## Controle de versão

- Git
- GitHub

---

# 📁 Estrutura do projeto

```
.
├── app/
│   ├── models/
│   │   ├── user.py
│   │   ├── goal.py
│   │   └── session.py
│   │
│   ├── routes/
│   │   ├── api_auth.py
│   │   ├── api_users.py
│   │   ├── api_goals.py
│   │   ├── api_sessions.py
│   │   ├── goal_service.py
│   │   └── session_service.py
│   │
│   ├── database.py
│   └── __init__.py
│
├── tests/
│   ├── test_users.py
│   ├── test_goals.py
│   ├── test_sessions.py
│   ├── test_sessions_api.py
│   ├── test_auth.py
│   └── test_validations.py
│
├── alembic/
│   └── versions/
│
├── requirements.txt
├── requirements-dev.txt
├── app.py
└── README.md
```

---

# 🔐 Segurança

Implementações atuais:

- Autenticação JWT
- Cookies seguros para tokens
- Hash de senhas utilizando Werkzeug
- Validação de dados de entrada
- Controle de permissões entre usuários
- Configuração por variáveis de ambiente

---

# 🌐 API REST

## Autenticação

| Método | Endpoint | Descrição |
|-|-|-|
| POST | `/auth/login` | Login |
| POST | `/auth/refresh` | Renovação de token |

---

## Usuários

| Método | Endpoint | Descrição |
|-|-|-|
| GET | `/api/users/` | Listar usuários |
| POST | `/api/users/` | Criar usuário |
| GET | `/api/users/{id}` | Buscar usuário |
| PUT | `/api/users/{id}` | Atualizar usuário |
| DELETE | `/api/users/{id}` | Remover usuário |

---

## Metas

| Método | Endpoint | Descrição |
|-|-|-|
| GET | `/api/goals/` | Listar metas semanais |
| POST | `/api/goals/` | Criar meta semanal |
| PUT | `/api/goals/{id}` | Atualizar meta semanal |

---

## Sessões

| Método | Endpoint | Descrição |
|-|-|-|
| POST | `/api/sessions/start` | Iniciar sessão |
| POST | `/api/sessions/pause` | Pausar sessão |
| POST | `/api/sessions/resume` | Retomar sessão |
| POST | `/api/sessions/finish` | Finalizar sessão |
| POST | `/api/sessions/cancel` | Cancelar sessão |
| GET | `/api/sessions/list` | Listar sessões |

---

# 🧪 Testes automatizados

O projeto utiliza Pytest para garantir a estabilidade das regras de negócio.

Cobertura atual:

```
63 testes passando
```

Cenários testados:

- Cadastro de usuários
- Autenticação
- Validações
- CRUD de metas semanais
- Fluxo completo de sessões
- Estados inválidos de sessões
- Regras de negócio
- Integração entre API e banco de dados

Executar testes:

```bash
pytest
```

Modo detalhado:

```bash
pytest -v
```

Teste específico:

```bash
pytest tests/test_sessions_api.py
```

---

# ⚙️ Configuração local

## Pré-requisitos

- Python 3.12+
- PostgreSQL (produção)
- Git

---

## Clone

```bash
git clone https://github.com/fabiohcf/Registro-de-Produtividade.git

cd Registro-de-Produtividade
```

---

## Ambiente virtual

Linux/macOS:

```bash
python -m venv .venv

source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

---

## Dependências

Produção:

```bash
pip install -r requirements.txt
```

Desenvolvimento:

```bash
pip install -r requirements-dev.txt
```

---

## Variáveis de ambiente

Criar arquivo:

```
.env
```

Exemplo:

```env
JWT_SECRET_KEY=sua-chave-secreta

DATABASE_URL=postgresql+psycopg2://usuario:senha@localhost:5432/registro_prod
```

---

# Banco de dados

Executar migrações:

```bash
alembic upgrade head
```

Criar estrutura inicial:

```bash
python app.py
```

---

# Executando aplicação

```bash
python app.py
```

Aplicação disponível em:

```
http://127.0.0.1:5000
```

---

# 📈 Evolução do projeto

## Versão inicial

Projeto acadêmico simples:

- Registro básico de produtividade
- SQLite local
- Estrutura monolítica inicial

---

## Backend V2

Principais melhorias:

- Migração para arquitetura modular
- PostgreSQL preparado para produção
- Alembic para versionamento de banco
- API REST estruturada
- Autenticação JWT
- Metas semanais
- Máquina de estados para sessões
- Camada de serviços
- Testes automatizados

---

# 🔮 Próximos passos

Planejamento futuro:

- Integração com frontend React + TypeScript
- Dashboard de produtividade
- Gráficos de evolução
- Relatórios personalizados
- Deploy completo em nuvem
- Documentação OpenAPI/Swagger

---

# 👨‍💻 Autor

**Fábio Henrique Costa Ferreira**

Desenvolvedor Backend | em formação

Estudante de Análise e Desenvolvimento de Sistemas

Interesses:

- Desenvolvimento Backend
- Arquitetura de software
- APIs REST
- Banco de dados
- Cloud e DevOps

---

# 📄 Licença

Projeto desenvolvido para fins educacionais, portfólio e evolução profissional.