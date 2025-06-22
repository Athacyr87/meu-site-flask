from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/buscador')
def buscar():
    return 'Aqui é um buscador'

if __name__ == '__main__':
    app.run(debug=True)
