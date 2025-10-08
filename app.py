# importa o modulo do back-end que configura a aplicação da web
from controller import create_application

# CRIA UMA INSTÂNCIA DA APLICAÇÃO DA WEB
# CORREÇÃO: Renomeado para 'app' para compatibilidade com o Gunicorn
app = create_application()

# verifica se esta executando o arquivo de gatilho run.py
if __name__=="__main__":
    
    # inicia o servidor local da aplicação da web em modo de depuração
    app.run(debug=True)