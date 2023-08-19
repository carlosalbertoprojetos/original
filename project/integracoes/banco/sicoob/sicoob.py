import requests
import contextlib
import OpenSSL.crypto
import os
import ssl
import tempfile

url_login = 'https://auth.sicoob.com.br/auth/realms/cooperado/protocol/openid-connect/token'
url_extrato = 'https://api.sicoob.com.br/conta-corrente/v2/extrato/%s/%s'
url_saldo = 'https://api.sicoob.com.br/conta-corrente/v2/saldo'
print(url_extrato % ('03', '2023'))

headers = {
    'Content-Type':'application/x-www-form-urlencoded',
    'grant_type':'',
    'scope':''
}





@contextlib.contextmanager
def pfx_to_pem(pfx_path, pfx_password):
    ''' Decrypts the .pfx file to be used with requests. '''
    with open('teste.pem','w') as t_pem:
        f_pem = open(t_pem.name, 'wb')
        pfx = open('eder.pfx', 'rb').read()
        p12 = OpenSSL.crypto.load_pkcs12(pfx, pfx_password)
        f_pem.write(OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, p12.get_privatekey()))
        f_pem.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, p12.get_certificate()))
        ca = p12.get_ca_certificates()
        if ca is not None:
            for cert in ca:
                f_pem.write(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM, cert))
        f_pem.close()
        yield t_pem.name
cert='./eder.pfx'
with pfx_to_pem(cert, '1234') as cert:
    data = {
        'client_id':'8cc4ae46-3c60-4ef3-b3cc-b212605ee195',
        'grant_type':'client_credentials',
        'scope':'openid cco_extrato cco_saldo'
    }
    x = requests.post(url_login, headers=headers, cert=cert, data=data)
    print(x.status_code)
    headers = {
        'Content-Type': 'application/json',
        'Authorization':'Bearer ' + x.json()['id_token'],
        'Accept': 'application/json',
        'x-sicoob-clientid':'8cc4ae46-3c60-4ef3-b3cc-b212605ee195',
    }
    data = {
        'client_id':'8cc4ae46-3c60-4ef3-b3cc-b212605ee195',
        'grant_type':'client_credentials',
        'scope':'cco_extrato cco_saldo'
    }
    #y = requests.get(url_extrato % ('03', '2023'), headers=headers, cert=cert)
    
    y = requests.get(url_saldo , headers=headers, cert=cert)
    print(y.text)