from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func 
import os
from send_email import send_email

app = Flask(__name__)

# Caminho do banco SQLite
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'collector.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o SQLAlchemy
db = SQLAlchemy(app)

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
        email = request.form['email_name']
        height = request.form['height_name']
        if db.session.query(Heigh).filter(Heigh.email == email).count() == 0:
            novo = Heigh(email, height)
            db.session.add(novo) 
            db.session.commit()
            try:
                avarege_height = round(db.session.query(func.avg(Heigh.altura)).scalar(),1)
                send_email(email, height, avarege_height)
            except:
                print("Erro ao enviar email")
            return render_template('success.html')   
        else:
            return render_template('index.html', text="Email já cadastrado. Tente outro.") 

if __name__ == '__main__':
    app.run(debug=True)
