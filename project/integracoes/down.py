from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.processamento.serializacao import SerializacaoXML
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.entidades.evento import EventoManifestacaoDest
from pynfe.entidades.fonte_dados import _fonte_dados
from pynfe.utils.descompactar import DescompactaGzip
from lxml import etree
from pynfe.utils.flags import NAMESPACE_NFE

from io import BytesIO
from lxml import etree

import datetime
import base64
import gzip

#usar xml tem o minidom, q e lento mas facil, tem o lxml q e rapidao mas chato, e achei o xmltodict
# que transforma o xml em dicionario, nao sei a performace, mas para o uso aqui nao tem problema
# de performace pq usa-se poucas vezes
import xmltodict

def descompactagzip(texto):
    """
    :paramn stringZipada: String

    :return : Etree
    """
    arq = BytesIO()
    arq.write(base64.b64decode(texto))
    arq.seek(0)
    zip = gzip.GzipFile(fileobj=arq)
    texto = zip.read()
    arq.close()
    zip.close()
    descompactado = texto.decode('utf-8')
    return etree.fromstring(descompactado), descompactado

certificado = "eder.pfx"
senha = '1234'
uf = 'MG'
homologacao = False
#import pdb;pdb.set_trace()

def retorna_lista_notas():
    """
    retorna as notas fiscais, cnpj e codigo da nota
    """
    con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
    ULT_NSU = 0
    xml = con.consulta_distribuicao(cnpj='27980581000121',  nsu=ULT_NSU, consulta_nsu_especifico=False)
    resposta = etree.fromstring(xml.content)
    ns = {'ns': NAMESPACE_NFE}
    zip_resposta = resposta.xpath('//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip', namespaces=ns)[0].text
    lista, xml = descompactagzip(zip_resposta)
    return xmltodict.parse(xml)

def retorna_dados_nota(chave):
    
    con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
    #xml = con.consulta_distribuicao(cnpj='27980581000121', chave='31230209119144000136550010000147071010226760', nsu=ULT_NSU, consulta_nsu_especifico=False)
    xml = con.consulta_distribuicao(cnpj='27980581000121',  chave=chave, consulta_nsu_especifico=False)
    resposta = etree.fromstring(xml.content)
    ns = {'ns': NAMESPACE_NFE}
    # zip_resposta = resposta.xpath('//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip', namespaces=ns)[0].text
    zip_resposta = resposta.xpath('ns:Envelope', namespaces=ns)[0].text
    root, xml = descompactagzip(zip_resposta)
    
    return xmltodict.parse(xml)