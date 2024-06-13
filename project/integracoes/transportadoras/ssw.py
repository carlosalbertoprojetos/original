from zeep import Client
from suds.client import Client
from suds.plugin import MessagePlugin
import logging
#from zeep import helpers
#from zeep.transports import Transport
import logging.config


class CorrectNamespace(MessagePlugin):
    def marshalled(self, context):
        soap_env_parent = context.envelope
        #context.envelope.nsprefixes'SOAP-ENV']=''
        #context.envelope.updatePrefix('SOAP-ENV','oi')
        soap_env_parent.prefix =  ''
        import pdb;pdb.set_trace()
        #soap_env_parent.set('xmlns:xsd', 'http://www.w3.org/2001/XMLSchema')
        #soap_env_parent.unset('xmlns:ns0')
        #soap_env_parent.unset('xmlns:ns3')
        ##soap_env_parent.unset('xmlns:ns2')
        #soap_env_parent.set('ns0', 'namespace')


def ssw_cotacoes(cnpj_remetente, cep_remetente, cnpj_destinatario, cep_destinario):
    """
    funcao ssw que faz cotacao
    cotar
    (xs:string dominio, xs:string login, xs:string senha, xs:string cnpjPagador, xs:integer cepOrigem, xs:integer cepDestino, xs:decimal valorNF, xs:integer quantidade, 
    xs:decimal peso, xs:decimal volume, xs:integer mercadoria, xs:string ciffob, xs:string cnpjRemetente, xs:string cnpjDestinatario, xs:string observacao, xs:string trt, 
    xs:string coletar, xs:string entDificil, xs:string destContribuinte, xs:integer qtdePares
    """


    import requests
    # SOAP request URL
    url = 'https://ssw.inf.br/ws/sswCotacaoColeta/index.php?wsdl'
    
    # structured XML
    payload = """
    <x:Envelope
    xmlns:x="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:urn="urn:sswinfbr.sswCotacaoColeta">
    <x:Header/>
    <x:Body>
        <urn:cotarSite>
            <urn:dominio>PAJ</urn:dominio>
            <urn:login>51905769000190</urn:login>
            <urn:senha>ORIGINAL2023</urn:senha>
            <urn:cnpjPagador>51905769000190</urn:cnpjPagador>
            <urn:senhaPagador>32673004</urn:senhaPagador>
            <urn:cepOrigem>25930550</urn:cepOrigem>
            <urn:cepDestino>250000</urn:cepDestino>
            <urn:valorNF>2500</urn:valorNF>
            <urn:quantidade>1</urn:quantidade>
            <urn:peso>43</urn:peso>
            <urn:volume>1</urn:volume>
            <urn:mercadoria>bebedouro</urn:mercadoria>
            <urn:ciffob>51905769000190</urn:ciffob>
            <urn:cnpjRemetente>51905769000190</urn:cnpjRemetente>
            <urn:cnpjDestinatario>03338450000187</urn:cnpjDestinatario>
            <urn:observacao>-</urn:observacao>
            <urn:trt>N</urn:trt>
            <urn:coletar>N</urn:coletar>
            <urn:entDificil>N</urn:entDificil>
            <urn:destContribuinte>0</urn:destContribuinte>
            <urn:qtdePares>0</urn:qtdePares>
        </urn:cotarSite>
    </x:Body>
</x:Envelope>
    """
    # headers
    headers = {
        'Content-Type': 'text/xml; charset=utf-8',
        'SOAPAction': 'urn:sswinfbr.sswCotacaoColeta#cotarSite'
    }
    # POST request
    response = requests.request("POST", url, headers=headers, data=payload)
    
    # prints the response
    print(response.text)
    print(response)
    import pdb;pdb.set_trace()

    """
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('suds.client').setLevel(logging.DEBUG)

    
    #url = 'https://ssw.inf.br/ws/sswCotacaoCliente/index.php?wsdl'
    #https://ssw.inf.br/ws/sswCotacaoColeta/help.html
    url = 'https://ssw.inf.br/ws/sswCotacaoColeta/index.php?wsdl'


    client = Client(url, plugins=[CorrectNamespace()])
    
    domino = 'PAJ'
    login = '51905769000190'
    senha = 'ORIGINAL2023'
    cnpjPagador = '51905769000190'
    cepOrigem = 32673004
    cepDestino = 25930550
    valorNF = '250000'
    quantidade = 1
    peso = '42'
    volume = '868842'
    mercadoria = 1
    ciffob = 'C'
    cnpjRemetente = '51905769000190'
    cnpjDestinatario = '03338450000187'
    observacao = ''
    trt = 'N'
    coletar = 'N'
    entDificil = 'N'
    destContribuinte = 'N'
    qtdePares = 0
    resposta = client.service.cotarSite(domino, login, senha, cnpjPagador, cepOrigem, cepDestino, valorNF, quantidade, peso, volume, mercadoria, ciffob, cnpjRemetente, cnpjDestinatario, observacao, trt, coletar, entDificil, destContribuinte, qtdePares)
    #import pdb;pdb.set_trace()
    # cotarSite(xs:string dominio, xs:string login, xs:string senha, xs:string cnpjPagador, xs:string senhaPagador, xs:integer cepOrigem, xs:integer cepDestino, xs:decimal valorNF, xs:integer quantidade, xs:decimal peso, xs:decimal volume, xs:integer mercadoria, xs:string ciffob, xs:string cnpjRemetente, xs:string cnpjDestinatario, xs:string observacao, xs:string trt, xs:string coletar, xs:string entDificil, xs:string destContribuinte, xs:integer qtdePares)
    #with client.options(raw_response=True):
    #    resposta = client.service.cotar(domino, login, senha, cnpjPagador, senha, cepOrigem, cepDestino, valorNF, quantidade, peso, volume, mercadoria, ciffob, cnpjRemetente, cnpjDestinatario, observacao, coletar, entDificil, destContribuinte, qtdePares)
    #    #coletar, xs:string entDificil, xs:string destContribuinte, xs:integer qtdePares)
    #    print(resposta)
    #import pdb;pdb.set_trace()


    #client = Client(url)
    #
    #result = client.service.cotar(dominio, login, senha, cnpjPagador, cepOrigem, cepDestino, valorNF)
    #result = client.service.ConvertSpeed(100, 'kilometersPerhour', 'milesPerhour')
"""

#ssw_cotacoes('51905769000190', '32673004', '03338450000187', '25930550')