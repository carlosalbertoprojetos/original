from urllib.parse import urlencode, quote_plus
from urllib.request import urlopen

import datetime
import calendar
from typing import Any
from django.urls import reverse
from django.db.models.query import QuerySet
from django.urls import reverse_lazy as _
from django.shortcuts import redirect, render
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django.db.models import Sum, Count
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView
from django.shortcuts import redirect
import base64
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

from .models import ContasMercadoLivre 

class Contas(LoginRequiredMixin, ListView):
    model = ContasMercadoLivre
    template_name = "mercadolivre/contasList.html"

    def get_context_data(self, **kwargs: Any):
        data =  super().get_context_data(**kwargs)

        #testa status das contas
        contas = ContasMercadoLivre.objects.all()
        for conta in contas:
            access_token = conta.access_token
            if not access_token:
                conta.status = 'Necessário logar nesse email.'
                conta.save()
            else:
                #testa se tem acesso
                headers={'Authorization':'Bearer '+ access_token}
                params={}
                url = 'https://api.mercadolibre.com/users/me'
                resposta = requests.get(url=url, headers=headers, data=params)
                if resposta.status_code != 200:
                    conta.status = 'Necessário logar nesse email.'
                    conta.save()
                



        contas = ContasMercadoLivre.objects.all()
        data['contas'] = contas

        return data

ContasList = Contas.as_view()

@login_required
@permission_required("venda.change_venda")
def mercadolivrevendas(request):
    pass

@login_required
@permission_required("venda.change_venda")
def mercadolivre(request):
    # verifica se o token e valido
    params = urlencode({'response_type':'code', 'client_id': os.environ.get("CLIENT_ID_MERCADOLIVRE", "")})
    f = urlopen("https://auth.mercadolivre.com.br/authorization?%s" % params)
    url = f.geturl()
    response = redirect(url)
    return response

@login_required
@permission_required("venda.change_venda")
def mercadolivreredirect(request):
    if not 'code' in request.GET:
        response = redirect('/mercadolivre/')
        return response
    
    code = request.GET['code']
    headers = {'accept': 'application/json',
                         'content-type':'application/x-www-form-urlencoded',
                        }
    
    params = {'client_id': os.environ.get("CLIENT_ID_MERCADOLIVRE", ""),
            'grant_type':'authorization_code',
            'client_secret': os.environ.get("CLIENT_SECRET_MERCADOLIVRE", ""),
            'code': code,
            'redirect_uri': os.environ.get("REDIRECT_URL_MERCADOLIVRE", ""),
            'code_verifier':'12x3',
                        }
    url = 'https://api.mercadolibre.com/oauth/token'
    resposta = requests.post(url=url, headers=headers, data=params)
    if  'message' in resposta.json():
        return HttpResponseRedirect(reverse('mercadolivre:contas'))
    else:
        access_token = resposta.json()['access_token']
        expires_in = resposta.json()['expires_in']
        user_id = resposta.json()['user_id']
        refresh_token = resposta.json()['refresh_token']

        headers={'Authorization':'Bearer '+ access_token}
        params={}
        url = 'https://api.mercadolibre.com/users/me'
        resposta = requests.get(url=url, headers=headers, data=params)
        first_name = resposta.json()['first_name']
        last_name = resposta.json()['last_name']
        id = resposta.json()['id']
        email = resposta.json()['email']
        #salva status
        conta = ContasMercadoLivre.objects.filter(email=email)
        if conta:
            conta = conta[0]
            conta.first_name = first_name
            conta.last_name = last_name
            conta.codigo = id
            conta.expires_in = expires_in
            conta.access_token = access_token
            conta.refresh_token = refresh_token
            conta.expires_now = datetime.now()
            conta.status = 'Conectado'
            conta.save()
        return HttpResponseRedirect(reverse('mercadolivre:contas'))

