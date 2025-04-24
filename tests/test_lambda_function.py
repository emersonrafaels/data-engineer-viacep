import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

from pytest import raises

from lambda_function import consultar_cep, lambda_handler

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def test_consultar_cep_sucesso():
    """Teste para verificar se a função consultar_cep retorna os dados corretamente."""
    cep = "01001000"
    mock_response = {
        "cep": "01001-000",
        "logradouro": "Praça da Sé",
        "bairro": "Sé",
        "localidade": "São Paulo",
        "uf": "SP",
    }

    with patch("lambda_function.requests.get") as mock_get:
        # Configura o mock para retornar uma resposta de sucesso
        mock_get.return_value = MagicMock(status_code=200, json=lambda: mock_response)

        # Chama a função
        response = consultar_cep(cep)

        # Verifica se a resposta está correta
        if response != mock_response:
            raise AssertionError("Resposta não corresponde ao esperado.")
        mock_get.assert_called_once_with(
            f"https://viacep.com.br/ws/{cep}/json/", timeout=5
        )


def test_consultar_cep_erro_http():
    """Teste para verificar se a função consultar_cep lida com erros HTTP."""
    cep = "01001000"

    with patch("lambda_function.requests.get") as mock_get:
        # Configura o mock para levantar uma exceção HTTP
        mock_get.side_effect = ConnectionError("Erro na requisição")

        # Verifica se a exceção é levantada
        with raises(ConnectionError, match="Erro na requisição"):
            consultar_cep(cep)


def test_lambda_handler_sucesso():
    """Teste para verificar o comportamento do lambda_handler em caso de sucesso."""

    mock_response = {
        "cep": "01001-000",
        "logradouro": "Praça da Sé",
        "bairro": "Sé",
        "localidade": "São Paulo",
        "uf": "SP",
    }

    with patch("lambda_function.consultar_cep", return_value=mock_response):
        # Chama o lambda_handler
        response = lambda_handler({}, {})

        # Verifica se o statusCode e o body estão corretos
        if response["statusCode"] != 200:
            raise AssertionError("StatusCode não corresponde ao esperado.")
        if json.loads(response["body"]) != mock_response:
            raise AssertionError("Body não corresponde ao esperado.")


def test_lambda_handler_cep_invalido():
    """Teste para verificar o comportamento do lambda_handler com um CEP inválido."""

    mock_response = {"erro": True}

    with patch("lambda_function.consultar_cep", return_value=mock_response):
        # Chama o lambda_handler
        response = lambda_handler({}, {})

        # Verifica se o statusCode e o body estão corretos
        if response["statusCode"] != 200:
            raise AssertionError("StatusCode não corresponde ao esperado.")
        if json.loads(response["body"]) != mock_response:
            raise AssertionError("Body não corresponde ao esperado.")


def test_lambda_handler_erro():
    """Teste para verificar o comportamento do lambda_handler em caso de erro."""

    with patch(
        "lambda_function.consultar_cep", side_effect=ValueError("Erro inesperado")
    ):
        # Chama o lambda_handler
        response = lambda_handler({}, {})

        # Verifica se o statusCode e o body estão corretos
        if response["statusCode"] != 500:
            raise AssertionError("StatusCode não corresponde ao esperado.")
        if json.loads(response["body"]) != {"erro": "Erro inesperado"}:
            raise AssertionError("Body não corresponde ao esperado.")
