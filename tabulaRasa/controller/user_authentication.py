# importa os modulos do Flask
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

# importa o modulo do sql alchemy que cria conexao banco de dados
from sqlalchemy.orm import sessionmaker

# importa o modulo do werkzeug que compar senha criptogragada
from werkzeug.security import check_password_hash

# importa as classes do banco de dados
from models.database import engine, Usuario

# cria uma instancia do blueprint
blueprint = Blueprint("user_authentication", __name__)

# cria uma sessão do back-end com banco de dados
Session = sessionmaker(bind=engine)


# rota para o login de usuario
@blueprint.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        # recupera os dados enviado pelo formulario de html
        cpf = request.form["cpf"]
        senha = request.form["senha"]

        # abre conexao com o bando de dados
        connection = Session()

        # busca o usuario no banco usando o cpf
        existe = connection.query(Usuario).filter_by(cpf=cpf).first()

        # fechar conexao com o banco
        connection.close()

        # verifica se o usuario existe e se a senha esta correta
        if existe and check_password_hash(existe.senha, senha):

            # grava informações do usuário em cookies do navegador
            session["user_id"] = existe.id
            session["user_name"] = existe.nome

            # redireciona o usuario para o main.html
            return redirect(url_for("user_authentication.dashboard"))

        else:
            # retorna uma mensagens ao usuario
            flash("CPF ou senha inválidos...", "danger")

            # redereciona o usuario para o index
            return redirect(url_for("user_authentication.login"))

    else:

        # renderiza o html do login do usuario
        return render_template("index.html")
    
# rota para o dashboar.html
@blueprint.route("/dashboard")
def dashboard():

    # verifica se existem informações armazenadas na sessão de usuario
    if "user_id" in session:

        # renderiza o html do main
        return render_template("dashboard.html")
    
    else:

        # retorna uma mensagens ao usuario
        flash("Para acessar o software faça login...", "warning")

        # redereciona o usuario para o index
        return redirect(url_for("user_authentication.login"))
    
# rota para logout do usuario
@blueprint.route("/logout")
def logout():
    # remove todos os cookies e dados da sessão de usário
    session.clear()

    # retorna uma mensagens de sucesso
    flash("Logout feito com sucesso!!!", "success")

    # redereciona o usuario para o index
    return redirect(url_for("user_authentication.login"))