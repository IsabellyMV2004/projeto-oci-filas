
import json

from config import QUEUE_ID, MESSAGES_ENDPOINT, API_VERSION
from oci_http_request import executar_requisicao


def publicar_mensagem(email, mensagem):
    """
    Publica uma mensagem normalmente na fila.
    """

    url = (
        f"{MESSAGES_ENDPOINT}/"
        f"{API_VERSION}/queues/{QUEUE_ID}/messages"
    )

    # Os dados são convertidos para JSON antes de serem
    # enviados no conteúdo da mensagem.
    conteudo = json.dumps({
        "email": email,
        "msg": mensagem
    }, ensure_ascii=False)

    dados = {
        "messages": [
            {
                "content": conteudo
            }
        ]
    }

    return executar_requisicao(
        metodo="POST",
        url=url,
        dados=dados
    )


def publicar_mensagem_canal(email, mensagem):
    """
    Publica uma mensagem associada ao canal canal1.
    """

    url = (
        f"{MESSAGES_ENDPOINT}/"
        f"{API_VERSION}/queues/{QUEUE_ID}/messages"
    )

    conteudo = json.dumps({
        "email": email,
        "msg": mensagem
    }, ensure_ascii=False)

    dados = {
        "messages": [
            {
                "content": conteudo,
                "metadata": {
                    "channelId": "canal1"
                }
            }
        ]
    }

    return executar_requisicao(
        metodo="POST",
        url=url,
        dados=dados
    )
