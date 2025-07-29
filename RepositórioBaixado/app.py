from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)


# Configurar o banco de dados SQLite

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///exemplo.db')  # Fallback para SQLite local
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar o SQLAlchemy
db = SQLAlchemy(app)

#Definir um modelo (tabela no banco de dados)
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False) #Email para login
    senha = db.Column(db.String(80), nullable=False)#Senha para login

    def __repr__(self):
        return f'<Usuario {self.nome}>'
    
# Criar o banco de dados
with app.app_context():
    db.create_all()


# Rota para exibir o formulário de login e processar o login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        if email and senha:
            usuario = Usuario.query.filter_by(email=email).first()
            if usuario and usuario.senha == senha:
                return render_template('adicionar_usuario.html', nome=usuario.nome)
            mensagem = 'Email ou senha incorretos.'
            return render_template('login.html', mensagem=mensagem), 401
        mensagem = 'Erro: Preencha todos os campos.'
        return render_template('login.html', mensagem=mensagem), 400
    return render_template('login.html', mensagem=None)
    

    

# Rota para adicionar um novo usuário
@app.route('/adicionar_usuario', methods=['GET'])
def adicionar_usuario():
    return render_template('adicionar_usuario.html')
         
    

# Rota para adicionar um novo usuário
@app.route('/cadastro', methods=[ 'GET','POST']) 
def cadastro():
    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    if nome and email and senha:
        try:
            novo_usuario = Usuario(nome=nome, email=email, senha=senha)
            db.session.add(novo_usuario)
            db.session.commit()
            return render_template('cadastro.html', mostrar_modal=True, nome=nome)
        except Exception as e:
            db.session.rollback()
            mensagem = f'Erro ao cadastrar: {str(e)} (Email já existe!)'
            return render_template('cadastro.html', mensagem=mensagem, mostrar_modal=False), 400
    mensagem = 'Erro: Preencha todos os campos.'
    return render_template('cadastro.html'), 400



# Rota simples para testar
@app.route('/')
def index():
    return render_template('index.html')
    


if __name__ == '__main__':
    app.run(debug=True)

#https://www.youtube.com/shorts/5PMCgp0Y4fc?feature=share
