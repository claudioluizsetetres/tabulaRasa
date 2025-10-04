# importa o flask
from flask import Flask

# importa os modulos do bach-end
from . import user_authentication
from . import book_management
from . import user_management
from . import emprestimo

# função que configura a aplicação da web
def create_application():

    # instancia da aplicação da web
    web_application = Flask(__name__, template_folder="../templates", static_folder="../static")

    # chave de segurança 
    web_application.config["SECRET_KEY"] = "b'$2b$12$Ea2wM7Q3R6J9K8L7N5P4O1U3E4F6D8H9C0A7B5V9W1X5Y9Z0S1T2A3B4C5D6E7F8'" # claudio791senai senha em hash

    # mapea os arquivos de back-end importandos
    web_application.register_blueprint(user_authentication.blueprint)
    web_application.register_blueprint(book_management.blueprint)
    web_application.register_blueprint(user_management.blueprint)
    web_application.register_blueprint(emprestimo.blueprint)

    # retorna a aplicação da web
    return web_application