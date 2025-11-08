# scripts/create_tables.py


from app.database import engine
from app.models.base import Base
from app.models import user, goal, session  # importa os models para registrar no Base

Base.metadata.create_all(bind=engine)
print("Todas as tabelas criadas com sucesso!")
