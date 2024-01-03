import http.client
import json


template_emissao_pf = """
{
  "ID": @1137,
  "url_notificacao": "@http://meudominio.com/retorno.php",
  "operacao": 1,
  "natureza_operacao": "@Venda de produção do estabelecimento",
  "modelo": @1,
  "finalidade": @1,
  "ambiente": @1,
  "pedido": {
    "pagamento": 0,
    "presenca": 2,
    "modalidade_frete": 0,
    "frete": "12.56",
    "desconto": "10.00",
    "total": "174.60"
  }
}
"""

from empresa.models import Empresa
from cliente.models import Cliente
from venda.models import Venda

def emite_nf(pk):
    """
    emite nota fiscal no sistema webmania
    """
    venda = Venda.objects.get(id=pk)
    cliente = venda.cliente

    # valida se tem frete
    if venda.codigo_mercadolivre:
      if not venda.valor_frete and not venda.cotacao_transportadora:
        erros = ['Venda Mercado Livre é necessário informar cotação e valor do frete']
        return None, erros

    nf = {}
    nf['operacao'] = 1
    nf['natureza_operacao'] = venda.vendedor.extenduser.empresa.natureza_operacao
    nf['modelo'] = 1
    nf['finalidade'] = 1
    nf['ambiente'] = 1

    #monta produto
    produtos = []
    peso_total = 0
    volume_total = 0
    for produto in venda.vendaproduto_set.all():
      dictproduto = {}
      dictproduto['nome'] = produto.produto.nome + ' ' + produto.voltagem.nome + ' ' +  produto.torneira.nome
      dictproduto['codigo'] = produto.produto.codigoproduto
      dictproduto['ncm'] = produto.produto.ncm
      dictproduto['cest'] = produto.produto.cst
      dictproduto['quantidade'] = produto.quantidade
      dictproduto['unidade'] = produto.produto.unimed.unidade
      dictproduto['peso'] = produto.produto.peso
      peso_total += produto.produto.peso * produto.quantidade
      volume_total += produto.quantidade
      dictproduto['origem'] = 0
      dictproduto['subtotal'] = str(produto.preco)
      dictproduto['total'] = str(produto.preco *  produto.quantidade)
      dictproduto['classe_imposto'] = venda.vendedor.extenduser.empresa.webmania_classedeimposto
      produtos.append(dictproduto)
    if produtos:
      nf['produtos'] = produtos

    
    try:
      empresa = venda.vendedor.extenduser.empresa
    except:
      empresa = Empresa.objects.first()
    #adiciona o filtro
    desconto = 0
    #if empresa.nome != 'ORIGINAL2':
    dictproduto = {}
    dictproduto['nome'] = 'Filtro Iguatu'
    dictproduto['codigo'] = '15'
    dictproduto['ncm'] = '84212100'
    dictproduto['cest'] = '2109800'
    dictproduto['quantidade'] = volume_total
    dictproduto['unidade'] = 'Un'
    dictproduto['peso'] = 0
    dictproduto['origem'] = 0
    dictproduto['subtotal'] = 28
    dictproduto['total'] = str(28 *  produto.quantidade)
    if empresa.nome == 'ORIGINAL':
        dictproduto['classe_imposto'] = 'REF157931346'
    else:
        dictproduto['classe_imposto'] = 'REF154942336'
    desconto = 28 * volume_total
    produtos.append(dictproduto)
    #monta cliente
    dict_cliente = {}
    if cliente.cpf:
      dict_cliente['cpf'] = cliente.cpf.number
    elif cliente.cnpj:
      dict_cliente['cnpj'] = cliente.cnpj.number
      dict_cliente['razao_social'] = cliente.nome
      dict_cliente['ie'] = cliente.insc_estadual

    
    dict_cliente['nome_completo'] = cliente.nome
    dict_cliente['endereco'] = cliente.logradouro
    dict_cliente['complemento'] = cliente.complemento
    dict_cliente['numero'] = cliente.numero
    dict_cliente['bairro'] = cliente.bairro
    dict_cliente['cidade'] = cliente.cidade
    dict_cliente['uf'] = cliente.estado
    dict_cliente['cep'] = cliente.cep
    dict_cliente['telefone'] = cliente.tel_principal
    dict_cliente['email'] = cliente.email
    nf['cliente'] = dict_cliente

    pedido = {}
    pagamento_a_prazo = 0 if venda.parcelas == 1 else 1
    # pedido    
    pedido['pagamento'] = pagamento_a_prazo


    pedido['presenca'] = empresa.presenca
    pedido['modalidade_frete'] =  empresa.modalidade_frete
    pedido['desconto'] = desconto
    pedido['frete'] =  0 # float(venda.valor_frete)
    informacoes_complementares = ' ref pedido: ' + str(venda.id)
    if venda.cotacao_transportadora:
      informacoes_complementares += ' ' + str(venda.cotacao_transportadora) + ' ' + str(venda.valor_frete)
    if venda.quemrecebe_mercadolivre:
      informacoes_complementares += ' quem recebe:' + venda.quemrecebe_mercadolivre
    if venda.telefonequemrecebe_mercadolivre:
      informacoes_complementares += ' tel quem recebe: ' + venda.telefonequemrecebe_mercadolivre
    pedido['informacoes_complementares'] = informacoes_complementares
    pedido['total'] = str(venda.valor_venda)

    nf['pedido'] = pedido

    #transporte
    transporte = {}
    if venda.transportadora:
      if venda.transportadora.nome != 'Cliente Retira':
        if venda.transportadora.cnpj:
          transporte['cnpj'] = venda.transportadora.cnpj.number
        transporte['especie'] = 'unidade'
        transporte['marca'] = 'original'
        transporte['volume'] = volume_total
        transporte['peso_bruto'] = peso_total
        transporte['peso_liquido'] = peso_total
        
        # calcula peso
        transporte['razao_social'] = venda.transportadora.nome
        transporte['ie'] = venda.transportadora.insc_estadual
        transporte['endereco'] = venda.transportadora.logradouro
        transporte['uf'] = venda.transportadora.estado
        transporte['cidade'] = venda.transportadora.cidade
        transporte['cep'] = venda.transportadora.cep
        nf['transporte'] = transporte


    #"ID": 1137,
    #"url_notificacao": "https://webmaniabr.com/retorno.php",
    conn = http.client.HTTPSConnection("webmaniabr.com")

    # Credenciais de acesso
    headers = {
      'cache-control': "no-cache",
      'content-type': "application/json",
      'x-consumer-key': venda.vendedor.extenduser.empresa.webmania_consumerkey,
      'x-consumer-secret': venda.vendedor.extenduser.empresa.webmania_consumersecret,
      'x-access-token': venda.vendedor.extenduser.empresa.webmania_accesstoken,
      'x-access-token-secret': venda.vendedor.extenduser.empresa.webmania_accesstokensecret
    }

    # Comunicando com a API
    json_object = json.dumps(nf, indent = 8)

    print('json_object')
    print(json_object)
    conn.request("POST", "/api/1/nfe/emissao/", json_object, headers)

    # Retorno da API
    res = conn.getresponse()
    data = res.read()

    # Exibir retorno
    resposta = data.decode("utf-8")
    resposta =  json.loads(resposta)
    erros = []
    print('resposta', resposta)
    if 'nfe' in resposta:
      nfe = resposta['nfe']
      venda.numero_nf = nfe

    if 'chave' in resposta:
      chave = resposta['chave']
      venda.chave = chave
      venda.status = 'nfemitida'
    if 'status' in resposta:
      status = resposta['status']
      venda.status = status
    if 'motivo' in resposta:
      motivo = resposta['motivo']
      venda.motivo = motivo
    if 'uuid' in resposta:
      uuid = resposta['uuid']
      venda.uuid = uuid
    if 'xml' in resposta:
      xml = resposta['xml']
      venda.xml = xml
    if 'danfe' in resposta:
      danfe = resposta['danfe']
      venda.danfe = danfe
    if 'danfe_simples' in resposta:
      danfe_simples = resposta['danfe_simples']
      venda.danfe_simples = danfe_simples
    if 'danfe_etiqueta' in resposta:
      danfe_etiqueta = resposta['danfe_etiqueta']
      venda.danfe_etiqueta = danfe_etiqueta
    
    # 
    venda.save()

    if 'error' in resposta:
      erro = resposta['error']
      erros.append(erro)
    return resposta, erros


def consulta_nf(self):
  """
  """
  conn = http.client.HTTPSConnection("webmaniabr.com")

  # Credenciais de acesso
  headers = {
      'cache-control': "no-cache",
      'content-type': "application/json",
      'x-consumer-key': venda.vendedor.extenduser.empresa.webmania_consumerkey,
      'x-consumer-secret': venda.vendedor.extenduser.empresa.webmania_consumersecret,
      'x-access-token': venda.vendedor.extenduser.empresa.webmania_accesstoken,
      'x-access-token-secret': venda.vendedor.extenduser.empresa.webmania_accesstokensecret
  }

  # Comunicação com a API
  conn.request("GET", "/api/1/nfe/consulta/?chave="+array['chave']+"&ambiente="+array['ambiente'], headers=headers)

  # Retorno da API
  res = conn.getresponse()
  data = res.read()

  # Exibir retorno
  print(data.decode("utf-8"))
