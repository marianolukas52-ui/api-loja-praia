from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"mensagem": "Minha API está no ar na internet!"})

@app.route('/produto/<codigo>')
def consultar_produto(codigo):
    estoque = {"101": {"nome": "Guarda-sol", "preco": 85.00}}
    if codigo in estoque:
        return jsonify(estoque[codigo])
    return jsonify({"erro": "Produto não encontrado"}), 404

# Nota: Não precisamos do app.run() aqui para o deploy profissional!