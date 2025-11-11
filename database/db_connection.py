from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

#criando uma instância do banco de dados
engine = create_engine('sqlite:///bot.db', echo=False)

# Cria as tabelas, se ainda não existirem
Base.metadata.create_all(bind=engine)

#cria uma sessão dentro da data base
sessaoAtual = sessionmaker(bind=engine, autocommit=False, autoflush=False)