# Importa o Flask.
from flask import Flask

# Importa os módulos do back-end.
from . import user_authentication
from . import book_management

# Importa os módulos do banco de dados.
from models.database import Tabular, engine, Usuario

# Importa os módulos do ORM ( Objetct Relational Mapping) do SQLAlchemy
from sqlalchemy.orm import sessionmaker
# Importa o módulo para a consulta de existência
from sqlalchemy import select # <--- IMPORTAÇÃO ADICIONADA

# Importa a biblioteca para manipular o sistema operacional.
import os

# Importa o módulo para criptografar a senha de usuário.
from werkzeug.security import generate_password_hash

# Importa o módulo para trabalhar com data e hora.
from datetime import date

# Função que configura a aplicação da web.
def create_application():

    # instância da aplicação web.
    web_application = Flask(__name__, template_folder='../templates', static_folder='../static')

    # Chave de segurança.
    web_application.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '123456')

    # Mapeia os aquvivos de Back-end importados.
    web_application.register_blueprint(user_authentication.blueprint)
    web_application.register_blueprint(book_management.blueprint)
    web_application.register_blueprint(user_management.blueprint)
    web_application.register_blueprint(emprestimo.blueprint)

    # Configurações de cookies (HTTPS).
    web_application.config['SESSION_COOKIE_SAMESITE'] ='Lax'
    web_application.config['SESSION_COOKIE_SECURE'] = True

    # Converte o Python em SQL (Cria as tabelas).
    Tabular.metadata.create_all(engine)

    # Feedback para o usuário.
    print('Banco de dados, criado com sucesso!')

    # Abre a conexão com o banco de dados.
    Session = sessionmaker(bind=engine)

    # Recurso responsável por executar os comandos no banco de dados.
    connection = Session()

    # --- INÍCIO DA CORREÇÃO DE INTEGRIDADE ---

    admin_cpf = '123.456.789-10'

    # 1. Verifica se o usuário administrador JÁ EXISTE no banco.
    # Usamos o `select` do SQLAlchemy 2.0 e `scalar_one_or_none()` para verificar a existência.
    existing_user_query = select(Usuario).where(Usuario.cpf == admin_cpf)
    existing_user = connection.scalar(existing_user_query)

    # 2. Se o usuário NÃO existir, cria e insere.
    if existing_user is None:
        # Criar um objeto de usuário (Administrador do software)
        new_user = Usuario(
            nome='Administrador da Librarium',
            cpf=admin_cpf, # Usa a variável
            nascimento=date(2000, 1, 1),
            endereco='Servidor da Librarium',
            telefone='(12) 34567-8910',
            email='adminstrador@librarium.com.br',
            senha=generate_password_hash('abc123!!', method='pbkdf2:sha256'),
            perfil='Administrador'
        )

        # Adiciona o novo usuário ao banco de dados.
        connection.add(new_user)

        # Confirma a transação.
        connection.commit()

        # Feedback para o usuário.
        print('Usuário administrador criado com sucesso')
    else:
        # Feedback caso o usuário já exista
        print('Usuário administrador JÁ EXISTE no banco. Nenhuma inserção realizada.')

    # --- FIM DA CORREÇÃO DE INTEGRIDADE ---
    
    # Fecha a conexão com o banco de dados.
    connection.close()

    # Retorna a aplicação web.
    return web_application