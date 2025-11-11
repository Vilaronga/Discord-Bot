from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base

#sqlalchemy: transforma uma classe em uma tabela no banco de dados, ou seja, todas as alteração são feitas como objeto, sem a necessidade de utilizar código sql.

Base = declarative_base() #Classe base em que as classes irão herdar dela para construir as tabelas do banco de dados.

class Usuario(Base):
    __tablename__ = 'usuario'  #aqui informamos que a nossa tabela se chamará usuário, porém no python se chamará usuário

    id = Column(Integer, primary_key=True) #aqui é criada uma coluna "id" e ela vai armazenar dados do tipo inteiro, sendo ela uma chave primária.
    discord_id = Column(Integer, unique=True)
    github_url = Column(String, unique=True)

class Repositorios(Base):
    __tablename__ = 'repositorios'  #aqui informamos que a nossa tabela se chamará usuário, porém no python se chamará usuário

    id = Column(Integer, primary_key=True) #aqui é criada uma coluna "id" e ela vai armazenar dados do tipo inteiro, sendo ela uma chave primária.
    repo_nome = Column(String)
    repo_url = Column(String, unique=True)
    repo_dono = Column(String)