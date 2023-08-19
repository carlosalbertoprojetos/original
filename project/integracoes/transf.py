# from pynfe.processamento.comunicacao import ComunicacaoSefaz
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


import pprint
import xmltodict


# Open the file and read the contents
# with open('C:\\PROJETOS\\TRABALHOS\\INTIP\ERP\\erp\\project\\integracoes\\arq.xml', 'r', encoding='utf-8') as file:
with open('C:\\xml\\32230101754239000896550010005912221000247546.xml', 'r', encoding='utf-8') as file:
    my_xml = file.read()

# Use xmltodict to parse and convert the 
# XML document
my_dict = xmltodict.parse(my_xml)

# print(my_dict)

# Print the dictionary
# pprint.pprint(my_dict, indent=2)



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


def retorna_dados_nota(chave):

    con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
    xml = con.consulta_distribuicao(cnpj='27980581000121',  chave=chave, consulta_nsu_especifico=False)
    resposta = etree.fromstring(xml.content)
    ns = {'ns': NAMESPACE_NFE}
    zip_resposta = resposta.xpath('//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip', namespaces=ns)[0].text
    root, xml = descompactagzip(zip_resposta)
    # return xmltodict.parse(xml)

    xmltodict.parse(xml)
    # print(xml)
    pprint.pprint(xml, indent=2)

    return xmltodict.parse(xml)


# chave='32230101754239000896550010005912221000247546'
# print(retorna_dados_nota(chave))


# https://github.com/felipebz/schemas-mdfe/blob/master/retDistDFeInt.xsd




xml = {'chNFe': 'NFe32230101754239000896550010005912221000247546', 'CNPJ': '64966559000153', 'xNome': 'ZUFER TECNOLOGIA E FERRAMENTARIA LTDA', 'IE': '623020769115', 'dhEmi': '2023-01-03T00:00:00-03:00', 'tpNF': '1', 'vNF': '2695.95', 'digVal': 'hZ3icApykBs+JTX7Ed+DsjxqGNs=', 'dhRecbto': '2023-01-03T17:41:15-03:00', 'nProt': '135230011050902', 'cSitNFe': '1'}

"""

xml = {'nfeProc': {'@versao': '4.00', '@xmlns': 'http://www.portalfiscal.inf.br/nfe', 'NFe': {'@xmlns': 'http://www.portalfiscal.inf.br/nfe', 'infNFe': {'@Id': 'NFe32230101754239000896550010005912221000247546', '@versao': '4.00', 
'ide': {'cUF': '32', 'cNF': '00024754', 'natOp': 'Retorno em Garantia', 'mod': '55', 'serie': '1', 'nNF': '591222', 'dhEmi': '2023-01-06T17:22:17-03:00', 'dhSaiEnt': '2023-01-06T17:22:17-03:00', 'tpNF': '1', 'idDest': '2', 'cMunFG': '3205200', 'tpImp': '1', 'tpEmis': '1', 'cDV': '6', 'tpAmb': '1', 'finNFe': '1', 'indFinal': '0', 'indPres': '0', 'procEmi': '0', 'verProc': '6.3.4000.127'}, 'emit': {'CNPJ': '01754239000896', 'xNome': 'REFRIGERACAO DUFRIO COMERCIO E IMPORTACAO S.A.', 'xFant': 'REFRIGERACAO DUFRIO COMERCIO E IMPORTACAO S.A.', 'enderEmit': {'xLgr': 'RODOVIA DARLY SANTOS', 'nro': '800', 'xCpl': 'LOTE 1-C', 'xBairro': 'JARDIM ASTECA', 'cMun': '3205200', 'xMun': 'VILA VELHA', 'UF': 'ES', 'CEP': '29104491', 'cPais': '1058', 'xPais': 'Brasil'}, 'IE': '082551707', 'CRT': '3'}, 'dest': {'CNPJ': '27980581000121', 'xNome': 'EDER SAULO COSTA 06073667612', 'enderDest': {'xLgr': 'AV JUIZ MARCO TULIO ISAAC', 'nro': '4260', 'xBairro': 'JARDIM DAS ALTEROSAS 1A SECAO', 'cMun': '3106705', 'xMun': 'BETIM', 'UF': 'MG', 'CEP': '32671104', 'cPais': '1058', 'xPais': 'Brasil', 'fone': '31993989016'}, 'indIEDest': '1', 'IE': '0029868940028', 'email': 'originalbebedouros@gmail.com'}, 'det': [{'@nItem': '1', 'prod': {'cProd': '12083', 'cEAN': 'SEM GTIN', 'xProd': 'COMP 1/5 HP R134 220V LBP TH231GS TECUMSEH', 'NCM': '84143011', 'cBenef': 
None, 'CFOP': '6949', 'uCom': 'PC', 'qCom': '1.0000', 'vUnCom': '315.0000000000', 'vProd': '315.00', 'cEANTrib': 'SEM GTIN', 'uTrib': 'PC', 'qTrib': '1.0000', 'vUnTrib': '315.0000000000', 'indTot': '1', 'nFCI': '670406A5-A6CA-44EE-AEAC-2867BEE5C355'}, 'imposto': {'ICMS': {'ICMS00': {'orig': '5', 'CST': '00', 'modBC': '3', 'vBC': '315.00', 'pICMS': '12.00', 'vICMS': '37.80'}}, 'IPI': {'cEnq': '999', 'IPITrib': {'CST': '99', 'vBC': '0.00', 'pIPI': '0.00', 'vIPI': '0.00'}}, 'PIS': {'PISOutr': {'CST': '49', 'vBC': '315.00', 'pPIS': '0.00', 'vPIS': '0.00'}}, 'COFINS': {'COFINSOutr': {'CST': '49', 'vBC': '315.00', 'pCOFINS': '0.00', 'vCOFINS': '0.00'}}}}, {'@nItem': '2', 'prod': {'cProd': '12084', 'cEAN': 'SEM GTIN', 'xProd': 'COMP 1/4 HP L128 220V LBP TH231GS TECUMSEH', 'NCM': '84143011', 'cBenef': None, 'CFOP': '6949', 'uCom': 'PC', 'qCom': '1.0000', 'vUnCom': '279.9000000000', 'vProd': 
'279.90', 'cEANTrib': 'SEM GTIN', 'uTrib': 'PC', 'qTrib': '1.0000', 'vUnTrib': '279.9000000000', 'indTot': '1', 'nFCI': '670406A5-A6CA-44EE-AEAC-2867BEE5C355'}, 'imposto': {'ICMS': {'ICMS00': {'orig': '5', 'CST': '00', 'modBC': '3', 'vBC': '279.90', 'pICMS': '12.00', 'vICMS': '33.59'}}, 'IPI': {'cEnq': '999', 'IPITrib': {'CST': '99', 'vBC': '0.00', 'pIPI': '0.00', 'vIPI': '0.00'}}, 'PIS': {'PISOutr': {'CST': '49', 'vBC': '279.90', 'pPIS': '0.00', 'vPIS': '0.00'}}, 'COFINS': {'COFINSOutr': {'CST': '49', 'vBC': '279.90', 'pCOFINS': '0.00', 'vCOFINS': '0.00'}}}}, {'@nItem': '3', 'prod': {'cProd': '12085', 'cEAN': 'SEM GTIN', 'xProd': 'COMP 2 HP R220 110V LBP TH231GS TECUMSEH', 'NCM': '84143011', 'cBenef': None, 'CFOP': '6949', 'uCom': 'PC', 'qCom': '1.0000', 'vUnCom': '315.0000000000', 'vProd': '315.00', 'cEANTrib': 'SEM GTIN', 'uTrib': 'PC', 'qTrib': '1.0000', 'vUnTrib': '315.0000000000', 'indTot': '1', 'nFCI': '670406A5-A6CA-44EE-AEAC-2867BEE5C355'}, 'imposto': {'ICMS': {'ICMS00': {'orig': '5', 'CST': '00', 'modBC': '3', 'vBC': '315.00', 'pICMS': '12.00', 'vICMS': '37.80'}}, 'IPI': {'cEnq': '999', 'IPITrib': {'CST': '99', 'vBC': '0.00', 'pIPI': '0.00', 'vIPI': '0.00'}}, 'PIS': {'PISOutr': {'CST': '49', 'vBC': '315.00', 'pPIS': '0.00', 'vPIS': '0.00'}}, 'COFINS': {'COFINSOutr': {'CST': '49', 'vBC': '315.00', 'pCOFINS': '0.00', 'vCOFINS': '0.00'}}}}], 'total': {'ICMSTot': {'vBC': '909.90', 'vICMS': '109.19', 'vICMSDeson': '0.00', 'vFCP': '0.00', 'vBCST': '0.00', 'vST': '0.00', 'vFCPST': '0.00', 'vFCPSTRet': '0.00', 'vProd': '909.90', 'vFrete': '0.00', 'vSeg': '0.00', 'vDesc': '0.00', 'vII': '0.00', 'vIPI': '0.00', 'vIPIDevol': '0.00', 'vPIS': '0.00', 'vCOFINS': '0.00', 'vOutro': '0.00', 'vNF': '909.90'}}, 'transp': {'modFrete': '0', 'vol': {'qVol': '3', 'esp': 'VOLUME', 'pesoL': '22.000', 'pesoB': '22.000'}}, 'cobr': {'fat': {'nFat': '000591222', 'vOrig': '909.90', 'vDesc': '0.00', 'vLiq': '909.90'}}, 'pag': {'detPag': {'tPag': '90', 'vPag': '0.00'}}, 'infAdic': {'infAdFisco': '- Valor aproximado dos tributos cf lei 12.741/12 Federais 0,00 Estaduais 109,19 -Volume Total: 0,026163 (m3) GARANTIA INTERLOJA REF - NF 333 - OG 170903 - OV00808986879', 'infCpl': 'Numeros De serie:51K212232160529 51K222231105316 51K152233003950 .'}, 'infRespTec': {'CNPJ': '01754239000110', 'xContato': 'Tainara Pohlmann Flores', 'email': 'tainara.flores@dufrio.com.br', 'fone': '5137787569'}}, 'Signature': {'@xmlns': 'http://www.w3.org/2000/09/xmldsig#', 'SignedInfo': {'CanonicalizationMethod': {'@Algorithm': 'http://www.w3.org/TR/2001/REC-xml-c14n-20010315'}, 'SignatureMethod': {'@Algorithm': 'http://www.w3.org/2000/09/xmldsig#rsa-sha1'}, 'Reference': {'@URI': '#NFe32230101754239000896550010005912221000247546', 'Transforms': {'Transform': [{'@Algorithm': 'http://www.w3.org/2000/09/xmldsig#enveloped-signature'}, {'@Algorithm': 'http://www.w3.org/TR/2001/REC-xml-c14n-20010315'}]}, 'DigestMethod': {'@Algorithm': 'http://www.w3.org/2000/09/xmldsig#sha1'}, 'DigestValue': 'pVffNRtJwGs28i3lyj4BSv37Z70='}}, 'SignatureValue': 'BPq1EgJj1ZKqmPH+6HFOORpZylcAwRSGIcvAE56Jder31z2zopkYHxQ6Z+JWKy1vAxn99ZZCa86cIYaLQPs7xccy1Fp5+yUbqvq8JZN9Ow6vPJ6ly/P88Bsj60CHmwyBf5o/dGhL+Q3cAZB46BpkuQp0V/BCFB/2cYlf+XEJ99tZR8Vh73EfnzlkcV0ibl2VyE8YVFoD4RtcKAPiBkGte2B1N6gJ/tGRL4WFIP+4ftMSG8gNYEywWhJ6Vif/1ysYDlGGj0N2eigAJ6Xk3p8dnbAZr8nhbTw4hkk2OUMaR4NK/5J41JGmKFWROAjpkJ3i0YozL8GnEfnj/v4FRCxywg==', 'KeyInfo': {'X509Data': {'X509Certificate': 'MIIHVzCCBT+gAwIBAgIITSsiCQVHw7AwDQYJKoZIhvcNAQELBQAwWTELMAkGA1UEBhMCQlIxEzARBgNVBAoTCklDUC1CcmFzaWwxFTATBgNVBAsTDEFDIFNPTFVUSSB2NTEeMBwGA1UEAxMVQUMgU09MVVRJIE11bHRpcGxhIHY1MB4XDTIyMDkwNTE4MjYwMFoXDTIzMDkwNTE4MjYwMFowgfgxCzAJBgNVBAYTAkJSMRMwEQYDVQQKEwpJQ1AtQnJhc2lsMQswCQYDVQQIEwJSUzEVMBMGA1UEBxMMUG9ydG8gQWxlZ3JlMR4wHAYDVQQLExVBQyBTT0xVVEkgTXVsdGlwbGEgdjUxFzAVBgNVBAsTDjA1NDA1OTg3MDAwMTQ4MRMwEQYDVQQLEwpQcmVzZW5jaWFsMRowGAYDVQQLExFDZXJ0aWZpY2FkbyBQSiBBMTFGMEQGA1UEAxM9UkVGUklHRVJBQ0FPIERVRlJJTyBDT01FUkNJTyBFIElNUE9SVEFDQU8gUy5BLjowMTc1NDIzOTAwMDExMDCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAIWlztHiDn0k5evfWP7tUUkSb2ik/LB1WnSVvsyGJ0nfBHP3YdqLDaxAt3H++1FBaU3KcXZNuFePticQDbwgTeR/eljQfvPk1s+vdNG0+av8yKlaud3tjz8USbBj48IoNXhJwOLKYNTXj5vJoQcFEdWdiwx7JAMQz/6y6jTrBd5WPkAdeCzqdk+2YF27RMn6jpkeil2XUxAKxhkc85EHgVF57G1YfAZ5BTi0fVi/YdETvrZhhx/RNzyCekYsjx/usWlpL0vD5mlTc4rA0O10PgRtVFeKrb4u/BrmBl+goibyYrHEil75g+TREe0xEReeyLQ6K3qoGnXxPLU7Vap3KxsCAwEAAaOCAoEwggJ9MAkGA1UdEwQCMAAwHwYDVR0jBBgwFoAUxVLtJYAJ35yCyJ9Hxt20XzHdubEwVAYIKwYBBQUHAQEESDBGMEQGCCsGAQUFBzAChjhodHRwOi8vY2NkLmFjc29sdXRpLmNvbS5ici9sY3IvYWMtc29sdXRpLW11bHRpcGxhLXY1LnA3YjCBvAYDVR0RBIG0MIGxgR1kYWdvYmVydG8uemFub25AZHVmcmlvLmNvbS5icqAiBgVgTAEDAqAZExdEYWdvYmVydG8gQXJ0ZW1pbyBaYW5vbqAZBgVgTAEDA6AQEw4wMTc1NDIzOTAwMDExMKA4BgVgTAEDBKAvEy0wODExMTk1NTE0OTM1Mjk1MDE1MDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDCgFwYFYEwBAwegDhMMMDAwMDAwMDAwMDAwMF0GA1UdIARWMFQwUgYGYEwBAgEmMEgwRgYIKwYBBQUHAgEWOmh0dHA6Ly9jY2QuYWNzb2x1dGkuY29tLmJyL2RvY3MvZHBjLWFjLXNvbHV0aS1tdWx0aXBsYS5wZGYwHQYDVR0lBBYwFAYIKwYBBQUHAwIGCCsGAQUFBwMEMIGMBgNVHR8EgYQwgYEwPqA8oDqGOGh0dHA6Ly9jY2QuYWNzb2x1dGkuY29tLmJyL2xjci9hYy1zb2x1dGktbXVsdGlwbGEtdjUuY3JsMD+gPaA7hjlodHRwOi8vY2NkMi5hY3NvbHV0aS5jb20uYnIvbGNyL2FjLXNvbHV0aS1tdWx0aXBsYS12NS5jcmwwHQYDVR0OBBYEFOvKfJXJkiFELwRkxBi4Lz76plfRMA4GA1UdDwEB/wQEAwIF4DANBgkqhkiG9w0BAQsFAAOCAgEAVdWsBWaIRt66NYjwId1enUiWJsYsVVioeki5lnF9Q4wnTnn7sfWYgVM55RJN+4tW8PhxKwXTAdk/kXBHzS75TgpvJe+RRRRYxQmVyCQ4QxT07Q00Ds+xGZFKUjliLN24tIrW/UV1h3ymtjZQoBIrz9GnNBXGfAsSlCR+oq/5/q3gSJ54z+mFCCy3pUJqv9zwUarbbWqTZCduT8RVkM70qBDDkM+RrJX0W+PF/+pPKgvVWKNl4Ap7TRdT9MydBlhixgu1yHWdqDRp8GOb2GW09bs5Ot92fEm9Q8u0Jxix7xywZyTe+bsJIcoSoXUXrdOBwnUczW5Q+d0ySgrLdias1qfF/iA5VZPqzpDtpVNOmHKm9rM2aikhEd05Eg7BQnywP0xgEilcY5zq8IvJJI7+ny97SIOS4M9vaBKse3KxhHissZnJXdJXvLGDb6Vw+mq/2VvcpNHJKkPVW+yauzY47HZGM2TQNyAuDG5ZpaCXCHkjtOLlfEQhzZ7v7Waqo1WkUfobl2awQKqRqWR1PahWm+ym2/gLCJOPiNX/nABkhahoA6P7Fjr6uJ8JJFF3vK7xQHL70iPEM0kmkNwArh9jgUvgL0tf7KrNpICPYyFF5bYTo25KvgZccTvPTKI1jrS1W8m7A+Y4X/Y/EAGifNmolsy4uapE99Cj0+YrnHLEfPU='}}}}, 'protNFe': {'@versao': '4.00', '@xmlns': 'http://www.portalfiscal.inf.br/nfe', 'infProt': {'tpAmb': '1', 'verAplic': 'SVRS202212291442', 'chNFe': '32230101754239000896550010005912221000247546', 'dhRecbto': '2023-01-06T17:22:20-03:00', 'nProt': '332230001588242', 'digVal': 'pVffNRtJwGs28i3lyj4BSv37Z70=', 'cStat': '100', 'xMotivo': 'Autorizado o uso da NF-e'}}}}


"""









# xml = {'nfeProc': {'@versao': '4.00', '@xmlns': 'http://www.portalfiscal.inf.br/nfe', 'NFe': {'@xmlns': 'http://www.portalfiscal.inf.br/nfe', 'infNFe': {'@Id': 'NFe32230101754239000896550010005912221000247546', '@versao': '4.00', 
# 'ide': {'cUF': '32', 'cNF': '00024754', 'natOp': 'Retorno em Garantia', 'mod': '55', 'serie': '1', 'nNF': '591222', 'dhEmi': '2023-01-06T17:22:17-03:00', 'dhSaiEnt': '2023-01-06T17:22:17-03:00', 'tpNF': '1', 'idDest': '2', 'cMunFG': '3205200', 'tpImp': '1', 'tpEmis': '1', 'cDV': '6', 'tpAmb': '1', 'finNFe': '1', 'indFinal': '0', 'indPres': '0', 'procEmi': '0', 'verProc': '6.3.4000.127'}, 'emit': {'CNPJ': '01754239000896', 'xNome': 'REFRIGERACAO DUFRIO COMERCIO E IMPORTACAO S.A.', 'xFant': 'REFRIGERACAO DUFRIO COMERCIO E IMPORTACAO S.A.', 'enderEmit': {'xLgr': 'RODOVIA DARLY SANTOS', 'nro': '800', 'xCpl': 'LOTE 1-C', 'xBairro': 'JARDIM ASTECA', 'cMun': '3205200', 'xMun': 'VILA VELHA', 'UF': 'ES', 'CEP': '29104491', 'cPais': '1058', 'xPais': 'Brasil'}, 'IE': '082551707', 'CRT': '3'}, 'dest': {'CNPJ': '27980581000121', 'xNome': 'EDER SAULO COSTA 06073667612', 'enderDest': {'xLgr': 'AV JUIZ MARCO TULIO ISAAC', 'nro': '4260', 'xBairro': 'JARDIM DAS ALTEROSAS 1A SECAO', 'cMun': '3106705', 'xMun': 'BETIM', 'UF': 'MG', 'CEP': '32671104', 'cPais': '1058', 'xPais': 'Brasil', 'fone': '31993989016'}, 'indIEDest': '1', 'IE': '0029868940028', 'email': 'originalbebedouros@gmail.com'}, 'det': [{'@nItem': '1', 'prod': {'cProd': '12083', 'cEAN': 'SEM GTIN', 'xProd': 'COMP 1/5 HP R134 220V LBP TH231GS TECUMSEH', 'NCM': '84143011', 'cBenef': 
# None, 'CFOP': '6949', 'uCom': 'PC', 'qCom': '1.0000', 'vUnCom': '315.0000000000', 'vProd': '315.00', 'cEANTrib': 'SEM GTIN', 'uTrib': 'PC', 'qTrib': '1.0000', 'vUnTrib': '315.0000000000', 'indTot': '1', 'nFCI': '670406A5-A6CA-44EE-AEAC-2867BEE5C355'}, 'imposto': {'ICMS': {'ICMS00': {'orig': '5', 'CST': '00', 'modBC': '3', 'vBC': '315.00', 'pICMS': '12.00', 'vICMS': '37.80'}}, 'IPI': {'cEnq': '999', 'IPITrib': {'CST': '99', 'vBC': '0.00', 'pIPI': '0.00', 'vIPI': '0.00'}}, 'PIS': {'PISOutr': {'CST': '49', 'vBC': '315.00', 'pPIS': '0.00', 'vPIS': '0.00'}}, 'COFINS': {'COFINSOutr': {'CST': '49', 'vBC': '315.00', 'pCOFINS': '0.00', 'vCOFINS': '0.00'}}}}, {'@nItem': '2', 'prod': {'cProd': '12084', 'cEAN': 'SEM GTIN', 'xProd': 'COMP 3/4 HP L543 220V TECUMSEH', 'NCM': '84143011', 'cBenef': None, 'CFOP': '6949', 'uCom': 'PC', 'qCom': '1.0000', 'vUnCom': '279.9000000000', 'vProd': 
# '279.90', 'cEANTrib': 'SEM GTIN', 'uTrib': 'PC', 'qTrib': '1.0000', 'vUnTrib': '279.9000000000', 'indTot': '1', 'nFCI': '670406A5-A6CA-44EE-AEAC-2867BEE5C355'}, 'imposto': {'ICMS': {'ICMS00': {'orig': '5', 'CST': '00', 'modBC': '3', 'vBC': '279.90', 'pICMS': '12.00', 'vICMS': '33.59'}}, 'IPI': {'cEnq': '999', 'IPITrib': {'CST': '99', 'vBC': '0.00', 'pIPI': '0.00', 'vIPI': '0.00'}}, 'PIS': {'PISOutr': {'CST': '49', 'vBC': '279.90', 'pPIS': '0.00', 'vPIS': '0.00'}}, 'COFINS': {'COFINSOutr': {'CST': '49', 'vBC': '279.90', 'pCOFINS': '0.00', 'vCOFINS': '0.00'}}}}, {'@nItem': '3', 'prod': {'cProd': '12085', 'cEAN': 'SEM GTIN', 'xProd': 'LAM 1/5 HP R214 110V LBP TJ635GS TECUMSEH', 'NCM': '84143011', 'cBenef': None, 'CFOP': '6949', 'uCom': 'PC', 'qCom': '1.0000', 'vUnCom': '315.0000000000', 'vProd': '315.00', 'cEANTrib': 'SEM GTIN', 'uTrib': 'PC', 'qTrib': '1.0000', 'vUnTrib': '315.0000000000', 'indTot': '1', 'nFCI': '670406A5-A6CA-44EE-AEAC-2867BEE5C355'}, 'imposto': {'ICMS': {'ICMS00': {'orig': '5', 'CST': '00', 'modBC': '3', 'vBC': '315.00', 'pICMS': '12.00', 'vICMS': '37.80'}}, 'IPI': {'cEnq': '999', 'IPITrib': {'CST': '99', 'vBC': '0.00', 'pIPI': '0.00', 'vIPI': '0.00'}}, 'PIS': {'PISOutr': {'CST': '49', 'vBC': '315.00', 'pPIS': '0.00', 'vPIS': '0.00'}}, 'COFINS': {'COFINSOutr': {'CST': '49', 'vBC': '315.00', 'pCOFINS': '0.00', 'vCOFINS': '0.00'}}}}], 'total': {'ICMSTot': {'vBC': '909.90', 'vICMS': '109.19', 'vICMSDeson': '0.00', 'vFCP': '0.00', 'vBCST': '0.00', 'vST': '0.00', 'vFCPST': '0.00', 'vFCPSTRet': '0.00', 'vProd': '909.90', 'vFrete': '0.00', 'vSeg': '0.00', 'vDesc': '0.00', 'vII': '0.00', 'vIPI': '0.00', 'vIPIDevol': '0.00', 'vPIS': '0.00', 'vCOFINS': '0.00', 'vOutro': '0.00', 'vNF': '909.90'}}, 'transp': {'modFrete': '0', 'vol': {'qVol': '3', 'esp': 'VOLUME', 'pesoL': '22.000', 'pesoB': '22.000'}}, 'cobr': {'fat': {'nFat': '000591222', 'vOrig': '909.90', 'vDesc': '0.00', 'vLiq': '909.90'}}, 'pag': {'detPag': {'tPag': '90', 'vPag': '0.00'}}, 'infAdic': {'infAdFisco': '- Valor aproximado dos tributos cf lei 12.741/12 Federais 0,00 Estaduais 109,19 -Volume Total: 0,026163 (m3) GARANTIA INTERLOJA REF - NF 333 - OG 170903 - OV00808986879', 'infCpl': 'Numeros De serie:51K212232160529 51K222231105316 51K152233003950 .'}, 'infRespTec': {'CNPJ': '01754239000110', 'xContato': 'Tainara Pohlmann Flores', 'email': 'tainara.flores@dufrio.com.br', 'fone': '5137787569'}}, 'Signature': {'@xmlns': 'http://www.w3.org/2000/09/xmldsig#', 'SignedInfo': {'CanonicalizationMethod': {'@Algorithm': 'http://www.w3.org/TR/2001/REC-xml-c14n-20010315'}, 'SignatureMethod': {'@Algorithm': 'http://www.w3.org/2000/09/xmldsig#rsa-sha1'}, 'Reference': {'@URI': '#NFe32230101754239000896550010005912221000247546', 'Transforms': {'Transform': [{'@Algorithm': 'http://www.w3.org/2000/09/xmldsig#enveloped-signature'}, {'@Algorithm': 'http://www.w3.org/TR/2001/REC-xml-c14n-20010315'}]}, 'DigestMethod': {'@Algorithm': 'http://www.w3.org/2000/09/xmldsig#sha1'}, 'DigestValue': 'pVffNRtJwGs28i3lyj4BSv37Z70='}}, 'SignatureValue': 'BPq1EgJj1ZKqmPH+6HFOORpZylcAwRSGIcvAE56Jder31z2zopkYHxQ6Z+JWKy1vAxn99ZZCa86cIYaLQPs7xccy1Fp5+yUbqvq8JZN9Ow6vPJ6ly/P88Bsj60CHmwyBf5o/dGhL+Q3cAZB46BpkuQp0V/BCFB/2cYlf+XEJ99tZR8Vh73EfnzlkcV0ibl2VyE8YVFoD4RtcKAPiBkGte2B1N6gJ/tGRL4WFIP+4ftMSG8gNYEywWhJ6Vif/1ysYDlGGj0N2eigAJ6Xk3p8dnbAZr8nhbTw4hkk2OUMaR4NK/5J41JGmKFWROAjpkJ3i0YozL8GnEfnj/v4FRCxywg==', 'KeyInfo': {'X509Data': {'X509Certificate': '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'}}}}, 'protNFe': {'@versao': '4.00', '@xmlns': 'http://www.portalfiscal.inf.br/nfe', 'infProt': 
# {'tpAmb': '1', 'verAplic': 'SVRS202212291442', 'chNFe': '32230101754239000896550010005912221000247546', 'dhRecbto': '2023-01-06T17:22:20-03:00', 'nProt': '332230001588242', 'digVal': 'pVffNRtJwGs28i3lyj4BSv37Z70=', 'cStat': 
# '100', 'xMotivo': 'Autorizado o uso da NF-e'}}}}


