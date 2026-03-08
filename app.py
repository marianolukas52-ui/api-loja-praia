from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Rota 1: A raiz da nossa API
@app.route('/')
def home():
    return jsonify({"mensagem": "API de Busca de CEP está no ar!"})

# Rota 2: O Back-end - Onde sua API conversa com a API do ViaCEP
@app.route('/cep/<numero_cep>')
def consultar_cep(numero_cep):
    # Tiramos o tracinho caso o usuário digite 11704-080
    cep_limpo = numero_cep.replace("-", "").strip()
    
    # Fazemos o pedido oficial para o sistema dos Correios/ViaCEP
    url = f"https://viacep.com.br/ws/{cep_limpo}/json/"
    resposta = requests.get(url)
    
    # Se a comunicação deu certo:
    if resposta.status_code == 200:
        dados = resposta.json()
        if "erro" in dados:
            return jsonify({"erro": "CEP não encontrado!"}), 404
        return jsonify(dados) # Devolvemos os dados para o nosso Front-end
    else:
        return jsonify({"erro": "Formato de CEP inválido!"}), 400

# Rota 3: O Front-end - A sua nova Interface Gráfica
@app.route('/busca')
def interface_busca():
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Buscador de CEP</title>
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f3f4f6; display: flex; justify-content: center; padding-top: 80px; margin: 0; }
            .cartao { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
            h2 { color: #1f2937; margin-top: 0; margin-bottom: 5px; font-size: 26px; }
            p { color: #6b7280; margin-bottom: 25px; font-size: 15px; }
            input { padding: 14px; font-size: 18px; border: 2px solid #e5e7eb; border-radius: 10px; width: 80%; margin-bottom: 20px; text-align: center; outline: none; transition: border 0.3s; }
            input:focus { border-color: #3b82f6; }
            button { padding: 14px 20px; font-size: 16px; background-color: #3b82f6; color: white; border: none; border-radius: 10px; cursor: pointer; width: 90%; font-weight: bold; transition: background-color 0.3s; box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3); }
            button:hover { background-color: #2563eb; }
            #resultado { margin-top: 25px; font-size: 16px; color: #374151; text-align: left; background: #f9fafb; padding: 20px; border-radius: 12px; border: 1px solid #e5e7eb; display: none; line-height: 1.6; }
            .erro { color: #ef4444; font-weight: bold; text-align: center; }
            strong { color: #111827; }
        </style>
    </head>
    <body>
        <div class="cartao">
            <h2>Buscador de Endereços 📍</h2>
            <p>Descubra a rua e o bairro de qualquer lugar</p>
            
            <input type="text" id="cepInput" placeholder="Ex: 11704-080" maxlength="9">
            <br>
            <button onclick="buscarCEP()">Pesquisar CEP</button>
            
            <div id="resultado"></div>
        </div>

        <script>
            function buscarCEP() {
                let cep = document.getElementById('cepInput').value;
                let areaResultado = document.getElementById('resultado');
                
                if(!cep) {
                    alert("Por favor, digite um CEP!");
                    return;
                }

                areaResultado.style.display = "block";
                areaResultado.innerHTML = "<div style='text-align:center;'>Buscando no satélite... 🛰️</div>";
                
                // O Javascript chama a SUA API na rota nova /cep/
                fetch('/cep/' + cep)
                    .then(resposta => resposta.json())
                    .then(dados => {
                        if(dados.erro) {
                            areaResultado.innerHTML = "<div class='erro'>❌ " + dados.erro + "</div>";
                        } else {
                            // Monta o visual com os dados que vieram lá do ViaCEP
                            areaResultado.innerHTML = `
                                <strong>Rua:</strong> ${dados.logradouro || 'Não informado'}<br>
                                <strong>Bairro:</strong> ${dados.bairro || 'Não informado'}<br>
                                <strong>Cidade:</strong> ${dados.localidade} - ${dados.uf}<br>
                                <strong>CEP:</strong> ${dados.cep}
                            `;
                        }
                    })
                    .catch(erro => {
                        areaResultado.innerHTML = "<div class='erro'>Erro ao comunicar com a API!</div>";
                    });
            }
        </script>
    </body>
    </html>
    """
if __name__ == '__main__':
    import os
    # Pega a porta 8080 do OpenShift
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
