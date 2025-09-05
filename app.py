from flask import Flask
from config.database import criar_tabelas

app = Flask(__name__)

@app.route("/")
def home():
    return "Registro de Produtividade - Versão Expandida 🚀"

if __name__ == "__main__":
    # Cria as tabelas no banco antes de rodar a aplicação
    criar_tabelas()
    app.run(debug=True)
