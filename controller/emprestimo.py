# importa os modulos do Flask
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

# importa o modulo do sql alchemy que cria conexao banco de dados
from sqlalchemy.orm import sessionmaker, joinedload

# importa as classes do banco de dados
from models.database import engine, Usuario, Livro, Emprestimo

# importa data
from datetime import date, datetime, timedelta

# cria uma instancia do blueprint
blueprint = Blueprint("emprestimo", __name__)

# cria uma sessão do back-end com banco de dados
Session = sessionmaker(bind=engine)

# rota para emprestimos de livros
@blueprint.route("/emprestimo")
def emprestimo():

    # verifica se o usuario esta logado
    if "user_id" not in session:

        # retorna uma mensagens ao usuario
        flash("Para acessar o software faça login...", "warning")

        # redereciona o usuario para o index
        return redirect(url_for("user_authentication.login"))
    
    else:

        # pegando a data de hoje
        emprestimoDt = date.today() 

        # data de retorno de 15 dias
        devolucaoDt = emprestimoDt + timedelta(days=15)

        # abre a conexao com bd
        Connection = Session()

        # busca todos os usuarios cadaastrados
        dbUser = Connection.query(Usuario).with_entities(Usuario.id,Usuario.nome).filter(Usuario.ativo == True, Usuario.perfil !="Administrador").order_by(Usuario.nome).all()

        # busca todos os livros cadaastrados
        dbLivros = Connection.query(Livro).with_entities(Livro.id,Livro.titulo).filter_by(ativo=True).order_by(Livro.titulo).all()

        # fecha conexao bd
        Connection.close()

        # renderiza o html emprestimo com as datas
        return render_template("bookRental.html",
                                dtEmprestimo = emprestimoDt, 
                                dtDevolucao = devolucaoDt,
                                dbUser = dbUser,
                                dbLivros = dbLivros
                                )
    

# rota para listagem de livros emprestados
@blueprint.route("/devolucao")
def listDevolucao():

    # verifica se o usuario esta logado
    if "user_id" not in session:

        # retorna uma mensagens ao usuario
        flash("Para acessar o software faça login...", "warning")

        # redereciona o usuario para o index
        return redirect(url_for("user_authentication.login"))
    
    else:
        # abre a conexao com bd
        connection = Session()

        # busca todos os emprestimo com status pendentes
        #tblEmprestimo = Connection.query(Emprestimo).filter(Emprestimo.ativo == True, Emprestimo.status == "Pendente").order_by(Emprestimo.data_devolucao).all()
        tblEmprestimo = (
            connection.query(Emprestimo)
            .options(joinedload(Emprestimo.usuario), joinedload(Emprestimo.livro))
            .filter(Emprestimo.ativo == True, Emprestimo.status == "Pendente")
            .order_by(Emprestimo.data_devolucao)
            .all()
            )


        # fecha conexao bd
        connection.close()

        # verifica se data de devolução é menor que hoje (para mudar a cor do texto)
        for vencimento in tblEmprestimo:
            vencimento.vencimento = vencimento.data_devolucao.date() <= date.today()

        # renderiza o html do listagem de emprestimos
        return render_template("bookRetorn.html", cEmprestimo=tblEmprestimo)



# registrar o emprestimo
@blueprint.route("/register-emprestimo", methods=["GET", "POST"])
def registerEmprestimo():
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
            idUser = request.form["usuario"]
            idLivro = request.form.getlist("fLivros[]")
            dtEmprestimo = datetime.strptime(request.form["dataEmprestimo"], "%Y-%m-%d").date()# convertendo string de data (yyyy-dd-mm) 
            dtDevolucao = datetime.strptime(request.form["dataDevolucao"], "%Y-%m-%d").date()# convertendo string de data (yyyy-dd-mm)

            # verifica a quantidade de livros selecionados e insere no banco de dados
            for livroId in idLivro:
                # cria um objeto
                novoEmprestimo = Emprestimo(
                    id_usuario = idUser,
                    id_livro = livroId,
                    data_emprestimo = dtEmprestimo,
                    data_devolucao = dtDevolucao,
                    status = "Pendente",
                )

                #inserir dados no banco de dados
                connection.add(novoEmprestimo)
                # confirma a trnasação
                connection.commit()

            # fecha a conexao
            connection.close()

            # envia mensagem
            flash("Emprestimo realizado com sucesso!", "success")

            # redireciona para html de livros
            return redirect(url_for("emprestimo.emprestimo"))



# rota para devolução de livros
@blueprint.route("/emprestimo/<string:id>/devolucao", methods=["POST"])
def devolver(id):

    # verifica se o usuario esta logado
    if "user_id" not in session:

        # retorna uma mensagens ao usuario
        flash("Para acessar o software faça login...", "warning")

        # redereciona o usuario para o index
        return redirect(url_for("user_authentication.login"))
    
    else:

        # abre conexao com bd
        connection = Session()

        # busca o objeto para mudar status para Liberado
        tblEmprestimo = connection.query(Emprestimo).filter_by(id=id).first()

        # define a liberação
        tblEmprestimo.status = "Liberado"

        # confirma a transação
        connection.commit()

        # fecha a conexao
        connection.close()

        # envia mensagem
        flash("Devolução concluida com sucesso!", "success")

        # redireciona para html de livros
        return redirect(url_for("emprestimo.listDevolucao"))


# rota para exclusao logica de emprestimos
@blueprint.route("/emprestimo/<string:id>/delete", methods=["POST"])
def deleteEmprestimo(id):

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
        tblEmprestimo = connection.query(Emprestimo).filter_by(id=id).first()

        # define a exclusao logica
        tblEmprestimo.ativo = False

        # confirma a transação
        connection.commit()

        # fecha a conexao
        connection.close()

        # envia mensagem
        flash("Empréstimo excluido com sucesso!", "success")

        # redireciona para html de livros
        return redirect(url_for("emprestimo.listDevolucao"))
