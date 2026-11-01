
import json
import smtplib

from email.mime.text import MIMEText
from urllib.parse import quote

from config import (
    QUEUE_ID,
    MESSAGES_ENDPOINT,
    API_VERSION,
    VISIBILITY_TIMEOUT,
    MESSAGE_LIMIT,
    SMTP_HOST,
    SMTP_PORT,
    SMTP_USER,
    SMTP_PASSWORD,
    EMAIL_FROM
)

from oci_http_request import executar_requisicao


def enviar_email(destinatario, mensagem):
    """
    Envia um e-mail utilizando SMTP.

    Se as configurações de e-mail não estiverem preenchidas,
    apenas simula o envio no terminal.
    """

    if not SMTP_USER or not SMTP_PASSWORD:
        print("Simulação de envio de e-mail:")
        print(f"Destinatário: {destinatario}")
        print(f"Mensagem: {mensagem}")

        return

    email = MIMEText(mensagem, "plain", "utf-8")
    email["Subject"] = "Mensagem recebida pela fila OCI"
    email["From"] = EMAIL_FROM
    email["To"] = destinatario

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as servidor:
        servidor.starttls()
        servidor.login(SMTP_USER, SMTP_PASSWORD)
        servidor.send_message(email)


def excluir_mensagem(receipt):
    """
    Exclui uma mensagem da fila após o processamento.
    """

    receipt_codificado = quote(receipt, safe="")

    url = (
        f"{MESSAGES_ENDPOINT}/"
        f"{API_VERSION}/queues/{QUEUE_ID}/messages/"
        f"{receipt_codificado}"
    )

    return executar_requisicao(
        metodo="DELETE",
        url=url
    )


def alterar_visibilidade(receipt):
    """
    Faz a mensagem ficar indisponível temporariamente,
    permitindo uma nova tentativa de processamento.
    """

    receipt_codificado = quote(receipt, safe="")

    url = (
        f"{MESSAGES_ENDPOINT}/"
        f"{API_VERSION}/queues/{QUEUE_ID}/messages/"
        f"{receipt_codificado}"
    )

    dados = {
        "visibilityInSeconds": VISIBILITY_TIMEOUT
    }

    return executar_requisicao(
        metodo="PUT",
        url=url,
        dados=dados
    )


def processar_mensagem(mensagem):
    """
    Processa uma mensagem recebida da fila.
    """

    # O conteúdo da mensagem está armazenado como JSON
    # dentro do campo content.
    conteudo = json.loads(mensagem["content"])

    destinatario = conteudo["email"]
    texto = conteudo["msg"]

    # Envia o e-mail ou realiza a simulação.
    enviar_email(destinatario, texto)


def consumir_mensagens(canal=None):
    """
    Busca e processa mensagens da fila.

    Se canal for informado, busca somente as mensagens
    associadas ao canal indicado.
    """

    url = (
        f"{MESSAGES_ENDPOINT}/"
        f"{API_VERSION}/queues/{QUEUE_ID}/messages"
    )

    parametros = {
        "limit": 1 if canal else MESSAGE_LIMIT
    }

    # Quando informado, o canal funciona como filtro.
    if canal:
        parametros["channelFilter"] = canal

    retorno = executar_requisicao(
        metodo="GET",
        url=url,
        parametros=parametros
    )

    mensagens = retorno.get("messages", [])
    resultados = []

    if not mensagens:
        return {
            "mensagem": "Nenhuma mensagem encontrada.",
            "resultados": []
        }

    for mensagem in mensagens:
        receipt = mensagem.get("receipt")

        try:
            # Primeiro processa a mensagem.
            processar_mensagem(mensagem)

            # Se o processamento funcionar, exclui a mensagem.
            excluir_mensagem(receipt)

            resultados.append({
                "status": "sucesso",
                "mensagem": "Mensagem processada e excluída da fila."
            })

        except Exception as erro:
            print(f"Erro ao processar mensagem: {erro}")

            # Se ocorrer um erro, a mensagem não é excluída.
            # Sua visibilidade é alterada para permitir
            # uma nova tentativa depois de 30 segundos.
            try:
                alterar_visibilidade(receipt)

                resultados.append({
                    "status": "erro",
                    "mensagem": (
                        "Falha no processamento. "
                        "Uma nova tentativa poderá ocorrer depois."
                    )
                })

            except Exception as erro_visibilidade:
                print(
                    "Erro ao alterar a visibilidade:",
                    erro_visibilidade
                )

                resultados.append({
                    "status": "erro",
                    "mensagem": (
                        "Falha no processamento e na alteração "
                        "da visibilidade da mensagem."
                    )
                })

    return {
        "mensagem": "Consumo finalizado.",
        "resultados": resultados
    }


def consumir_mensagens_canal():
    """
    Consome somente mensagens do canal canal1.
    """

    return consumir_mensagens(canal="canal1")
