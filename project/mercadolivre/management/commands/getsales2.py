from django.core.management.base import BaseCommand, CommandError
from mercadolivre.models import ContasMercadoLivre
from venda.models import Venda
from datetime import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv()



class Command(BaseCommand):
    help = "get sales"


    def handle(self, *args, **options):
        for conta in ContasMercadoLivre.objects.filter(status='Conectado'):
            print('conta', conta.email)
            headers={'Authorization':'Bearer '+ conta.access_token}
            params={}
            url = 'https://api.mercadolibre.com/orders/search?&order.status=paid&sort=date_desc&seller=' + str(conta.codigo)
            resposta = requests.get(url=url, headers=headers, data=params)
            dados = resposta.json()
            if 'results' in dados:
                for result in dados['results']:
                    buyer = dados['results'][0]['buyer']
                    produtos = result['order_items']
                    for produto in produtos:
                        id = produto['item']['id']
                        title = produto['item']['title']
                        voltagem = ''
                        variations = produto['item']['variation_attributes']
                        descritivo = ''
                        sales_item = produto['sale_fee']
                        for variation in variations:
                            if variation['name'] == 'Voltagem':
                                voltagem = variation['value_name']
                            else:
                                descritivo += ' ' + variation['value_name'] + ' <br>'

                    payments = result['payments']
                    status = ''
                    total = ''
                    for payment in payments:
                        status = payment['status']
                        total = payment['total_paid_amount']
                        date_approved = payment['date_approved']
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
                        print('id', id)
                        print('title', title)
                        print('voltagem', voltagem)
                        print('status', status)
                        print('date_approved', date_approved)
                        print('total', total)
                        print('descritivo', descritivo)
                        print('conta email', conta.email)

                        # insere vendas
                        #
                        #
                        address =  endereco['receiver_address']
                        pais = endereco['receiver_address']['country']['name']
                        rua =  endereco['receiver_address']['address_line']
                        cidade = endereco['receiver_address']['city']['name']
                        rua = endereco['receiver_address']['street_name']
                        cep = endereco['receiver_address']['zip_code']
                        recebedor = endereco['receiver_address']['receiver_name']
                        comentario = endereco['receiver_address']['comment']
                        estado =  endereco['receiver_address']['state']['name']
                        bairro =  endereco['receiver_address']['neighborhood']['name']
                        telefone_recebedor = endereco['receiver_address']['receiver_phone']


                        venda = Venda.objects.filter(mercadolivre_id = codigo)
                        if not venda:
                            #insere a venda
                            Venda.objects.create(
                                cliente = cliente,
                                data_pedido = date_approved,
                                transportadora = None, 
                                valor_frete = 0,
                                vendedor = xx,
                                valor_venda = total,
                                valor_mercadolivre = ,
                                subtotal = total - valor_mercadolivre,
                                status_venda = 'orcamento',
                                condicaopgto = 'avista',
                                dias_prim_par = 0,
                                dias_outras_par = 0,
                                parcelas = 1,
                                formapagto = 'mercadolivre',
                                detalhes = descritivo,
                                codigo_mercadolivre = codigo
                            )
    

