import json
import requests
from time import sleep
#url = 'https://cliente.viapajucara.com.br/rastrear/resultado?cnpj=51905769000190&tipo=remetente&notaFiscal=124'
#payload = {"nrIdentificacao":"51905769000190","tpDocumento":"NF","remDest":"R","idFilial":13532730,"nrDocumento":"260"}
#r = requests.post(url, data=json.dumps(payload))
#print(r)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def pega_dados_pajucara(danfe, cnpj=None, nf=None):
    #lista_ocorrencias = ['Entrega Realizada', 'Carta de mercadoria à disposição enviada', 'Ocorrência de entrega']a
    if 1:
        url = "https://ssw.inf.br/api/trackingdanfe"
        data = {"chave_nfe": danfe}
        headers = {"Content-Type": "application/json"}
        resposta = requests.post(url, headers=headers, data=json.dumps(data))
        if not resposta.json()['success']:
            if cnpj and nf:
                url = "https://ssw.inf.br/api/tracking"
                data = {'cnpj':cnpj, 'nro_nf': nf, 'senha':'ORIGINAL2023'}
                resposta = requests.post(url, headers=headers, data=json.dumps(data))
        if resposta.json()['success']:
          descricao = resposta.json()['documento']['tracking'][0]['descricao']
          previsao = resposta.json()['documento']['tracking'][0]['descricao'].find('Previsao de entrega')
          data_entrega = descricao[previsao+21:-1]
          situacao = ''
          return data_entrega, situacao
        return None, None

def pega_dados_pajucara_old(numero_nf, cnpj='51905769000190'):
    try:
        #lista_ocorrencias = ['Entrega Realizada', 'Carta de mercadoria à disposição enviada', 'Ocorrência de entrega']
        url = "https://cliente.viapajucara.com.br/rastrear/resultado?cnpj=%s&tipo=remetente&notaFiscal=%s" % (cnpj,numero_nf)
        driver = webdriver.Chrome()
        driver.get(url)
        #import pdb;pdb.set_trace()
        continua = True
        while continua:
            elementos = driver.find_elements(By.XPATH,"//h3")
            if elementos:
                continua = False
            sleep(1)
        sleep(3)

        #ve se tem nota fiscal
        h1s = driver.find_elements(By.XPATH,"//h1")
        for h1 in h1s:
            if h1.text == 'Nota fiscal não encontrada':
                return '', 'Nota fiscal não encontrada'


        posicao = driver.find_element(By.XPATH,"//div[@class = 'lf-player-container']")
        parent = posicao.find_element(By.XPATH,"./..");
        situacao = parent.text
        previsao = driver.find_elements(By.XPATH,"//h2")
        previsao = previsao[0].text
        previsao = previsao.replace('Previsto para chegar no dia ', '')
        driver.close()
        if situacao == 'Entregue':
            previsao = ''
        
        return previsao, situacao
    except:
        try:
            driver.close()
        except:
            return None, None

print(pega_dados_pajucara('31240351905769000190550010000007551433318883', 51905769000190, 755))
