from django.core.management.base import BaseCommand, CommandError
from venda.models import Venda
import os
import requests
from dotenv import load_dotenv
from django.db.models import Q
from cliente.models import Cliente
from transportadora.models import Transportadora
from integracoes.transportadoras.cotacao.ssw import realiza_cotacao
load_dotenv()


class Command(BaseCommand):
    help = "get cotacoes"

    def handle(self, *args, **options):
        vendas = Venda.objects.filter(status_expedicao = 'Fazer Cotação')
        for venda in vendas:
            print(venda)
            #pajucara
            cnpj = '51905769000190'
            cep = '32671102'
            if venda.cliente.cnpj:
                cnpjdestino = str(venda.cliente.cnpj)
            else:
                cnpjdestino = str(venda.cliente.cpf)
            cepdestino = venda.cliente.cep
            total = float(venda.subtotal)
            #pajucara
            if venda.cliente.estado in ['MG', 'SP', 'RJ', 'PR', 'RS', 'SC']:
                url = "https://cliente.viapajucara.com.br/login"
                password = 'ORIGINAL2023'
                cotacao, frete, prazo = realiza_cotacao(url, cnpjOrigem=cnpj, password=password, cnpjDestinatario=cnpjdestino, cepOrigem=cep, cepDestino=cepdestino, valor=total, qtde=1, peso=42, cubagem=0.86)
                import pdb;pdb.set_trace()
                # jeolog
                #atual
                # vhz
                # ?
            #    realiza_cotacao(cnpjdestinatario=venda.cpforcnpj
                #print(realiza_cotacao('31240151905769000190550010000004901205879800'))