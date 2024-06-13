import json
import requests
from time import sleep
#url = 'https://radar.tntbrasil.com.br/radar/public/localizacaoSimplificada.do'
#payload = {"nrIdentificacao":"51905769000190","tpDocumento":"NF","remDest":"R","idFilial":13532730,"nrDocumento":"260"}
#r = requests.post(url, data=json.dumps(payload))
#print(r)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By



def pega_dados_tnt(numero_nf, cnpj='51905769000190'):
    try:
        #lista_ocorrencias = ['Entrega Realizada', 'Carta de mercadoria à disposição enviada', 'Ocorrência de entrega']
        url = "https://radar.tntbrasil.com.br/radar/public/localizacaoSimplificada.do"
        driver = webdriver.Chrome()
        driver.get(url)
        inputcnpj = driver.find_element("id", "nrIdentificacao")
        inputcnpj.send_keys(cnpj)
        inputtipodoc = driver.find_element("id", "tpDocumento")
        inputtipodoc.click()
        driver.find_element(By.XPATH,"//li[@aria-label = 'Nota Fiscal']").click()
        inputdoc = driver.find_element("id", "nrDocumento")
        inputdoc.send_keys(numero_nf)
        driver.find_element(By.XPATH,"//button[@label = ' Buscar']").click()
        sleep(10)
        driver.find_element(By.XPATH,"//a[@class = 'link']").click()
        sleep(10)
        trs = driver.find_element(By.XPATH,"//tr[@class = 'ng-star-inserted']")
        data = trs.find_element(By.XPATH,"//td[1]").text
        situacao = trs.find_element(By.XPATH,"//td[2]").text
        previsao = driver.find_element(By.XPATH,"//div[@class = 'linhaTempoDataHora']").text
        #print('data e situacao',data, situacao)
        driver.close()
        return previsao, situacao
    except:
        driver.close()
        return None, None