from flask import Flask, jsonify

app = Flask(__name__)

# Rota 1: A mensagem de boas-vindas
@app.route('/')
def home():
    return jsonify({"mensagem": "Minha API está no ar na internet!"})

# Rota 2: O nosso Back-end (A API pura)
@app.route('/produto/<codigo>')
def consultar_produto(codigo):
    estoque = {"101": {"nome": "Guarda-sol", "preco": 85.00}}
    if codigo in estoque:
        return jsonify(estoque[codigo])
    return jsonify({"erro": "Produto não encontrado"}), 404

# Rota 3: O nosso Front-end (A Interface Gráfica)
@app.route('/loja')
def interface_loja():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Minha Loja de Praia</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-align: center; background-color: #e0f7fa; padding-top: 50px; }
            .caixa { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: inline-block; }
            input { padding: 10px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px; width: 200px; }
            button { padding: 10px 20px; font-size: 16px; background-color: #00796b; color: white; border: none; border-radius: 5px; cursor: pointer; margin-left: 10px; transition: 0.3s; }
            button:hover { background-color: #004d40; }
            #resultado { margin-top: 20px; font-size: 20px; font-weight: bold; color: #333; }
        </style>
    </head>
    <body>
        <div class="caixa">
            <h2>Consulta de Produtos 🏖️</h2>
            <p>Digite o código do produto (tente 101):</p>
            
            <input type="text" id="codigoInput" placeholder="Ex: 101">
            <button onclick="buscarProduto()">Buscar na API</button>
            
            <div id="resultado"></div>
        </div>

        <script>
            function buscarProduto() {
                // 1. Pega o número que o usuário digitou na caixinha
                let codigo = document.getElementById('codigoInput').value;
                let areaResultado = document.getElementById('resultado');
                
                areaResultado.innerHTML = "Buscando...";
                
                // 2. O Front-end (Javascript) faz o pedido para a sua API
                fetch('/produto/' + codigo)
                    .then(resposta => resposta.json()) // 3. Recebe o JSON
                    .then(dados => {
                        // 4. Monta a tela dependendo da resposta
                        if(dados.erro) {
                            areaResultado.innerHTML = "❌ " + dados.erro;
                            areaResultado.style.color = "red";
                        } else {
                            areaResultado.innerHTML = "✅ " + dados.nome + " - R$ " + dados.preco.toFixed(2);
                            areaResultado.style.color = "green";
                        }
                    })
                    .catch(erro => {
                        areaResultado.innerHTML = "Erro ao comunicar com a API!";
                        areaResultado.style.color = "red";
                    });
            }
        </script>
    </body>
    </html>
    """