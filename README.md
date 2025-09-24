# Registro de Produtividade - Projeto Pessoal

Este é um **projeto pessoal** que evoluiu de uma atividade acadêmica inicial. A versão original (simplificada) foi desenvolvida como parte da disciplina Imersão Profissional do curso de Análise e Desenvolvimento de Sistemas (UNIASSELVI). 

Esta versão expandida representa uma **evolução profissional** do conceito original, transformando um projeto acadêmico básico em uma aplicação robusta e escalável, pronta para uso em produção com múltiplos usuários.

## 🚀 Funcionalidades Principais

- **Gestão de Usuários**: Cadastro, autenticação e gerenciamento de usuários
- **Metas de Produtividade**: Definição de metas semanais de horas de estudo/trabalho
- **Sessões de Trabalho**: Controle de início, pausa, reinício e finalização de sessões
- **Autenticação Segura**: Sistema JWT com cookies seguros e CSRF protection
- **API REST**: Endpoints padronizados para integração frontend/mobile
- **Validações Robustas**: Validação completa de dados com mensagens em português
- **Testes Automatizados**: Cobertura completa de testes unitários e de integração

## 🛠 Tecnologias Utilizadas

### Backend
- **Python 3.12**
- **Flask** (framework web)
- **SQLAlchemy** (ORM)
- **Flask-JWT-Extended** (autenticação)
- **Alembic** (migrações de banco)
- **Pytest** (testes)

### Banco de Dados
- **PostgreSQL** (produção)
- **SQLite** (testes e desenvolvimento local)

### Infraestrutura
- **Render** (deploy em produção)
- **Git** (controle de versão)

## 📁 Estrutura do Projeto

```
├── app/
│   ├── __init__.py              # App factory e configuração JWT
│   ├── database.py              # Configuração de banco de dados
│   ├── models/                  # Modelos SQLAlchemy
│   │   ├── user.py
│   │   ├── goal.py
│   │   └── session.py
│   ├── routes/                  # Blueprints da API
│   │   ├── api_users.py
│   │   ├── api_goals.py
│   │   ├── api_sessions.py
│   │   ├── api_auth.py
│   │   └── main.py
│   ├── templates/               # Templates HTML
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── meta.html
│   │   └── relatorio.html
│   └── static/                  # Arquivos estáticos
│       ├── css/
│       ├── js/
│       └── img/
├── tests/                       # Testes automatizados
│   ├── test_users.py
│   ├── test_goals.py
│   ├── test_sessions.py
│   ├── test_auth.py
│   └── test_validations.py
├── alembic/                     # Migrações de banco
├── app.py                       # Ponto de entrada
├── requirements.txt             # Dependências de produção
├── requirements-dev.txt         # Dependências de desenvolvimento
└── .env.example                 # Exemplo de variáveis de ambiente
```

## 🔧 Configuração e Instalação

### Pré-requisitos
- Python 3.12+
- PostgreSQL (para produção)
- Git

### 1. Clone o repositório
```bash
git clone https://github.com/fabiohcf/Registro-de-Produtividade.git
cd Registro-de-Produtividade
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```bash
# Chave secreta para JWT (obrigatória)
JWT_SECRET_KEY=sua-chave-secreta-forte-aqui

# URL do banco de dados (obrigatória para produção)
DATABASE_URL=postgresql+psycopg2://usuario:senha@localhost:5432/registro_prod
```

### 5. Configure o banco de dados

#### Para desenvolvimento (SQLite):
```bash
python app.py  # Cria automaticamente o banco SQLite
```

#### Para produção (PostgreSQL):
```bash
# Crie o banco no PostgreSQL
createdb registro_prod

# Execute as migrações
alembic upgrade head
```

### 6. Execute a aplicação
```bash
python app.py
```

A aplicação estará disponível em: http://127.0.0.1:5000

## 🧪 Executando Testes

```bash
# Execute todos os testes
pytest

# Execute com verbose
pytest -v

# Execute testes específicos
pytest tests/test_users.py
```

## 📚 API Endpoints

### Autenticação
- `POST /auth/login` - Login de usuário
- `POST /auth/refresh` - Renovar token de acesso
- `POST /auth/logout` - Logout (limpa cookies)

### Usuários
- `GET /api/users/` - Listar usuários
- `POST /api/users/` - Criar usuário
- `GET /api/users/{id}` - Buscar usuário por ID
- `PUT /api/users/{id}` - Atualizar usuário
- `DELETE /api/users/{id}` - Deletar usuário

### Metas
- `GET /api/goals/` - Listar metas
- `POST /api/goals/` - Criar meta

### Sessões
- `POST /api/sessions/start` - Iniciar sessão
- `POST /api/sessions/pause` - Pausar sessão
- `POST /api/sessions/restart` - Reiniciar sessão
- `POST /api/sessions/finish` - Finalizar sessão

## 🔒 Segurança

- **Autenticação JWT** com cookies seguros
- **CSRF Protection** ativado em produção
- **Validação de dados** robusta com mensagens em português
- **Hash de senhas** com Werkzeug
- **Variáveis de ambiente** para configurações sensíveis

## 🌐 Deploy em Produção

### Render (recomendado)
1. Conecte seu repositório ao Render
2. Configure as variáveis de ambiente:
   - `JWT_SECRET_KEY`
   - `DATABASE_URL` (PostgreSQL)
3. O deploy será automático a cada push

### Variáveis de ambiente necessárias:
```bash
JWT_SECRET_KEY=sua-chave-secreta-forte
DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/dbname
```

## 🏗 Arquitetura

- **App Factory Pattern**: Criação flexível da aplicação
- **Blueprint Organization**: Separação modular de rotas
- **ORM com SQLAlchemy**: Mapeamento objeto-relacional
- **Test-Driven Development**: Desenvolvimento orientado a testes
- **Separation of Concerns**: Separação clara de responsabilidades

## 📈 Evolução Profissional - Melhorias Implementadas

### 🔄 **Transformação de Projeto Acadêmico para Profissional**
- **Base acadêmica**: Versão simplificada com SQLite local e interface básica
- **Evolução pessoal**: Arquitetura robusta com APIs REST e autenticação segura

### ✅ **Implementações Técnicas Avançadas**
- **Autenticação JWT** com cookies seguros e CSRF protection
- **Validações robustas** em todos os endpoints com mensagens em português
- **Testes automatizados** com alta cobertura (30+ testes)
- **Suporte a PostgreSQL** para produção com Alembic migrations
- **API REST** padronizada e documentada
- **Estrutura modular** com Blueprints e App Factory pattern
- **Padronização de código** com Black e boas práticas
- **Configuração flexível** para diferentes ambientes (dev/prod/test)

## 📄 Licença

Uso educacional para fins de demonstração acadêmica.

## 👨‍💻 Autor

**Fábio Henrique Costa Ferreira**  
Desenvolvedor Full Stack | Estudante de Análise e Desenvolvimento de Sistemas - UNIASSELVI

### 🎯 **Objetivo do Projeto**
Este projeto pessoal demonstra a **capacidade de evolução técnica** e **aprendizado contínuo**, transformando um conceito acadêmico simples em uma aplicação profissional completa. Representa habilidades em:

- **Desenvolvimento Full Stack** com Python/Flask
- **Arquitetura de APIs REST** modernas
- **Autenticação e segurança** (JWT, CSRF, validações)
- **Banco de dados relacionais** (PostgreSQL, SQLAlchemy, Alembic)
- **Testes automatizados** e TDD
- **Deploy em nuvem** e DevOps básico
- **Padrões de código** e boas práticas

---

**Nota**: Este repositório evoluiu de uma atividade acadêmica para um projeto pessoal profissional, demonstrando capacidade de crescimento técnico e aplicação de conceitos avançados de desenvolvimento de software.