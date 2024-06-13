from django.core.management.base import BaseCommand, CommandError
from venda.models import Venda
import os
import requests
from dotenv import load_dotenv
from integracoes.transportadoras.tnt import pega_dados_tnt
from integracoes.transportadoras.pajucara import pega_dados_pajucara
from django.db.models import Q
from mercadolivre.models import ContasMercadoLivre
from cliente.models import Cliente
from transportadora.models import Transportadora
from venda.models import Venda, VendaProduto, CondicaoVenda,FormaPagamento, Voltagem, Adesivado, Torneira
from produto.models import Produto
from funcionario.models import ExtendUser
from datetime import datetime, timedelta
from financeiro.models import ContaReceber
from django.contrib.auth import get_user_model
from integracoes.transportadoras.pajucara import pega_dados_pajucara
from integracoes.transportadoras.tnt import pega_dados_tnt
from integracoes.transportadoras.vhz import pega_dados_vhz
from integracoes.transportadoras.jeolog import pega_dados_jeolog
User = get_user_model()
import json
load_dotenv()


class Command(BaseCommand):
    help = "atualiza status das vendas do mercadolivre"


    def handle(self, *args, **options):
        print('##################')
        for conta in ContasMercadoLivre.objects.filter(status='Conectado'):
            #if conta.email not in ('edersaulocosta@yahoo.com.br'):
            #    continue
            #if conta.email != 'alexsandra@crm.com.br':
            #    continue
            #if conta.email != 'alexsandrahelena@hotmail.com':
            #    continue
            #if conta.email != 'patriciagarbo@yahoo.com.br':
            #    continue
            #if conta.email != 'alexsandra@intip.com.br':
            #    continue
            print('conta', conta.email)
            #import pdb;pdb.set_trace()
            headers={'Authorization':'Bearer '+ conta.access_token}
            params={}
            offsets = [0,50] #offsets = [0,50,100]
            for offset in offsets:
                url = 'https://api.mercadolibre.com/orders/search?&order.status=paid&sort=date_desc&offset=%s&seller=%s' % (str(offset), str(conta.codigo))
                resposta = requests.get(url=url, headers=headers, data=params)

                dados = resposta.json()
                #import pdb;pdb.set_trace()
                #print('dados', dados)
                if 'results' in dados:
                    for result in dados['results']:
                        buyer = result['buyer']
                        seller = result['seller']
                        pedido_id = result['id']
                        # print('pedido_id', pedido_id)
                        #import time
                        #time.sleep(3)
                        #if (pedido_id != 2000007806094498 ):
                        #    continue
                        #else:
                        #    print('.')
                        #    import pdb;pdb.set_trace()
                        #if (pedido_id != 2000007466084416):
                        #    continue
                        #import pdb;pdb.set_trace()
                        params = {}
                        url_pedido  = 'https://api.mercadolibre.com/orders/%s' % pedido_id
                        resposta_pedido = requests.get(url=url_pedido, headers=headers, data=params)
                        tags = resposta_pedido.json()['tags']
                        if 'catalog' in tags: tags.remove('catalog')
                        if tags == ['paid', 'not_delivered']:
                            # tem venda pendente enviar
                            if not resposta_pedido.json()['shipping']['id']:
                                continue

                            url_shipping = 'https://api.mercadolibre.com/shipments/%s' % resposta_pedido.json()['shipping']['id']
                            #import pdb;pdb.set_trace()
                            try:
                                resposta = requests.get(url=url_shipping, headers=headers, data=params)
                            except:
                                print('erro requieiscao api mercadoivre shipping')
                                continue
                            #print(resposta.json()['status'])
                            if resposta.json()['status'] == 'pending':
                                venda = Venda.objects.filter(codigo_mercadolivre=pedido_id)
                                if venda:
                                    venda = venda[0]
                                    if venda.status_venda == 'enviado' and venda.status_posvenda == 'Concluido':
                                        continue
                                    #if venda.id == 1299:
                                    #import pdb;pdb.set_trace()
                                    print(venda.cliente.nome)
                                    #if venda.id==1581: import pdb;pdb.set_trace()
                                    if venda.numero_nf:
                                        numero_nf = venda.numero_nf
                                        tracking_number = None
                                        mensagem = None
                                        #achou a venda, agora ve se o pedido ja foi enviado
                                        if venda.transportadora.id == 22224: # tnt 24
                                            previsao, situacao = pega_dados_tnt(numero_nf, cnpj='51905769000190')
                                            if previsao:
                                                mensagem = """Olá, seu produto já está a caminho! 
                                                Previsão de chegada: %s
                                                Segue o código de rastreio:
                                                https://radar.tntbrasil.com.br/radar/public/localizacaoSimplificada.do
                                                CNPJ: 51905769000190
                                                NF: %s
                                                """ % (previsao, numero_nf)
                                                tracking_number = 'tnt%s' % numero_nf 

                                        elif venda.transportadora.id == 28: #pajucara   
                                            previsao, situacao =  pega_dados_pajucara(venda.chave)
                                            if venda.cliente.cnpj:
                                                cpforcnpj = venda.cliente.cnpj.number
                                            else:
                                                cpforcnpj = venda.cliente.cpf.number
                                            if previsao:
                                                mensagem = """Olá, seu produto já está a caminho! Segue o código de rastreio:
                                                Selecionar campo  destinatario.
                                                https://cliente.viapajucara.com.br/rastrear
                                                Previsão de chegada: %s
                                                cnpj ou cnpj: %s
                                                nf %s
                                                Gentileza conferir o produto quando chegar e se tiver com avaria recusar recebimento.
                                                """ % (previsao, cpforcnpj, numero_nf)
                                                tracking_number = 'paju%s' % numero_nf
                                        elif venda.transportadora.id == 48: #aguia-sul
                                            previsao, situacao =  pega_dados_pajucara(venda.chave)
                                            if venda.cliente.cnpj:
                                                cpforcnpj = venda.cliente.cnpj.number
                                            else:
                                                cpforcnpj = venda.cliente.cpf.number
                                            if previsao:
                                                mensagem = """Olá, seu produto já está a caminho! Segue o código de rastreio:
                                                Selecionar campo  destinatario.
                                                https://www.aguiasul.com.br/novo/
                                                Clicar em rastreio
                                                Previsão de chegada: %s
                                                cnpj ou cnpj: 51905769000190
                                                nota fiscal : %s
                                                Gentileza conferir o produto quando chegar e se tiver com avaria recusar recebimento.
                                                """ % (previsao, numero_nf)
                                                tracking_number = 'aguiasul%s' % numero_nf
                                        elif venda.transportadora.id == 47:
                                            previsao, situacao =  pega_dados_pajucara(venda.chave)
                                            if previsao:
                                                mensagem = """Olá, seu produto já está a caminho! Segue o código de rastreio:
                                                https://www.mfnlogistica.com.br/rastreamento/
                                                Previsão de chegada: %s
                                                Por nota fiscal:
                                                CNPJ: 51905769000190
                                                NF: %s

                                                """ % (previsao, numero_nf)
                                                tracking_number = 'vhz%s' % numero_nf
                                            
                                        elif venda.transportadora.id == 32: #vhz
                                            previsao, situacao =  pega_dados_pajucara(venda.chave)
                                            if previsao:
                                                mensagem = """Olá, seu produto já está a caminho! Segue o código de rastreio:
                                                http://www.vhztransporte.com.br/rastreamento.php
                                                Previsão de chegada: %s
                                                Por nota fiscal:
                                                CNPJ: 51905769000190
                                                NF: %s
        
                                                """ % (previsao, numero_nf)
                                                tracking_number = 'vhz%s' % numero_nf 
                                        elif venda.transportadora.id == 34: #jeolog
                                            previsao, situacao =  pega_dados_pajucara(venda.chave)
                                            if previsao:
                                                mensagem = """Olá, seu produto já está a caminho! Segue o código de rastreio:
                                                https://jeolog.com.br/rastreamento/
                                                Previsão de chegada: %s
                                                Por nota fiscal:
                                                CNPJ: 51905769000190
                                                NF: %s
                                                Gentileza conferir o produto quando chegar e se tiver com avaria recusar recebimento.
                                                """ % (previsao, numero_nf)
                                                tracking_number = 'vhz%s' % numero_nf 

                                        elif venda.transportadora.id == 45: #trm
                                            previsao, situacao =  pega_dados_pajucara(venda.chave)
                                            if previsao:
                                                mensagem = """Olá, seu produto já está a caminho! Segue o código de rastreio:
                                                https://trmlogistica.com.br/
                                                Previsão de chegada: %s
                                                Por nota fiscal:
                                                CNPJ: 51905769000190
                                                NF: %s
                                                Gentileza conferir o produto quando chegar e se tiver com avaria recusar recebimento.
                                                """ % (previsao, numero_nf)
                                                tracking_number = 'vhz%s' % numero_nf
                                        elif venda.transportadora.id == 40: #luz
                                            previsao, situacao =  pega_dados_pajucara(venda.chave)
                                            if previsao:
                                                mensagem = """Olá, seu produto já está a caminho! Segue o código de rastreio:
                                                https://ssw.inf.br/2/rastreamento
                                                Previsão de chegada: %s
                                                Por nota fiscal:
                                                CNPJ: 51905769000190
                                                NF: %s
                                                Gentileza conferir o produto quando chegar e se tiver com avaria recusar recebimento.
                                                """ % (previsao, numero_nf)
                                                tracking_number = 'luz%s' % numero_nf


                                        if mensagem:
                                            if previsao:
                                                params = {}
                                                # ainda nao informou que esta a caminho, então informa
                                                #import pdb;pdb.set_trace()
                                                if venda.transportadora.id == 32: #vhz
                                                    data_previsao = datetime.strptime(previsao, "%d/%m/%y")
                                                elif venda.transportadora.id == 34: #jeolog
                                                    data_previsao = datetime.strptime(previsao, "%d/%m/%y")
                                                elif venda.transportadora.id == 28: #pajucara
                                                    #import pdb;pdb.set_trace()
                                                    #meses = {'janeiro':'01', 'fevereiro':'02','março':'03', 'abril':'04', 'maio':'05', 'junho':'06', 'julho':'07', 'agosto':'08', 'setembro':'09', 'outubro':'10', 'novembro':'11', 'dezembro':'12'}
                                                    #_previsao = previsao.split()
                                                    #dia = _previsao[0]
                                                    #mes = meses[_previsao[2]]
                                                    #mes = _previsao[1]
                                                    #ano='24'
                                                    #__previsao = '%s/%s/%s' % (dia, mes, ano)
                                                    data_previsao = datetime.strptime(previsao, "%d/%m/%y")
                                                else:
                                                    try:
                                                      data_previsao = datetime.strptime(previsao, "%d/%m/%y")
                                                    except:
                                                      data_previsao = datetime.strptime(previsao, "%d/%m/%Y")
                                                data_hoje = datetime.now()
                                                diferenca = data_previsao - data_hoje
                                                horas_faltante = diferenca.days * 24 + 24
                                                params = {"speed": horas_faltante,"status":"shipped","tracking_number": tracking_number,"receiver_id": resposta_pedido.json()['buyer']['id']}
                                                url_caminho = 'https://api.mercadolibre.com/shipments/%s' % resposta_pedido.json()['shipping']['id']
                                                resposta_caminho = requests.put(url=url_caminho, headers=headers, json=params)
                                                params = {"from" : {"user_id": resposta_pedido.json()['seller']['id'],},"to": {"user_id" : resposta_pedido.json()['buyer']['id']},"text": mensagem,}
                                                url_mensagem = "https://api.mercadolibre.com/messages/packs/%s/sellers/%s?tag=post_sale" % (pedido_id, resposta_pedido.json()['seller']['id'])
                                                #url_mensagem = 'https://api.mercadolibre.com/messages/action_guide/packs/%s/?tag=post_sale' % pedido_id
                                                params =json.dumps(params)
                                                resposta_mensagem = requests.post(url=url_mensagem, headers=headers, data=params)
                                                if resposta_mensagem.status_code in [200,201] or resposta_caminho.status_code == 200:
                                                    venda.status_venda = 'enviado'
                                                    venda.status_expedicao = 'Enviado'
                                                    venda.status_posvenda = 'Concluido'
                                                    venda.save()
                                                    print('pedido atualizado')                              
                            else:
                                if resposta.json()['status'] == 'shipped':
                                    venda = Venda.objects.filter(codigo_mercadolivre=pedido_id)
                                    if venda:
                                        venda = venda[0]
                                        if venda.status_venda != 'enviado':
                                            venda.status_venda = 'enviado'
                                            venda.status_expedicao = 'Enviado'
                                            venda.status_posvenda = 'Concluido'
                                            venda.save()
                                            print('pedido atualizado')  
                                #print('pedido ja foi enviado')

                        """
                        if venda.transportadora.id == 24:
                            try:
                                data, situacao = pega_dados_tnt(venda.numero_nf)
                                if situacao == 'Entrega realizada':
                                    venda.status_venda='entregue'
                                    venda.status = 'entregue'
                                    venda.status_expedicao = 'entregue'
                                    venda.save()
                                    print('venda', venda.id, 'numero nf', venda.numero_nf, situacao, data)
                                else:
                                    print('situacao  ', situacao)
                            except:
                                pass
                        """

                


    
