# https://github.com/TadaSoftware/PyNFe/wiki/Consulta-Nota
import xmltodict

# def retornaDicionario(xml):
#   return xmltodict.parse(xml)

# if __name__=='__main__':
#   with open('xml/32230101754239000896550010005912221000247546.xml') as f:
#     data = f.read()

#   dicionario = retornaDicionario(data)
#   print(dicionario)


from pynfe.processamento.comunicacao import ComunicacaoSefaz
from lxml import etree
from pynfe.utils.flags import NAMESPACE_NFE


certificado = "eder.pfx"
senha = '1234'
uf = 'MG'
homologacao = True


CNPJ = '27980581000121' 
chave_acesso = '32230101754239000896550010005912221000247546'

def faz():

    con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
    envio = con.consulta_nota('nfe', chave_acesso) # nfe ou nfce
    print (envio.text.encode('utf-8')) # SEFAZ SP utilizar envio.content




    ns = {'ns':NAMESPACE_NFE}
    prot = etree.fromstring(envio.text.encode('utf-8')) # SEFAZ SP utilizar envio.content
    status = prot[0][0].xpath('ns:retConsSitNFe/ns:cStat', namespaces=ns)[0].text
    if status == '100':
        prot_nfe = prot[0][0].xpath('ns:retConsSitNFe/ns:protNFe', namespaces=ns)[0]
        xml = etree.tostring(prot_nfe, encoding='unicode')
        print(xml)

faz(chave_acesso)