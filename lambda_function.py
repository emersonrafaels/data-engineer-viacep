import json
import logging
import secrets  # Substituir random por secrets para maior segurança

import requests

# Configuração do logger para registrar logs em diferentes níveis (INFO, WARNING, ERROR)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Lista de CEPs válidos para simular chamadas reais
CEPS_VALIDOS = [
    "01001000",  # São Paulo
    "30140071",  # Belo Horizonte
    "70040900",  # Brasília
    "80010000",  # Curitiba
    "59010020",  # Natal
]


def consultar_cep(cep):
    """
    Realiza a consulta de um CEP na API ViaCEP.

    Args:
        cep (str): O CEP a ser consultado.

    Returns:
        dict: Os dados retornados pela API em formato JSON.
    """
    url = f"https://viacep.com.br/ws/{cep}/json/"
    try:
        # Realiza a requisição GET para a API ViaCEP
        response = requests.get(url, timeout=5)
        # Levanta uma exceção para códigos de status HTTP de error
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # Captura erros relacionados à requisição HTTP
        logger.error(
            json.dumps({"log_type": "erro_requisicao", "mensagem": str(e), "cep": cep}),
            exc_info=True,
        )
        raise e


def lambda_handler(event, context):
    """
    Função Lambda principal que simula a consulta de um CEP e retorna os dados.

    Args:
        event (dict): Dados de entrada do evento (não utilizado neste exemplo).
        context (object): Contexto de execução da função
        Lambda (não utilizado neste exemplo).

    Returns:
        dict: Resposta HTTP com os dados do CEP ou mensagem de erro.
    """
    # Seleciona aleatoriamente um CEP da lista de CEPs válidos
    cep = secrets.choice(CEPS_VALIDOS)

    try:
        # Consulta o CEP utilizando a função consultar_cep
        data = consultar_cep(cep)

        # Verifica se o CEP é inválido (API retorna "erro" em caso de CEP inexistente)
        if "erro" in data:
            logger.warning(
                json.dumps(
                    {
                        "log_type": "cep_invalido",
                        "cep": cep,
                        "mensagem": "CEP não encontrado",
                    }
                )
            )
        else:
            # Loga os dados do CEP consultado
            logger.info(
                json.dumps(
                    {
                        "log_type": "consulta_cep",
                        "cep": cep,
                        "localidade": data.get("localidade"),
                        "uf": data.get("uf"),
                        "bairro": data.get("bairro"),
                        "logradouro": data.get("logradouro"),
                    }
                )
            )

        # Retorna os dados do CEP na resposta
        return {"statusCode": 200, "body": json.dumps(data)}

    except Exception as e:
        # Loga o erro e retorna uma mensagem de erro na resposta
        logger.error(
            json.dumps({"log_type": "erro", "mensagem": str(e), "cep": cep}),
            exc_info=True,
        )

        return {"statusCode": 500, "body": json.dumps({"erro": str(e)})}
