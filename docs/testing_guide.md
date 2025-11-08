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