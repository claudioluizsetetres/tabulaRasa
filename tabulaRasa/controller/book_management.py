# importa os modulos do Flask
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

# importa o modulo do sql alchemy que cria conexao banco de dados
from sqlalchemy.orm import sessionmaker

# importa as classes do banco de dados
from models.database import engine, Livro

# cria uma instancia do blueprint
blueprint = Blueprint("book_management", __name__)

# cria uma sessão do back-end com banco de dados
Session = sessionmaker(bind=engine)

# rota para listar livros
@blueprint.route("/books")
def list_books():

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
        livros = Connection.query(Livro).filter_by(ativo=True).order_by(Livro.titulo).all()

        # fecha conexao bd
        Connection.close()

        # renderiza o html do listagem de cadastro de livros
        return render_template("bookList.html", livros=livros)
    

# rota para cadastrar
@blueprint.route("/register-book", methods=["GET", "POST"])
def register_book():
    
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
            isbn = request.form["isbn"]
            titulo = request.form["titulo"]
            autor = request.form["autor"]
            editora = request.form["editora"]
            edicao = request.form["edicao"]
            volume = request.form["volume"]
            genero = request.form["genero"]
            paginas = request.form["paginas"]
            publicacao = request.form["publicacao"]
            exemplares = request.form["exemplares"]

            # verifica se o livro ja existe no banco de dados
            exite = connection.query(Livro).filter_by(isbn=isbn).first()

            if exite:

                # envia uma mensagem de erro
                flash("O ISBN do livro já está cadastrado...", "danger")

                # fecha connexao com bando de dados
                connection.close()

                # redireciona para html de livros
                return redirect(url_for("book_management.list_books"))
            
            else:

                # cria novo objeto
                novoLivro = Livro(
                    isbn=isbn,
                    titulo=titulo,
                    autor=autor,
                    editora=editora,
                    edicao=edicao,
                    volume=int(volume),
                    genero_literario=genero,
                    numero_paginas=int(paginas),
                    ano_publicacao=int(publicacao),
                    exemplares=int(exemplares),

                )
                # adiciona o objeto no banco de dados
                connection.add(novoLivro)

                # confirma a trnasação
                connection.commit()

                # fecha a conexao
                connection.close()

                # envia mensagem
                flash("Livro cadastrado com sucesso!", "success")

                # redireciona para html de livros
                return redirect(url_for("book_management.list_books"))
            
        else:

            #  renderiza o html de cadastro de livro
            return render_template("bookRegister.html")
        

# rota para atualização do cadastro de livro
@blueprint.route("/books/<string:isbn>/edit", methods=["POST", "GET"])
def edit_book(isbn):

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
            livro = connection.query(Livro).filter_by(isbn=isbn).first()

            # recupera os dados enviados pelo formulario html
            livro.isbn = request.form["isbn"]
            livro.titulo = request.form["titulo"]
            livro.autor = request.form["autor"]
            livro.editora = request.form["editora"]
            livro.edicao = request.form["edicao"]
            livro.volume = int(request.form["volume"])
            livro.genero_literario = request.form["genero"]
            livro.numero_paginas = int(request.form["paginas"])
            livro.ano_publicacao = int(request.form["publicacao"])
            livro.exemplares = int(request.form["exemplares"])

            # confirma a transação
            connection.commit()

            # fecha a conexao
            connection.close()

            # envia mensagem
            flash("Livro alterado com sucesso!", "success")

            # redireciona para html de livros
            return redirect(url_for("book_management.list_books"))
        
        else:

            # Abre conexão com banco
            connection = Session()

            # busca objeto que será atualizado
            livro = connection.query(Livro).filter_by(isbn=isbn).first()

            # fecha a conexao
            connection.close()

            # renderiza o html de edição de livro
            return render_template("bookEdit.html", livro=livro)


            
# rota para exclusao logica do livro
@blueprint.route("/books/<string:isbn>/delete", methods=["POST"])
def delete_book(isbn):

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
        livro = connection.query(Livro).filter_by(isbn=isbn).first()

        # define a exclusao logica
        livro.ativo = False

        # confirma a transação
        connection.commit()

        # fecha a conexao
        connection.close()

        # envia mensagem
        flash("Livro excluido com sucesso!", "success")

        # redireciona para html de livros
        return redirect(url_for("book_management.list_books"))