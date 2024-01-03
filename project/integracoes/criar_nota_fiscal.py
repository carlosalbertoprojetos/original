from lxml import etree
from decimal import Decimal
import datetime
import urllib3

from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.entidades.cliente import Cliente
from pynfe.entidades.emitente import Emitente
from pynfe.entidades.notafiscal import NotaFiscal
from pynfe.entidades.fonte_dados import _fonte_dados
from pynfe.processamento.serializacao import SerializacaoXML
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.utils.flags import CODIGO_BRASIL

urllib3.disable_warnings()


certificado = 'eder.pfx'
senha = '1234'
uf = 'MG'
homologacao = True
CPFCNPJ = '27980581000121'
IE = '29868940028'
NUMERO_NF = '1000'
SERIE_NF = '001'


# emitente
emitente = Emitente(
    razao_social='NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL',
    nome_fantasia='Nome Fantasia da Empresa',
    cnpj=CPFCNPJ,  # cnpj apenas números
    codigo_de_regime_tributario='3',  # 1 para simples nacional ou 3 para normal
    inscricao_estadual=IE,  # numero de IE da empresa
    # inscricao_municipal='12345',
    cnae_fiscal='9999999',  # cnae apenas números
    endereco_logradouro='RUA UM',
    endereco_numero='111',
    endereco_bairro='CENTRO',
    endereco_municipio='CUIABA',
    endereco_uf='MT',
    endereco_cep='78118000',
    endereco_pais=CODIGO_BRASIL,
    endereco_telefone='65999662821',
)

# cliente
cliente = Cliente(
    razao_social='NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL',
    tipo_documento='CNPJ',  # CPF ou CNPJ
    email='email@email.com',
    numero_documento='01346979000389',  # numero do cpf ou cnpj
    indicador_ie=1,  # 9=Não contribuinte
    inscricao_estadual='136315941',
    endereco_logradouro='AV JOSE ANTONIO DE FARIAS',
    endereco_numero='096',
    endereco_complemento='',
    endereco_bairro='LOTEAMENTO JARDIM ELITE',
    endereco_municipio='BARRA DO BUGRES',
    endereco_uf='MT',
    endereco_cep='78390000',
    endereco_pais=CODIGO_BRASIL,
    endereco_telefone='11912341234',
)

# Nota Fiscal
nota_fiscal = NotaFiscal(
    emitente=emitente,
    cliente=cliente,
    uf=uf.upper(),
    natureza_operacao='VENDA',  # venda, compra, transferência, devolução, etc
    # 0=Pagamento à vista; 1=Pagamento a prazo; 2=Outros.
    forma_pagamento=0,
    tipo_pagamento=1,
    modelo=55,                 # 55=NF-e; 65=NFC-e
    serie=SERIE_NF,
    numero_nf=NUMERO_NF,           # Número do Documento Fiscal.
    data_emissao=datetime.datetime.now(),
    data_saida_entrada=datetime.datetime.now(),
    tipo_documento=1,          # 0=entrada; 1=saida
    municipio='5101704',       # Código IBGE do Município
    # 0=Sem geração de DANFE;1=DANFE normal, Retrato;2=DANFE normal
    # Paisagem;3=DANFE Simplificado;4=DANFE NFC-e;
    tipo_impressao_danfe=1,
    forma_emissao='1',         # 1=Emissão normal (não em contingência);
    cliente_final=0,           # 0=Normal;1=Consumidor final;
    indicador_destino=1,
    indicador_presencial=1,
    # 1=NF-e normal;2=NF-e complementar;3=NF-e de ajuste;4=Devolução de
    # mercadoria.
    finalidade_emissao='1',
    processo_emissao='0',  # 0=Emissão de NF-e com aplicativo do contribuinte;
    transporte_modalidade_frete=1,
    informacoes_adicionais_interesse_fisco='Mensagem complementar',
    totais_tributos_aproximado=Decimal('21.06'),
)

# Produto
nota_fiscal.adicionar_produto_servico(
    codigo='1',                           # id do produto
    descricao='CANA DE ACUCAR',
    ncm='12129300',
    # cest='0100100',                            # NT2015/003
    cfop='5101',
    unidade_comercial='UN',
    ean='SEM GTIN',
    ean_tributavel='SEM GTIN',
    quantidade_comercial=Decimal('12'),        # 12 unidades
    valor_unitario_comercial=Decimal('9.75'),  # preço unitário
    valor_total_bruto=Decimal('117.00'),       # preço total
    unidade_tributavel='UN',
    quantidade_tributavel=Decimal('12'),
    valor_unitario_tributavel=Decimal('9.75'),
    ind_total=1,
    # numero_pedido='12345',                   # xPed
    # numero_item='123456',                    # nItemPed
    icms_modalidade='51',
    icms_modalidade_determinacao_bc=3,
    icms_origem=0,
    # icms_cstcsosn='400',
    pis_modalidade='08',
    cofins_modalidade='08',
    # ipi
    ipi_codigo_enquadramento='53',
    ipi_classe_enquadramento='999',
    # aprox. tributos
    valor_tributos_aprox='21.06',
    cbenef=''
)

# responsável técnico
nota_fiscal.adicionar_responsavel_tecnico(
    cnpj='99999999000199',
    contato='L Softwarehouse',
    email='l@gmail.com',
    fone='65911662826'
)

# exemplo de nota fiscal referenciada (devolução/garantia)
# nfRef = NotaFiscalReferenciada(
#     chave_acesso='99999999999999999999999999999999999999999999')
# nota_fiscal.notas_fiscais_referenciadas.append(nfRef)

# serialização
serializador = SerializacaoXML(_fonte_dados, homologacao=homologacao)
nfe = serializador.exportar()

# assinatura
a1 = AssinaturaA1(certificado, senha)
xml = a1.assinar(nfe)

# envio
con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
import pdb;pdb.set_trace()
envio = con.autorizacao(modelo='nfe', nota_fiscal=xml)

# em caso de sucesso o retorno será o xml autorizado
# Ps: no modo sincrono, o retorno será o xml completo (<nfeProc> = <NFe> + <protNFe>)
# no modo async é preciso montar o nfeProc, juntando o retorno com a NFe

if envio[0] == 0:
    print('Sucesso!')
    xml = etree.tostring(
        envio[1],
        encoding="unicode").replace(
        '\n',
        '').replace(
            'ns0:',
        '')
    # em caso de erro o retorno será o xml de resposta da SEFAZ + NF-e enviada
else:
    print('Erro:')
    print(envio[1].text)
    # print('Nota:')
    xml = etree.tostring(envio[2], encoding="unicode")  # nfe

filename = f'emite_nfe-{NUMERO_NF}.xml'
with open(filename, 'w+', encoding='UTF-8') as f:
    f.write(xml)