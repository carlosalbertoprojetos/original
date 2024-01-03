import json
import requests


def validarBoletoAPI():
    CLEINT_ID = "c4c6b6b6-dbba-41db-96b0-f23bd0a363f3"
    CLIENT_SECRET = "1e0ba37d-54b8-4008-b758-b420564d3183"
    url = "https://sts.itau.com.br/api/oauth/token"
    cert = ("c:/Certificado.crt", "c:/ARQUIVO_CHAVE_PRIVADA.key")
    payload = "grant_type=client_credentials&{CLEINT_ID}&client_secret={CLIENT_SECRET}"
    headers = {
        "x-itau-flowID": "1",
        "x-itau-correlationID": "2",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = requests.post(url=url, data=payload, headers=headers, cert=cert)

    if 200 != response.status_code:
        print(response.headers)

    print(response.json())


validarBoletoAPI()
