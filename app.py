from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Olá, Flask no GitHub!'

@app.route('/buscador')
def buscar():
    return 'Aqui é um buscador'

if __name__ == '__main__':
    app.run(debug=True)
