from django.core.management.base import BaseCommand, CommandError
from mercadolivre.models import ContasMercadoLivre
from cliente.models import Cliente
from transportadora.models import Transportadora
from venda.models import Venda, VendaProduto, CondicaoVenda,FormaPagamento, Voltagem, Adesivado, Torneira
from produto.models import Produto
from funcionario.models import ExtendUser
from datetime import datetime, timedelta
from financeiro.models import ContaReceber
from project.constantes import ESTADOS_NOME_SIGLA
import os
import requests
from dotenv import load_dotenv
from django.contrib.auth import get_user_model
from decimal import Decimal
User = get_user_model()

load_dotenv()

class Command(BaseCommand):
    help = "get sales"

    def handle(self, *args, **options):
        for conta in ContasMercadoLivre.objects.filter(status='Conectado'):
            #if conta.email  in ('edersaulocosta@yahoo.com.br'):
            #    continue
                #if conta.email != 'alexsandra@crm.com.br':
                #continue
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
            url = 'https://api.mercadolibre.com/orders/search?&order.status=paid&sort=date_desc&seller=' + str(conta.codigo)
            resposta = requests.get(url=url, headers=headers, data=params)
            dados = resposta.json()
            #import pdb;pdb.set_trace()
            #print('dados', dados)
            if 'results' in dados:
                for result in dados['results']:
                    buyer = result['buyer']
                    seller = result['seller']
                    pedido_id = result['id']
                    print('pedido_id', pedido_id)
                    #import time
                    #time.sleep(3)
                    #if (pedido_id == 2000007161001140):
                    #  import pdb;pdb.set_trace()
                    #import pdb;pdb.set_trace()
                    url_pedido  = 'https://api.mercadolibre.com/orders/%s' % pedido_id
                    resposta_pedido = requests.get(url=url_pedido, headers=headers, data=params)
                    buyer_id =  resposta_pedido.json()['buyer']['id']
                    try:
                        buyer_nickname = resposta_pedido.json()['buyer']['nickname']
                    except:
                        buyer_nickname = ''
                    try:
                      buyer_email = resposta_pedido.json()['buyer']['email']
                    except:
                      buyer_email = ''
                    print(resposta_pedido.json()['buyer'])
                    try:
                        buyer_firstname = resposta_pedido.json()['buyer']['first_name']
                        buyer_lastname = resposta_pedido.json()['buyer']['last_name']
                    except:
                        buyer_firstname = ''
                        buyer_lastname = ''
                    try:
                      buyer_number = resposta_pedido.json()['buyer']['phone']['number']
                      print('buyer_number', buyer_number)
                    except:
                      buyer_number = ''

                    shipping = result['shipping']
                    produtos = result['order_items']
                    tags = result['tags']
                    _produtos = []
                    _produto = {}
                    for produto in produtos:
                        #
                        produto_id = produto['item']['id']
                        title = produto['item']['title']
                        unit_price = produto['unit_price']
                        quantity = produto['quantity']
                        voltagem = ''
                        variations = produto['item']['variation_attributes']
                        descritivo = ''
                        valor_mercadolivre = produto['sale_fee']
                        for variation in variations:
                            if variation['name'] == 'Voltagem':
                                voltagem = variation['value_name']
                            else:
                                descritivo += ' ' + variation['value_name'] + ' <br>'
                        #
                        _produto['produto_id'] = produto_id
                        _produto['title'] = title
                        _produto['unit_price'] = unit_price
                        _produto['quantity'] = quantity
                        _produto['voltagem'] = voltagem
                        _produto['variations'] = variations
                        _produto['valor_mercadolivre'] = valor_mercadolivre
                        _produto['descritivo'] = descritivo

                        tam = ''
                        if 'Bebedouro' in title:
                            if '50' in title:
                                tam = 50
                            elif '100' in title:
                                tam = 100
                            elif '25' in title:
                                tam = 25
                            elif '200' in title:
                                tam = 200
    
                        _produto['tam'] = tam

                        _produtos.append(_produto)
                        print('id', produto_id)
                        print('title', title)
                        print('voltagem', voltagem)
                        print('quantity', quantity)
                        print('unit_price', unit_price)
                        print('valor_mercadolivre', valor_mercadolivre)
                    payments = result['payments']
                    status = ''
                    total = 0
                    for payment in payments:
                        #print('payment', payment)
                        status = payment['status']
                        #nimport pdb;pdb.set_trace()
                        if status == 'approved':
                          total  += payment['transaction_amount']
                          date_approved = payment['date_approved']

                        #buyer_id = buyer['id']
                        #buyer_nickname = buyer['nickname']
                        #buyer_firstname = buyer['first_name']
                        #pega os dados do endereco para envio

                        #url_user = 'https://api.mercadolibre.com/users/%s' % user_id
                        #url_pay = 'https://api.mercadopago.com/v1/payments/%s' % payment_id
                    if 1:#total:
                        if not shipping:
                            pais = cidade = rua = numero = cep = recebedor = comentario = estado = bairro = telefone_recebedor = ''
                        else:
                          url_shipping = 'https://api.mercadolibre.com/shipments/%s' % shipping['id']
                          resposta = requests.get(url=url_shipping, headers=headers, data=params)
                          endereco = resposta.json()
                          #address =  endereco['receiver_address']
                          pais = cidade = rua = numero = cep = recebedor = comentario = estado = bairro = telefone_recebedor = ''
                          if  'receiver_address' in endereco:
                            try:                   
                                pais = endereco['receiver_address']['country']['name']
                                cidade = endereco['receiver_address']['city']['name']
                                rua = endereco['receiver_address']['street_name']
                                numero = endereco['receiver_address']['street_number']
                                cep = endereco['receiver_address']['zip_code']
                                recebedor = endereco['receiver_address']['receiver_name']
                                comentario = endereco['receiver_address']['comment']
                                estado = endereco['receiver_address']['state']['name']
                                bairro = endereco['receiver_address']['neighborhood']['name']
                                if not bairro:
                                    bairro = 'não informado'
                                telefone_recebedor = endereco['receiver_address']['receiver_phone']
                                print('telefone recebedor', telefone_recebedor)
                            except:
                                pass
                        # pega os dados do compradora
                        #url_buyer = 'https://api.mercadolibre.com/users/76922011'

                        #resposta = requests.get(url=url_buyer, headers=headers, data=params)
                        url_billing = 'https://api.mercadolibre.com/orders/%s/billing_info' % pedido_id
                        resposta = requests.get(url=url_billing, headers=headers, data=params)

                        try:
                            tipo_documento = resposta.json()['billing_info']['doc_type']
                            doc_number = resposta.json()['billing_info']['doc_number']
                        except:
                            tipo_documento = None
                            doc_number = None
                        
                        # verifica se o produto e bebedouro
                        continua = False
                        for produto in _produtos:
                            if 'Bebedouro' in produto['title'] and 'Boia' not in produto['title'] and 'Refil Multiuso' not in produto['title']:
                                continua = True


                        if status != 'approved':
                            continue
                        if date_approved:
                            data_aprovada = datetime.strptime(date_approved[0:10] + ' ' + date_approved[11:16],"%Y-%m-%d %H:%M").strftime('%Y-%m-%d %H:%M')
                            if data_aprovada < '2023-11-05 00:00':
                                print('venda anterior, nao insere')
                                continue

                        if not continua:
                            print('nao vai inserir pq nao e venda de bebedouro')

                        if continua:
                            cliente = None
                            venda = None
                            print('vai inserir')

                            # adiciona o clientea
                            _recebedor = recebedor
                            if buyer_firstname:
                                _recebedor = '%s %s' % (buyer_firstname, buyer_lastname)
                            
                            status_expedicao = None
                            if tipo_documento == 'CPF':
                                cliente = Cliente.objects.filter(cpf = doc_number)
                                #if doc_number == '11719449775': import pdb;pdb.set_trace()
                                if cliente:
                                    cliente = cliente[0]
                                    cliente.mercadolivre_id = buyer_id
                                else:
                                    cliente = Cliente.objects.create(cpf=doc_number, nome=_recebedor, nome_fantasia=buyer_nickname, mercadolivre_id=buyer_id)
                            elif tipo_documento == 'CNPJ':
                                cliente = Cliente.objects.filter(cnpj = doc_number)
                                if cliente:
                                    cliente = cliente[0]
                                else:
                                    cliente = Cliente.objects.create(cnpj=doc_number, nome=_recebedor, nome_fantasia=buyer_nickname, mercadolivre_id=buyer_id)

                            else:
                                #cliente nao tem dados como cnpj ou cnpj
                                status_expedicao = 'Combinar Entrega'
                                cliente = Cliente.objects.filter(mercadolivre_id = buyer_id)
                                if cliente:
                                    cliente = cliente[0]
                                else:
                                    cliente = Cliente.objects.create(mercadolivre_id=buyer_id, nome=_recebedor, nome_fantasia=buyer_nickname)
                                #import pdb;pdb.set_trace()
                            # adiciona endereco
                            if not cliente:
                                continue
                            
                            if cliente.cep or cliente.logradouro:
                                if cliente.cep != cep or cliente.logradouro != rua:
                                    _descricao_antiga = cliente.descricao
                                    cliente.descricao =  '%s <br>Endereco antigo: Pais: %s Estado: %s Cidade: %s Cep: %s Bairro: %s Rua:%s Numero: %s' % (_descricao_antiga, cliente.pais, cliente.estado, cliente.cidade, cliente.cep, cliente.bairro, cliente.logradouro, cliente.numero)
                                    cliente.save()
                            #

                            #venda = Venda.objects.filter(codigo_mercadolivre = pedido_id)
                            #if venda:
                            #    continue





                            print('date_approved', date_approved)
                            print('total', unit_price)
                            print('descritivo', descritivo)
                            print('conta email', conta.email)
                            print('status', status)
                            cliente.cep = cep
                            cliente.pais = pais
                            if estado:
                                cliente.estado = ESTADOS_NOME_SIGLA[estado.upper()]
                            if not cliente.cidade:
                                cliente.cidade = cidade
                            if not cliente.bairro:
                                cliente.bairro = bairro
                            if not cliente.logradouro:
                                cliente.logradouro = rua
                            if not cliente.numero:
                                cliente.numero = numero
                            if comentario:
                                if len(comentario) > 60: comentario = comentario[0:60]
                            if not cliente.complemento:
                                cliente.complemento = comentario
                            cliente.save()
        
                            if cliente.tel_principal and buyer_number:
                                if cliente.tel_principal != buyer_number and cliente.tel_principal:
                                    if cliente.descricao:
                                        cliente.descricao += '<br> O telefone antigo e %s ' % cliente.tel_principal
                                    else:
                                        cliente.descricao = '<br> O telefone antigo e %s ' % cliente.tel_principal
                            if buyer_number:
                              cliente.tel_principal = buyer_number
                            elif telefone_recebedor:
                              cliente.tel_principal = telefone_recebedor

                            cliente.save()

                            id_transportadora = 24
                            if cliente.estado == 'RJ':
                                id_transportadora = 28

                            venda = Venda.objects.filter(codigo_mercadolivre = pedido_id)
                            if venda: 
                                continue


                            extenduser = ExtendUser.objects.filter(mercadolivre_user__contains=seller['nickname'])
                            if extenduser:
                                extenduser = extenduser[0]
                                vendedor = extenduser.usuario
                            else:
                                vendedor = User.objects.get(username='mercadolivre')
                            
                            if venda:
                                venda = venda[0]
                            else:
                                condicaovenda = CondicaoVenda.objects.get(nome='30 dias')
                                formapagto = FormaPagamento.objects.get(nome='Mercado Pago')
 
                                if not date_approved:
                                    continue
                                data_aprovada = datetime.strptime(date_approved[0:10] + ' ' + date_approved[11:16] ,"%Y-%m-%d %H:%M").strftime('%Y-%m-%d %H:%M')
                                transportadora = Transportadora.objects.get(id=id_transportadora)
                                
                                detalhes = 'Conta da venda %s' % seller['nickname']
                                #if buyer_nickname == 'GOMESJALISON20221204112231': import pdb;pdb.set_trace()
                                venda = Venda.objects.create(
                                    codigo_mercadolivre = pedido_id,
                                    nickname_mercadolivre = buyer_nickname,
                                    cliente = cliente,
                                    data_pedido = data_aprovada,
                                    valor_venda = total,
                                    taxa_mercadolivre = valor_mercadolivre,
                                    subtotal= total - valor_mercadolivre,
                                    vendedor=vendedor,
                                    detalhes = detalhes,
                                    status_venda='expedicao',
                                    condicaopgto=condicaovenda,
                                    formapgto=formapagto,
                                    dias_prim_par = 30,
                                    dias_outras_par = 0,
                                    parcelas = 1,
                                    transportadora=transportadora,
                                    quemrecebe_mercadolivre = recebedor,
                                    telefonequemrecebe_mercadolivre = telefone_recebedor,
                                    
                                )
                                if status_expedicao:
                                    venda.status_expedicao = status_expedicao
                                    venda.save()

                                for _produto in _produtos:
                                     produto = Produto.objects.filter(nome__contains=_produto['tam'])
                                     if produto:
                                        produto = produto[0]
                                        voltagem = Voltagem.objects.get(nome='Nao sei')
                                        if tam == 25:
                                            torneira = Torneira.objects.get(nome='2t')
                                        elif tam == 50:
                                            torneira = Torneira.objects.get(nome='2t')
                                        elif tam == 100:
                                            torneira = Torneira.objects.get(nome='3t')
                                        elif tam == 200:
                                            torneira = Torneira.objects.get(nome='4t')
                                        
                                        if '220' in _produto['voltagem']:
                                            _voltagem = Voltagem.objects.filter(nome__contains='220')
                                            if _voltagem:
                                                voltagem = _voltagem[0]

                                        if '110' in _produto['voltagem'] or '127' in  _produto['voltagem']:
                                                _voltagem = Voltagem.objects.filter(nome__contains='127')
                                                if _voltagem:
                                                    voltagem = _voltagem[0]

                                        adesivado = Adesivado.objects.get(nome='Não')
                                        vendaproduto = VendaProduto.objects.create(
                                            venda=venda,
                                            produto = produto,
                                            quantidade = _produto['quantity'],
                                            preco = _produto['unit_price'],
                                            subtotal = float(_produto['quantity']) * (_produto['unit_price']),
                                            torneira = torneira,
                                            adesivado = adesivado,
                                            voltagem=voltagem
                                        )
                                        ContaReceber.objects.create(
                                            venda = venda,
                                            parcela = 1,
                                            valor = Decimal(total - valor_mercadolivre),
                                            datavencimento= datetime.strptime(date_approved[0:10],"%Y-%m-%d") + timedelta(days=30),
                                            boleto=None,
                                            comprovante=None,
                                            responsavel=None,
                                            formapgto = formapagto,
                                            dados_boleto = None,
                                            detalhes='venda feita pelo mercado livre, aguardando liberação pagamento'
                                        )


