import json
import logging
import requests
import random

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Lista de CEPs válidos para simular chamadas reais
CEPS_VALIDOS = [
    "01001000",  # SP
    "30140071",  # BH
    "70040900",  # Brasília
    "80010000",  # Curitiba
    "59010020",  # Natal
]

def lambda_handler(event, context):
    cep = random.choice(CEPS_VALIDOS)
    url = f"https://viacep.com.br/ws/{cep}/json/"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        if "erro" in data:
            logger.warning(json.dumps({
                "log_type": "cep_invalido",
                "cep": cep,
                "mensagem": "CEP não encontrado"
            }))
        else:
            logger.info(json.dumps({
                "log_type": "consulta_cep",
                "cep": cep,
                "localidade": data.get("localidade"),
                "uf": data.get("uf"),
                "bairro": data.get("bairro"),
                "logradouro": data.get("logradouro")
            }))

        return {
            "statusCode": 200,
            "body": json.dumps(data)
        }

    except Exception as e:
        logger.error(json.dumps({
            "log_type": "erro",
            "mensagem": str(e),
            "cep": cep
        }), exc_info=True)

        return {
            "statusCode": 500,
            "body": json.dumps({"erro": str(e)})
        }