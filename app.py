
from flask import Flask, render_template, request, jsonify

from produtor import (
    publicar_mensagem,
    publicar_mensagem_canal
)

from consumidor import (
    consumir_mensagens,
    consumir_mensagens_canal
)


app = Flask(__name__)


@app.route("/")
def inicio():
    """
    Exibe a página principal.
    """

    return render_template("index.html")


@app.route("/publicar", methods=["POST"])
def publicar():
    """
    Recebe os dados do formulário e publica uma mensagem.
    """

    email = request.form.get("email", "").strip()
    mensagem = request.form.get("msg", "").strip()

    if not email or not mensagem:
        return jsonify({
            "status": "erro",
            "mensagem": "Informe o e-mail e a mensagem."
        }), 400

    try:
        retorno = publicar_mensagem(email, mensagem)

        return jsonify({
            "status": "sucesso",
            "mensagem": "Mensagem publicada na fila com sucesso!",
            "retorno": retorno
        })

    except Exception as erro:
        return jsonify({
            "status": "erro",
            "mensagem": f"Erro ao publicar mensagem: {erro}"
        }), 500


@app.route("/publicarCanal", methods=["POST"])
def publicar_canal():
    """
    Publica uma mensagem no canal canal1.
    """

    email = request.form.get("email", "").strip()
    mensagem = request.form.get("msg", "").strip()

    if not email or not mensagem:
        return jsonify({
            "status": "erro",
            "mensagem": "Informe o e-mail e a mensagem."
        }), 400

    try:
        retorno = publicar_mensagem_canal(email, mensagem)

        return jsonify({
            "status": "sucesso",
            "mensagem": "Mensagem publicada no canal com sucesso!",
            "retorno": retorno
        })

    except Exception as erro:
        return jsonify({
            "status": "erro",
            "mensagem": f"Erro ao publicar mensagem: {erro}"
        }), 500


@app.route("/consumir", methods=["POST"])
def consumir():
    """
    Consome mensagens normalmente da fila.
    """

    try:
        retorno = consumir_mensagens()

        return jsonify({
            "status": "sucesso",
            "retorno": retorno
        })

    except Exception as erro:
        return jsonify({
            "status": "erro",
            "mensagem": f"Erro ao consumir mensagens: {erro}"
        }), 500


@app.route("/consumirCanal", methods=["POST"])
def consumir_canal():
    """
    Consome somente mensagens do canal canal1.
    """

    try:
        retorno = consumir_mensagens_canal()

        return jsonify({
            "status": "sucesso",
            "retorno": retorno
        })

    except Exception as erro:
        return jsonify({
            "status": "erro",
            "mensagem": f"Erro ao consumir mensagens do canal: {erro}"
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=3000,
        debug=True
    )
