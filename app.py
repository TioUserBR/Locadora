from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
ARQUIVO = "locadora.json"

# 🔹 Garante que o arquivo existe
if not os.path.exists(ARQUIVO):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)

# 🔹 POST - adiciona locação
@app.route("/locadora", methods=["POST"])
def adicionar_locacao():
    try:
        dados = request.get_json()

        with open(ARQUIVO, "r", encoding="utf-8") as f:
            registros = json.load(f)

        registros.append(dados)

        with open(ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(registros, f, ensure_ascii=False, indent=4)

        return jsonify({"status": "sucesso", "mensagem": "Registro adicionado!"}), 200

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400

# 🔹 GET - lista locações
@app.route("/locadora", methods=["GET"])
def listar_locacoes():
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        registros = json.load(f)
    return jsonify(registros)

# 🔹 DELETE - remove registro específico por Nome + Data + Hora
@app.route("/locadora", methods=["DELETE"])
def deletar_registro():
    try:
        dados = request.get_json()
        nome = dados.get("Nome")
        data = dados.get("Data")
        hora = dados.get("Hora")

        if not nome or not data or not hora:
            return jsonify({"status": "erro", "mensagem": "Informe Nome, Data e Hora para deletar"}), 400

        with open(ARQUIVO, "r", encoding="utf-8") as f:
            registros = json.load(f)

        # Remove apenas o registro exato
        novos_registros = [r for r in registros if not (
            r.get("Nome") == nome and r.get("Data") == data and r.get("Hora") == hora
        )]

        if len(novos_registros) == len(registros):
            return jsonify({"status": "erro", "mensagem": "Nenhum registro encontrado com esses dados"}), 404

        with open(ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(novos_registros, f, ensure_ascii=False, indent=4)

        return jsonify({"status": "sucesso", "mensagem": f"Registro de {nome} em {data} {hora} apagado!"}), 200

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
          
