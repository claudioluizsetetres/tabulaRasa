# Importa os módulos do SQL Alchemy.
from sqlalchemy import (
    create_engine, Column, ForeignKey,
    Integer, Text, String, Date, DateTime, Boolean
)

# Importa os módulos do ORM (Object-Relational Mapping) do SQL Alchemy.
from sqlalchemy.orm import (
    declarative_base, relationship
)

# importa a biblioteca  para manipular o sistema operacional
import os


# Configuração do banco de dados (SQLite).
database_path = os.environ.get("DATA_DIR", "data")
engine = create_engine(f'sqlite:///{database_path}/tabulaRasa.db')

# Configuração do SQL Alchemy que transforma as classes em tabela.
Tabular = declarative_base()

# Define uma tabela para armazenar informações do usuário.
class Usuario (Tabular):

    # Nome da tabela.
    __tablename__ = 'usuario'

    # Atributos da tabela.
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    nascimento = Column(Date, nullable=False)
    endereco = Column(Text, nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    senha = Column(String(255), nullable=False)
    perfil = Column(String(20), nullable=False)
    ativo = Column(Boolean, default=True)

    # Relacionamento da tabela.
    emprestimo = relationship('Emprestimo', back_populates='usuario')

    # Método que exibe as informações registradas.
    def __repr__ (self):

        return f'Usuário: {self.nome}, {self.cpf}, {self.nascimento}, {self.telefone}, {self.perfil}'
    
# Define uma tabela para armazenar informações do livro.
class Livro (Tabular):

    # Nome da tabela.
    __tablename__ = 'livro'

    # Atributos da tabela.
    id = Column(Integer, primary_key=True)
    titulo = Column(String(100), nullable=False)
    isbn = Column(String(25), unique=True, nullable=False)
    autor = Column(Text, nullable=False)
    editora = Column(String(100), nullable=False)
    edicao = Column(String(15), nullable=True)
    volume = Column(Integer, nullable=True)
    genero_literario = Column(String(100), nullable=False)
    numero_paginas = Column(Integer, nullable=False)
    ano_publicacao = Column(Integer, nullable=False)
    exemplares = Column(Integer, nullable=False)
    ativo = Column(Boolean, default=True)

    # Relacionamento da tabela.
    emprestimo = relationship('Emprestimo', back_populates='livro')

    # Método que exibe as informações registradas.
    def __repr__ (self):

        return f'Livro: {self.titulo}, {self.isbn}, {self.autor}, {self.editora}, {self.ano_publicacao}'
    
# Define uma tabela para vincular um leitor a um livro.
class Emprestimo (Tabular):

    # Nome da tabela.
    __tablename__ = 'emprestimo'

    # Atributos da tabela.
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    id_livro = Column(Integer, ForeignKey('livro.id'), nullable=False)
    data_emprestimo = Column(DateTime, nullable=False)
    data_devolucao = Column(DateTime, nullable=False)
    status = Column(String(25), nullable=False)
    ativo = Column(Boolean, default=True)

    # Relacionamento da tabela.
    usuario = relationship('Usuario', back_populates='emprestimo')
    livro = relationship('Livro', back_populates='emprestimo')

    # Método que exibe as informações registradas.
    def __repr__ (self):

        return f'Empréstimo: {self.id}, {Livro.titulo}, {Usuario.nome}, {self.data_emprestimo}, {self.data_devolucao}'
    
