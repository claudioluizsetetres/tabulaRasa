# importa o flask
from flask import Flask

# importa os modulos do bach-end
from . import user_authentication
from . import book_management
from . import user_management
from . import emprestimo

# importa os modulos do banco de dados
from models.database import Tabular, engine, Usuario

# importa modulo para criptografar a senha de usuário
from werkzeug.security import generate_password_hash

# importa os modulos do ORM (Object-Relational-Mapping) do sql Alchemy
from sqlalchemy.orm import sessionmaker

# importa o modulo para trabalha com data e hora
from datetime import date

# importa a biblioteca para manipular o sistema operacional
import os


# função que configura a aplicação da web
def create_application():

    # instancia da aplicação da web
    web_application = Flask(__name__, template_folder="../templates", static_folder="../static")

    # chave de segurança 
    web_application.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "123456")

    # mapea os arquivos de back-end importandos
    web_application.register_blueprint(user_authentication.blueprint)
    web_application.register_blueprint(book_management.blueprint)
    web_application.register_blueprint(user_management.blueprint)
    web_application.register_blueprint(emprestimo.blueprint)

    # configurações de cookies (HTTPS)
    web_application.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    web_application.config["SESSION_COOKIE_SECURE"] = True

     # Converte o Python em SQL.
    Tabular.metadata.create_all(engine)

    # Feedback para o usuário.
    print('Banco de dados criado com sucesso!')

    # abre a conexao com o banco de dados
    Session = sessionmaker(bind=engine)

    # recurso responsável por executar os comandos no banco de dados
    connection = Session()
    
    # variavel para verificar se o cpf do administrador ja existe
    adminCpf = "123.456.789-10"

    # consulta para saber se usuario administrador ja existe
    existing_user_query = select(Usuario).where(Usuario.cpf == adminCpf)
    existing_user = connection.scalar(existing_user_query)

    # se administrado não existir, cria e insere
    if existing_user is None:

        # cria um objeto de usuário (administrador do software)
        newUser = Usuario(
           nome = "Administrador da Tábula rasa",
           cpf = adminCpf,
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

        # feedback para o usuário
        print("Usuário administrador criado com sucesso!!!")

    else:
        # feedback caso o administrador ja exista
        print("Usuário administrador já existe no banco de dados")

    # fecha a conexao
    connection.close()

    # retorna a aplicação da web
    return web_application