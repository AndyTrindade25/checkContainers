from flask import Flask

app = Flask(__name__)

@app.route('/webhook/<int:valor>', methods=['GET'])
def webhook(valor):
    resultado = f'{valor}'
    return resultado

if __name__ == '__main__':
    app.run(debug=True)
