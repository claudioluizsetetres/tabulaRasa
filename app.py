# importa o modulo do back-end que configra a aplicação da web
from controller import create_application

# cria uma instancia da aplicação da web
web_application = create_application()

# verifica se esta executando o arquivo de gatilho run.py
if __name__=="__main__":
    
    # inicia o servidor local da aplicação da web em modo de depuração
    web_application.run(debug=True)