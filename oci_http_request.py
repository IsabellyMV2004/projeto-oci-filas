
import oci
import requests


# Carrega as informações de autenticação do arquivo
# ~/.oci/config, utilizando o perfil DEFAULT.
config = oci.config.from_file(
    file_location="~/.oci/config",
    profile_name="DEFAULT"
)

# Cria o assinador para autenticar as requisições na OCI.
signer = oci.signer.Signer(
    tenancy=config["tenancy"],
    user=config["user"],
    fingerprint=config["fingerprint"],
    private_key_file_location=config["key_file"],
    pass_phrase=config.get("pass_phrase")
)


def executar_requisicao(metodo, url, dados=None, parametros=None):
    """
    Executa uma requisição HTTP autenticada na Oracle Cloud.

    metodo: GET, POST, PUT ou DELETE.
    url: endereço da API.
    dados: conteúdo enviado no corpo da requisição.
    parametros: parâmetros enviados na URL.
    """

    resposta = requests.request(
        method=metodo,
        url=url,
        json=dados,
        params=parametros,
        auth=signer,
        timeout=30
    )

    # Gera uma exceção caso a OCI retorne um erro HTTP.
    resposta.raise_for_status()

    # Algumas operações, como DELETE, podem não retornar conteúdo.
    if resposta.content:
        return resposta.json()

    return None
