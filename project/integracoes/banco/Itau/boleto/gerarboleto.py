import unittest
import requests


def geraboleto():
    """Gera o token"""
    client_id = "82e96e5c-7132-3add-8a6f-5dbd9d60d500"
    client_secret = "8183c235-61a0-470a-8584-aa2ccbca2dab"
    client = {"client_id": client_id, "client_secret": client_secret}
    url = "https://devportal.itau.com.br/api/jwt"
    headers = {"content-Type": "application/json"}
    request_token = requests.post(
        url,
        client,
        headers,
    )
    token = request_token.json()
    headers = {"x-sandbox-token": token["access_token"]}

    """ Gera os dados do boleto """
    boleto_data = requests.get(
        "https://devportal.itau.com.br/sandboxapi/itau-ep9-gtw-cash-management-ext-v2/v2/boletos?id_beneficiario=150000052061",
        headers=headers,
    )

    # print(boleto_data.text)
    return boleto_data.text
