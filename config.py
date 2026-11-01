
import os

# Identificação da fila na Oracle Cloud.
QUEUE_ID = os.getenv(
    "QUEUE_ID",
    "ocid1.queue.oc1.phx.amaaaaaa62b2piaa4xaxgqaovrm4ny5u45obgfxtip73rj2fz6gajzzii6ba"
)

# Endpoint de mensagens disponibilizado pela OCI.
MESSAGES_ENDPOINT = os.getenv(
    "MESSAGES_ENDPOINT",
    "https://cell-1.queue.messaging.us-phoenix-1.oci.oraclecloud.com"
)

# Versão da API de filas da OCI.
API_VERSION = "20210201"

# Tempo, em segundos, para uma mensagem voltar a ficar
# disponível caso ocorra um erro durante o processamento.
VISIBILITY_TIMEOUT = 30

# Quantidade máxima de mensagens buscadas por vez.
MESSAGE_LIMIT = 10

# Configurações opcionais para envio de e-mail.
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USER)
