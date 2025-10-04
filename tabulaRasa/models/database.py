# Importa os módulos do SQL Alchemy.
from sqlalchemy import (
    create_engine, Column, ForeignKey,
    Integer, Float, Text, String, Date, DateTime, Boolean
)

# Importa os módulos do ORM (Object-Relational Mapping) do SQL Alchemy.
from sqlalchemy.orm import (
    declarative_base, sessionmaker,
    relationship
)

# importa modulo para criptografar a senha de usuário
from werkzeug.security import generate_password_hash

# importa o modulo para trabalha com data e hora
from datetime import date

# Configuração do banco de dados (SQLite).
engine = create_engine('sqlite:///data/tabulaRasa.db')

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
    
# Cria os objetos no banco de dados (SQLite).
if __name__ == '__main__':

    # Converte o Python em SQL.
    Tabular.metadata.create_all(engine)

    # Feedback para o usuário.
    print('Banco de dados criado com sucesso!')

    # abre a conexao com o banco de dados
    Session = sessionmaker(bind=engine)

    # recurso responsável por executar os comandos no banco de dados
    connection = Session()

    # cria um objeto de usuário (administrador do software)
    newUser = Usuario(
        nome = "Administrador da Tábula rasa",
        cpf = "123.456.789-10",
        nascimento = date(2000, 1, 1),
        endereco = "Servido da Fábula Rasa",
        telefone ="(12) 34567-8910",
        email = "administrador@fabularasa.com",
        senha = generate_password_hash("abc123!!!", method="pbkdf2:sha256"),
        perfil = "Administrador"
    )

    # adiciona o novo usuário ao banco de dados
    connection.add(newUser)

    # confirma a transação
    connection.commit()

    # fecha a conexao
    connection.close()

    # feedback para o usuário
    print("Usuário administrador criado com sucesso!!!")