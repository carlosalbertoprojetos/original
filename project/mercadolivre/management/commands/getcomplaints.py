from django.core.management.base import BaseCommand, CommandError
<<<<<<< HEAD
from mercadolivre.models import ContasMercadoLivre
=======
from mercadolivre.models import ContasMercadoLivre, PacksMercadoLivre, MensagensMercadoLivre
>>>>>>> 3ae5c7515821ed97299fd925e6aa810d88755c13
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
    help = "get compleints"

    def handle(self, *args, **options):
        for conta in ContasMercadoLivre.objects.filter(status='Conectado'):
            print('conta', conta.email)
            #if conta.email != 'edersaulocosta@yahoo.com.br':
            #if conta.email != 'alexsandrahelena@hotmail.com':
            #if conta.email != 'alexsandra@crm.com.br':
            #    continue
            headers={'Authorization':'Bearer '+ conta.access_token}
            params={}
            #codig = '2000006735183108'
            #url = 'https://api.mercadolibre.com/merchant_orders/' + codig #str(conta.codigo)
            url = 'https://api.mercadopago.com/v1/payments/search?sort=money_release_date&criteria=desc'
            url = 'https://api.mercadolibre.com/billing/integration/periods'
            url = 'https://api.mercadolibre.com/billing/integration/monthly/periods'
            url = 'https://api.mercadolibre.com/billing/integration/monthly/periods?group=MP&document_type=BILL&offset=1&limit=2'
            #url = 'https://api.mercadolibre.com/billing/integration/periods/key/2023-12-01/group/ML/details?document_type=BILL'
            url = 'https://api.mercadolibre.com/billing/integration/periods/key/2023-12-03/group/ML/payment/details'
            url = 'https://api.mercadolibre.com/billing/integration/periods/key/2023-12-04/group/ML/details?document_type=CREDIT_NOTE'
            url = 'https://api.mercadolibre.com/billing/integration/monthly/periods?group=ML&document_type=BILL'
            url = 'https://api.mercadolibre.com/billing/integration/periods/key/2023-12-03/documents?group=MP&document_type=BILL'
            url = 'https://api.mercadolibre.com/billing/integration/periods/key/2023-12-06/summary?group=MP&document_type=CREDIT_NOTE'
            url = 'https://api.mercadolibre.com/billing/integration/periods/key/2023-11-06/group/ML/details?document_type=CREDIT_NOTE'
            url = 'https://api.mercadolibre.com/billing/integration/group/ML/perceptions/details?document_id=66382261258&tax_type=CIVA'
            ###url = 'https://api.mercadolibre.com/billing/integration/periods/key/2023-12-01/group/ML/insurtech/details?document_type=BILL&detail_type=bonus'
            url = 'https://api.mercadolibre.com/billing/integration/periods/key/2023-12-01/group/ML/payment/details'
            url = 'https://api.mercadolibre.com/v1/claims/search?stage=dispute&sort=desc'
            url = 'https://api.mercadolibre.com/v1/claims/5237953255/messages'
            url = 'https://api.mercadolibre.com/messages/unread?tag=post_sale'
            url = 'https://api.mercadolibre.com/messages/packs/2000007153944902/sellers/468673808?tag=post_sale'
            params = {}

            resposta = requests.get(url=url, headers=headers, data=params)
            dados = resposta.json()
            print(dados)
            import pdb;pdb.set_trace()
            #print('dados', dados)
            if 'results' in dados:
            url = 'https://api.mercadolibre.com/v1/claims/336156794/messages'
            url = 'https://api.mercadolibre.com/messages/unread?role=seller&tag=post_sale'
            #url = 'https://api.mercadolibre.com/messages/packs/2000007153944902/sellers/468673808?tag=post_sale'
            params = {}

            resposta = requests.get(url=url, headers=headers, data=params)
            conversas = resposta.json()
            print(conversas)           
            #conversas = {'user_id': 200884628, 'total': 4, 'results': [{'resource': '/packs/2000004558523409/sellers/1133207496', 'count': 1}, {'resource': '/packs/2000004554390311/sellers/475750649', 'count': 1}, {'resource': '/packs/2000004597893399/sellers/1133207496', 'count': 1}, {'resource': '/packs/2000004620266767/sellers/227319997', 'count': 1}]}
            conversas = conversas['results']
            import pdb;pdb.set_trace()
            for conversa in conversas:
                resource =  conversa['resource']
                url = 'https://api.mercadolibre.com/messages/' + resource + '?tag=post_sale'
                resposta = requests.get(url=url, headers=headers, data=params)
                import pdb;pdb.set_trace()
            
            #print('dados', dados)
            continue
            if 'results' in conversas:
                for result in dados['results']:
                    #print('result', result)
                    money_release_status = result['money_release_status']
                    print('money_release_status', money_release_status)
                    if 1:# money_release_status == 'released':
                        transaction_amount = result['transaction_amount']
                        transaction_amount_refunded = result['transaction_amount_refunded']
                        date_approved = result['date_approved']
                        print('transaction_amount', transaction_amount, 'transaction_amount_refunded', transaction_amount_refunded, 'date_approved',date_approved)
                        #print(result)
                        import pdb;pdb.set_trace()

                    continue

                    buyer = result['buyer']
                    seller = result['seller']
                    pedido_id = result['id']
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
                        total  += payment['transaction_amount']
                        date_approved = payment['date_approved']

                        buyer_id = buyer['id']
                        buyer_nickname = buyer['nickname']
                        #pega os dados do endereco para envio

                        #url_user = 'https://api.mercadolibre.com/users/%s' % user_id
                        #url_pay = 'https://api.mercadopago.com/v1/payments/%s' % payment_id
                    if 1:#total:
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
                            except:
                                pass
                        # pega os dados do compradora
                        #url_buyer = 'https://api.mercadolibre.com/users/%s' % endereco['receiver_id']
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
                            data_aprovada = datetime.strptime(date_approved[0:10],"%Y-%m-%d").strftime('%Y-%m-%d')
                            #if data_aprovada < '2023-11-05':
                            #    print('venda anterior, nao insere')
                            #    continue

                        if not continua:
                            print('nao vai inserir pq nao e venda de bebedouro')

                        if continua:
                            cliente = None
                            venda = None
                            print('vai inserir')

                            # adiciona o clientea
                            if tipo_documento == 'CPF':
                                cliente = Cliente.objects.filter(cpf = doc_number)
                                if cliente:
                                    cliente = cliente[0]
                                    cliente.mercadolivre_id = buyer_id
                                else:
                                    cliente = Cliente.objects.create(cpf=doc_number, nome=recebedor, nome_fantasia=buyer_nickname, mercadolivre_id=buyer_id)
                            elif tipo_documento == 'CNPJ':
                                cliente = Cliente.objects.filter(cnpj = doc_number)
                                if cliente:
                                    cliente = cliente[0]
                                else:
                                    cliente = Cliente.objects.create(cnpj=doc_number, nome=recebedor, nome_fantasia=buyer_nickname, mercadolivre_id=buyer_id)

                            # adiciona endereco
                            if not cliente:
                                continue
                            
                            if cliente.cep or cliente.logradouro:
                                if cliente.cep != cep or cliente.logradouro != rua:
                                    _descricao_antiga = cliente.descricao
                                    cliente.descricao =  '%s <br>Endereco antigo: Pais: %s Estado: %s Cidade: %s Cep: %s Bairro: %s Rua:%s Numero: %s' % (_descricao_antiga, cliente.pais, cliente.estado, cliente.cidade, cliente.cep, cliente.bairro, cliente.logradouro, cliente.numero)
                                    cliente.save()
                            #

                            print('date_approved', date_approved)
                            print('total', unit_price)
                            print('descritivo', descritivo)
                            print('conta email', conta.email)
                            print('status', status)
                            cliente.cep = cep
                            cliente.pais = pais
                            if estado:
                                cliente.estado = ESTADOS_NOME_SIGLA[estado.upper()] 
                            cliente.cidade = cidade
                            cliente.bairro = bairro
                            cliente.logradouro = rua
                            cliente.numero = numero
                            cliente.save()
        
                            if cliente.tel_principal:
                                if cliente.tel_principal != telefone_recebedor:
                                    cliente.descricao += '<br> O telefone antigo e %s ' % cliente.tel_principal
                                    cliente.save()
                            cliente.tel_principal = telefone_recebedor
                            cliente.save()
                            if pedido_id == '2000006620322858':
                                import pdb;pdb.set_trace()
                            
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
                                data_aprovada = datetime.strptime(date_approved[0:10],"%Y-%m-%d").strftime('%Y-%m-%d')
                                transportadora = Transportadora.objects.get(nome='Fabrica entrega')
                                detalhes = 'Conta da venda %s' % seller['nickname']
                                venda = Venda.objects.create(
                                    codigo_mercadolivre = pedido_id,
                                    cliente = cliente,
                                    data_pedido = data_aprovada,
                                    valor_venda = total,
                                    taxa_mercadolivre = valor_mercadolivre,
                                    subtotal= total - valor_mercadolivre,
                                    vendedor=vendedor,
                                    detalhes = detalhes,
                                    status_venda='autorizado',
                                    condicaopgto=condicaovenda,
                                    formapgto=formapagto,
                                    dias_prim_par = 30,
                                    dias_outras_par = 0,
                                    parcelas = 1,
                                    transportadora=transportadora,
                                    
                                )
                                for _produto in _produtos:
                                     produto = Produto.objects.filter(nome__contains=_produto['tam'])
                                     if produto:
                                        produto = produto[0]
                                        voltagem = Voltagem.objects.get(nome='Nao sei')
                                        if not voltagem: import pdb;pdb.set_trace()
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

                                        adesivado = Adesivado.objects.get(nome='Sim')
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


