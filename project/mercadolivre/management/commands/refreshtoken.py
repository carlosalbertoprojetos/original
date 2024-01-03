from django.core.management.base import BaseCommand, CommandError
from mercadolivre.models import ContasMercadoLivre
from datetime import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv()



class Command(BaseCommand):
    help = "refresh token mercadolivre"


    def handle(self, *args, **options):
        for conta in ContasMercadoLivre.objects.filter(status='Conectado'):
            print('conta', conta.email)
            headers = {'accept': 'application/json',
                         'content-type':'application/x-www-form-urlencoded',
            }

            params = {'client_id': os.environ.get("CLIENT_ID_MERCADOLIVRE", ""),
            'grant_type':'refresh_token',
            'client_secret': os.environ.get("CLIENT_SECRET_MERCADOLIVRE", ""),
            'refresh_token': conta.refresh_token,
            }
            if not conta.refresh_token: params['refresh_token'] = conta.access_token
            url = 'https://api.mercadolibre.com/oauth/token'
            resposta = requests.post(url=url, headers=headers, data=params)
            if  'message' in resposta.json():
                 print('message', resposta.json()['message'])
                 conta.status = 'Necessário logar nesse email.'
                 conta.save()
            else:
                access_token = resposta.json()['access_token']
                expires_in = resposta.json()['expires_in']
                user_id = resposta.json()['user_id']
                refresh_token = resposta.json()['refresh_token']

                conta.expires_in = expires_in
                conta.access_token = access_token
                conta.refresh_token = refresh_token
                conta.expires_now = datetime.now()
                conta.status = 'Conectado'
                conta.save()
