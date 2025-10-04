# importa os modulos do Flask
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

# importa o modulo do sql alchemy que cria conexao banco de dados
from sqlalchemy.orm import sessionmaker

# importa as classes do banco de dados
from models.database import engine, Usuario

# importa modulo para criptografar a senha de usuário
from werkzeug.security import generate_password_hash

from datetime import date, datetime

# cria uma instancia do blueprint
blueprint = Blueprint("user_management", __name__)

# cria uma sessão do back-end com banco de dados
Session = sessionmaker(bind=engine)

# rota para gerenciamento de usuário
@blueprint.route("/usuarios")
def listUsers():

    # verifica se o usuario esta logado
    if "user_id" not in session:

        # retorna uma mensagens ao usuario
        flash("Para acessar o software faça login...", "warning")

        # redereciona o usuario para o index
        return redirect(url_for("user_authentication.login"))
    
    else:
        # abre a conexao com bd
        Connection = Session()

        # busca todos os livros cadaastrados
        tblUser = Connection.query(Usuario).filter(Usuario.ativo == True, Usuario.perfil !="Administrador").order_by(Usuario.nome).all()

        # fecha conexao bd
        Connection.close()

        # renderiza o html do listagem de cadastro de livros
        return render_template("userList.html", cUser=tblUser)
    

    
# rota para cadastrar
@blueprint.route("/register-user", methods=["GET", "POST"])
def registerUser():
    # verifica se o usuario esta logado
    if "user_id" not in session:

        # retorna uma mensagens ao usuario
        flash("Para acessar o software faça login...", "warning")

        # redereciona o usuario para o index
        return redirect(url_for("user_authentication.login"))
    else:

        # verifica se as informações foram enviadas de um formulário
        if request.method == "POST":

            # Abre conexão com banco
            connection = Session()

            # recupera os dados enviados pelo formulario html
            fNome = request.form["nome"]
            fCpf = request.form["cpf"]
            fNascimento = datetime.strptime(request.form["nascimento"], "%Y-%m-%d").date()# convertendo string de data (yyyy-dd-mm)
            fEndereco = request.form["endereco"]
            fTefefone = request.form["telefone"]
            fEmail = request.form["email"]
            fSenha = request.form["senha"]
            fPerfil = request.form["perfil"]

            # verifica se o usuario ja existe no banco de dados
            tblUser = connection.query(Usuario).filter_by(cpf=fCpf).first()

            if tblUser:

                # envia uma mensagem de erro
                flash("CPF já está cadastrado...", "danger")

                # fecha connexao com bando de dados
                connection.close()

                # redireciona para html de usuarios
                return redirect(url_for("user_management.listUsers"))
            
            else:

                # cria novo objeto
                novoUsuario = Usuario(
                    cpf=fCpf,
                    nome=fNome,
                    nascimento=fNascimento,
                    endereco=fEndereco,
                    telefone=fTefefone,
                    email=fEmail,
                    senha = generate_password_hash(fSenha, method="pbkdf2:sha256"),
                    perfil=fPerfil,

                )
                # adiciona o objeto no banco de dados
                connection.add(novoUsuario)

                # confirma a trnasação
                connection.commit()

                # fecha a conexao
                connection.close()

                # envia mensagem
                flash("CPF cadastrado com sucesso!", "success")

                # redireciona para html de livros
                return redirect(url_for("user_management.listUsers"))
            
        else:

            #  renderiza o html de cadastro de livro
            return render_template("userRegister.html")
        
        
# rota para edição de leitores/user
@blueprint.route("/usuarios/<string:cpf>/edit", methods=["POST", "GET"])
def editUser(cpf):

    # verifica se o usuario esta logado
    if "user_id" not in session:

        # retorna uma mensagens ao usuario
        flash("Para acessar o software faça login...", "warning")

        # redereciona o usuario para o index
        return redirect(url_for("user_authentication.login"))
    
    else:

        # verifica se as informações foram enviadas de um formulário
        if request.method == "POST":

            # Abre conexão com banco
            connection = Session()

            # busca objeto que será atualizado
            tblUser = connection.query(Usuario).filter_by(cpf=cpf).first()

            # recupera os dados enviados pelo formulario html
            tblUser.nome = request.form["nome"]
            tblUser.cpf = request.form["cpf"]
            tblUser.nascimento = datetime.strptime(request.form["nascimento"], "%Y-%m-%d").date()# convertendo string de data (yyyy-dd-mm)
            tblUser.endereco = request.form["endereco"]
            tblUser.telefone = request.form["telefone"]
            tblUser.email = request.form["email"]
            tblUser.senha = generate_password_hash(request.form["senha"], method="pbkdf2:sha256")
            tblUser.perfil = request.form["perfil"]

            # confirma a transação
            connection.commit()

            # fecha a conexao
            connection.close()

            # envia mensagem
            flash("Leitor alterado com sucesso!", "success")

            # redireciona para html de listagem de usuario
            return redirect(url_for("user_management.listUsers"))
        
        else:

            # Abre conexão com banco
            connection = Session()

            # busca objeto que será atualizado
            tblUser = connection.query(Usuario).filter_by(cpf=cpf).first()

            # fecha a conexao
            connection.close()

            # renderiza o html de edição de livro
            return render_template("userEdit.html", cUser=tblUser)
        

# rota para exclusao logica de usuarios
@blueprint.route("/usurario/<string:cpf>/delete", methods=["POST"])
def deleteUser(cpf):

    # verifica se o usuario esta logado
    if "user_id" not in session:

        # retorna uma mensagens ao usuario
        flash("Para acessar o software faça login...", "warning")

        # redereciona o usuario para o index
        return redirect(url_for("user_authentication.login"))
    
    else:

        # abre conexao com bd
        connection = Session()

        # busca o objeto que será excluido logicamente
        tblUser = connection.query(Usuario).filter_by(cpf=cpf).first()

        # define a exclusao logica
        tblUser.ativo = False

        # confirma a transação
        connection.commit()

        # fecha a conexao
        connection.close()

        # envia mensagem
        flash("Livro excluido com sucesso!", "success")

        # redireciona para html de livros
        return redirect(url_for("user_management.listUsers"))