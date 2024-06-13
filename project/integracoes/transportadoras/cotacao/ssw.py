from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from time import sleep


def interceptor(request):
    import pdb;pdb.set_trace()
    del request.headers['Referer']  # Delete the header first
    request.headers['Referer'] = 'some_referer'



def realiza_cotacao(url, cnpjOrigem='51905769000190', password='ORIGINAL2023', cnpjDestinatario='03635125601', cepOrigem='123', cepDestino='03635125601', valor=250000, qtde=1, peso=42, cubagem=0.86):

    #lista_ocorrencias = ['Entrega Realizada', 'Carta de mercadoria à disposição enviada', 'Ocorrência de entrega']
    
    driver = webdriver.Chrome()
    driver.request_interceptor = interceptor
    driver.get(url)
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='tel']"))
    )
    input = driver.find_element(By.XPATH,"//input[@type='tel']")
    input.send_keys(cnpjOrigem)
    driver.find_element(By.XPATH,"//main").click()
    driver.find_element(By.XPATH,"//form").submit()
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
    )
    print('passou da senha')
    #driver.find_element(By.XPATH,"//form").submit()
    #sleep(2)
    #import pdb;pdb.set_trace()
    input = driver.find_element(By.XPATH,"//input[@type='password']")
    input.send_keys(password)
    driver.find_element(By.XPATH,"//form").submit()
    sleep(5)
    descricao = 'Bebedouro Industrial'
    driver.get('https://cliente.viapajucara.com.br/cotacao/cotar')
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "solicitante"))
    )
    # cnpj rementente
    input = driver.find_element(By.XPATH,"//input[@name='cpfOuCnpjRemetente']")
    input.send_keys(cnpjOrigem)
    # clica no botao confirmar
    input = driver.find_element(By.XPATH,"//button[@type='submit']")
    input.click()
    # clica no destinatario
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='cpfOuCnpjDestinatario']"))
    )    
    input = driver.find_element(By.XPATH,"//input[@name='cpfOuCnpjDestinatario']")
    input.send_keys(cnpjDestinatario)
    # cep destino
    input = driver.find_element(By.XPATH,"//input[@name='cepDestino']")
    input.send_keys(cepDestino)
    # clica no botao confirmar
    input = driver.find_element(By.XPATH,"//button[@type='submit']")
    input.click()
    # valor total
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='valorTotal']"))
    )
    input = driver.find_element(By.XPATH,"//input[@name='valorTotal']")
    input.send_keys(valor)    
    
    # quantidade de volume
    input = driver.find_element(By.XPATH,"//input[@placeholder='Quantidade de volumes']")
    input.send_keys(qtde)
    # peso total
    input = driver.find_element(By.XPATH,"//input[@name='pesoTotal']")
    input.send_keys(peso)
    # cubagem
    input = driver.find_element(By.XPATH,"//input[@name='cubagemTotal']")
    input.send_keys(cubagem)
    # descricao da mercadoria
    input = driver.find_element(By.XPATH,"//input[@placeholder='Descrição da mercadoria']")
    input.send_keys(descricao)
    # clica no botao tipo de embalagem
    buttons = driver.find_elements(By.XPATH,"//button[@type='button']")
    buttons[4].click()
    # clica no botao confirmar
    input = driver.find_element(By.XPATH,"//button[@type='submit']")
    input.click()
    import pdb;pdb.set_trace()
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Confirmar e ver resultado')]"))
    )
    input = driver.find_element(By.XPATH,"//*[contains(text(), 'Confirmar e ver resultado')]")
    input.click()
    
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Resultado')]"))
    )
    # pega valor do frete
    frete = driver.find_element(By.XPATH,"//*[contains(text(), 'Frete:')]").text
    frete = frete.replace('Frete: R$ ','')
    # pega numero da cotacao
    cotacao = driver.find_element(By.XPATH,"//*[contains(text(), 'Número da cotação')]").text
    cotacao = cotacao.replace('Número da cotação: ','')
    #pega prazo estimado
    prazo = driver.find_element(By.XPATH,"//*[contains(text(), 'Prazo de entrega estimado')]").text
    prazo = prazo.replace('Prazo de entrega estimado: ', '').replace(' dias úteis', '')
    return cotacao, frete, prazo

#vendas = Venda.objects.filter(venda.status_venda = 'Fazer cotação'):
#for venda in vendas:
#    realiza_cotacao(cnpjdestinatario=venda.cpforcnpj
#print(realiza_cotacao('31240151905769000190550010000004901205879800'))