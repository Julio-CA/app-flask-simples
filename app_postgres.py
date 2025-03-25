from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from send_email import send_email
import os


app = Flask(__name__)

# Configuração do banco de dados
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_PORT=os.environ.get('DB_PORT')

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializa o SQLAlchemy
db = SQLAlchemy(app)

# Cria objeto da tabela
class Heigh(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    altura = db.Column(db.Integer, nullable=False)

    def __init__(self, email, altura):
        self.email = email
        self.altura = altura

# Rota para criar a tabela
@app.route("/criar_tabela")
def criar_tabela():
    db.create_all()
    return "Tabela 'heigh' criada com sucesso!"

# Rota para solicitar dados de usuário
@app.route('/')
def index():
    return render_template('index.html')

# Rota de adicionar um usuário
@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        # Recebe os dados do formulário
        email = request.form['email_name']
        height = request.form['height_name']
        # Verifica se o email já está cadastrado
        if db.session.query(Heigh).filter(Heigh.email == email).count() == 0:
            # Adiciona o novo usuário
            novo = Heigh(email, height)
            db.session.add(novo) 
            db.session.commit()
            # Calcula a média de altura
            avarege_height = round(db.session.query(func.avg(Heigh.altura)).scalar(),1)
            # Envia email
            try:
                send_email(email, height, avarege_height)
            except:
                print("Erro ao enviar email")
            return render_template('success.html')   
        else:
            return render_template('index.html', text="Email já cadastrado. Tente outro.") 

    
if __name__ == '__main__':
    app.run(debug=True)
