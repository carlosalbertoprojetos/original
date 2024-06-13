from datetime import datetime, timedelta
from typing import Any, Dict
from django.http import HttpResponseRedirect, JsonResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy as _
from django.utils import timezone
from django.conf import settings
from django.forms import inlineformset_factory
from django.db.models import Q, Max

from allauth.account.forms import ResetPasswordForm
from django.contrib.auth.models import User

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Cliente, VendedorPadrao
from .forms import ClienteForm, CompraForm, CompraProdutoForm
from produto.models import Produto
from transportadora.models import Transportadora

from venda.models import (
    Adesivado,
    CondicaoVenda,
    FormaPagamento,
    Torneira,
    Venda,
    VendaProduto,
    Voltagem,
)
from financeiro.models import ContaReceber
from suporte.models import (
    Acoes,
    Suporte,
    Timeline,
    WorkFlow,
    Problema,
    Subproblema,
    ProblemaSuporte,
)


date_time = datetime.now().strftime(("%d/%m/%y %H:%M"))
today = timezone.now()
date_time = datetime.now()

success_url_cliente = _("cliente:clienteList")


class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = "cliente/clienteList.html"


clienteList = ClienteListView.as_view()


def getClientesAjax(request):
    bd_data = Cliente.objects.all()[: 100 + 100]
    data = []
    for d in bd_data:
        if d.cpf == None:
            cpf = " "
        else:
            cpf = str(d.cpf)
        if d.cnpj == None:
            cnpj = " "
        else:
            cnpj = str(d.cnpj)

        acoes = f'<a class="px-1" href="{d.pk}/editar/"><i class=" fa fa-edit"></i></a>'

        user = User.objects.filter(username=d.email)
        if not user:
            acoes = f'<a class="px-1" href="{d.pk}/editar/"><i class=" fa fa-edit"></i></a><a class="px-1" href="{d.pk}/createuser/"><i class="fa fa-user"></i></a>'

        data.append(
            {
                "nome_fantasia": d.nome_fantasia,
                "nome": d.nome[:40],
                "tel_principal": d.tel_principal,
                # "tel_contato": d.tel_contato,
                "email": d.email[:20],
                "cpf": cpf,
                "cnpj": cnpj,
                "estado": d.estado,
                "acoes": acoes,
            }
        )
    return JsonResponse({"data": data})


class ClienteCreateView(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
    model = Cliente
    form_class = ClienteForm
    template_name = "cliente/clienteCreateUpdate.html"
    success_url = success_url_cliente
    permission_required = "cliente.add_cliente"


clienteCreate = ClienteCreateView.as_view()


class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = "cliente/clienteDetails.html"
    context_object_name = "clientes"


clienteDetails = ClienteDetailView.as_view()


class ClienteUpdateView(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    model = Cliente
    form_class = ClienteForm
    template_name = "cliente/clienteCreateUpdate.html"
    success_url = success_url_cliente
    permission_required = "cliente.change_cliente"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["id"] = self.kwargs["pk"]
        return context


clienteUpdate = ClienteUpdateView.as_view()


class ClienteDeleteView(LoginRequiredMixin, DeleteView, PermissionRequiredMixin):
    model = Cliente
    template_name = "cliente/clienteDelete.html"
    success_url = success_url_cliente
    permission_required = "cliente.delete_cliente"

    def get(self, request, *args, **kwargs):
        if self.get_object().clientevenda.all() or self.get_object().receita_set.all():
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            self.template_name = "cliente/clienteRestrict.html"
            return self.render_to_response(context)
            # tem elemento, nao posso excluir
        else:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)


clienteDelete = ClienteDeleteView.as_view()


# mensagem informando que o email para redefinir senha foi envia
def mensagem(request):
    return render(request, "cliente/account/mensagem.html")


# envia um link ao email cadastrado para resetar a senha
def send_password_reset(request, user: settings.AUTH_USER_MODEL):
    request = HttpRequest()
    request.user = user
    request.META["HTTP_HOST"] = "127.0.0.1:8000"
    form = ResetPasswordForm({"email": user.email})
    if form.is_valid():
        form.save(request)


# cria o usuário utilizando o email como username
def createClienteUser(request, email):
    user = User.objects.filter(username=email)
    if not user:
        # Cria um novo usuário tendo o email como username
        user = User.objects.create_user(username=email, email=email)
        user.save()
    if email:
        user = User.objects.get(username=email)
        send_password_reset(request, user)
    return redirect("cliente:mensagem")


# verifica se existe usuário com o email cadastrado
@login_required
def clienteUser(request, cliente):
    bd_cliente = Cliente.objects.get(pk=cliente)
    bd_cliente.email = bd_cliente.email.lower()
    cliente = bd_cliente.id
    bd_cliente.save()
    if not bd_cliente.email:
        return clienteEmailCreate(request, cliente)

    createClienteUser(request, bd_cliente.email)
    return redirect("cliente:mensagem")


# caso o cliente não tenha email cadastrado
# abre a opção de inserir email - salva no cadastro do cliente
def clienteEmailCreate(request, cliente):
    template_name = "cliente/account/clienteEmailCreate.html"
    bd_cliente = Cliente.objects.get(id=cliente)
    if request.method == "POST":
        email = request.POST["email"]
        bd_cliente.email = email.lower()
        bd_cliente.save()
        return createClienteUser(request, bd_cliente.email)
    context = {"objeto": bd_cliente}
    return render(request, template_name, context)


@login_required
def dashboard(request, cliente):
    template_name = "cliente/account/clienteBase.html"
    objeto = Cliente.objects.filter(email=cliente)
    cliente_email = []
    for ob in objeto:
        cliente_email = ob.email
    painel = f"/cliente/{cliente_email}/dashboard/"
    context = {"objeto": objeto, "painel": painel}
    return render(request, template_name, context)


@login_required
def clienteLogout(request, cliente):
    template_name = "cliente/account/clienteLogout.html"
    return render(request, template_name)


@login_required
def compraCreate(request, cliente):
    cliente_user = Cliente.objects.get(email=request.user)
    vendedor_padrao = VendedorPadrao.objects.all().last()
    status = ("orcamento", "Orçamento")
    cpgto = CondicaoVenda.objects.get(id=2)
    fpgto = FormaPagamento.objects.get(nome="Pix")
    tranpte = Transportadora.objects.get(nome="A definir")
    template_name = "cliente/compra/compraCreateUpdate.html"

    form = CompraForm(
        request.POST or None,
        initial={
            "cliente": cliente_user,
            "vendedor": vendedor_padrao.vendedor,
            "status_venda": status,
            "condicaopgto": cpgto,
            "formapgto": fpgto,
            "transportadora": tranpte,
            "valor_frete": 0,
            "porcentagem_desconto": 0,
            "atualizadopor": f"{request.user}-{date_time}",
        },
    )

    # cria formulário para cada produto cadastrado
    produtos = Produto.objects.all().order_by("id")
    extra = len(produtos)
    Formset_VendaProduto_Factory = inlineformset_factory(
        Venda,
        VendaProduto,
        form=CompraProdutoForm,
        extra=extra,
        can_delete=False,
    )
    voltagem = Voltagem.objects.get(nome="Não sei")
    torneira = Torneira.objects.get(nome="A definir")
    adesivado = Adesivado.objects.get(nome="A definir")
    initial = []
    # lista todos os produtos cadastrados e gera o formset para cada um
    for pod in produtos:
        initial.append(
            {
                f"produto": pod.id,
                "preco": pod.preco,
                "quantidade": 0,
                "voltagem": voltagem.id,
                "torneira": torneira,
                "adesivado": adesivado,
            }
        )

    produto_form = Formset_VendaProduto_Factory(request.POST or None, initial=initial)

    if request.method == "POST":
        if form.is_valid() and produto_form.is_valid():
            venda = form.save(commit=False)
            venda.atualizadopor = f"{request.user}-{date_time}"
            venda.valor_venda = venda.subtotal
            venda.save()
            produto_form.instance = venda
            produto_form.save()

            return redirect("cliente:mensagem_compra", cliente)
        else:
            context = {
                "texto": "Novo",
                "form": form,
                "produto": produto_form,
            }
            return render(request, template_name, context)
    else:
        context = {
            "texto": "Novo",
            "form": form,
            "produto": produto_form,
        }
        return render(request, template_name, context)


# mensagem informando que um email foi enviado para o vendedor concluir a compra
def mensagem_compra(request, cliente):
    vendedor = Venda.objects.filter(cliente__email=cliente).last()
    return render(request, "cliente/compra/mensagemCompra.html", {"vendedor": vendedor})


@login_required
def comprasList(request, cliente):
    template_name = "cliente/compra/compraList.html"
    venda = Venda.objects.filter(cliente__email=cliente).order_by("-id")

    bd_suporte = Suporte.objects.values_list("venda_id", flat=True)
    atendimento = list(bd_suporte)
    data = Suporte.objects.filter(venda__id__in=atendimento)

    context = {"venda": venda, "atendimento": atendimento, "data": data}
    return render(request, template_name, context)


@login_required
def boletoClienteList(request, cliente):
    template_name = "cliente/compra/boletosList.html"
    boletos = ContaReceber.objects.filter(venda__cliente__email=cliente).exclude(
        dados_boleto={}
    )

    # if request.method == "POST":
    #     if request.POST.get("exibirBoleto"):
    #         exibir = request.POST.get("exibirBoleto")
    #         sep_venda_parcela = exibir.split(",")
    #         exibir_parcela = []
    #         exibir_parcela.append(sep_venda_parcela[0])
    #         exibir_parcela.append(sep_venda_parcela[1])
    #         exibirBoleto(exibir_parcela)
    context = {"boletos": boletos}
    return render(request, template_name, context)


# SUPORTE
@login_required
def suportClienteList(request, cliente):
    template_name = "cliente/suporte/clienteSuporteList.html"

    listagemsuporte = Suporte.objects.filter(venda__cliente__email=cliente).exclude(
        status="Concluído"
    )

    # informações dos suporte e das timelines listadas
    dados_timeline = []

    timeline = Timeline.objects.all()
    for s in listagemsuporte:
        texto_acao = "Ação não selecionada"
        sup = Timeline.objects.filter(suporte__id=s.id).aggregate(Max("id"))
        if sup["id__max"] != None:
            id = sup["id__max"]
            timeline = Timeline.objects.filter(id=id)
            for tl in timeline:
                try:
                    if tl.acao:
                        texto_acao = tl.acao.nome
                except:
                    pass

                dados_timeline.append(
                    {
                        "id": tl.suporte.id,
                        "venda": tl.suporte.venda.id,
                        "nf": tl.suporte.venda.numero_nf,
                        "cliente": tl.suporte.venda.cliente.nome,
                        "criadopor": tl.suporte.responsavel.username,
                        # "responsavelatual": tl.responsavel.username,
                        # "transportadora": tl.suporte.venda.transportadora.nome,
                        "fluxo": tl.fluxo.nome,
                        # "prazofluxo": prazofluxo.strftime("%d/%m/%y"),
                        # "data": tl.data,
                        "acao": texto_acao,
                        # "coracao": coracao,
                        # "prazoacao": prazoacao,
                        #     "pwfred": pwfred,
                        #     "pwfyellow": pwfyellow,
                        #     "pacred": pacred,
                        #     "pacyellow": pacyellow,
                    }
                )
        else:
            dados_timeline.append(
                {
                    "id": s.id,
                    "venda": s.venda.id,
                    "nf": s.venda.numero_nf,
                    "cliente": s.venda.cliente.nome,
                    "criadopor": s.responsavel.username,
                    # "responsavelatual": s.responsavel.username,
                    # "transportadora": s.venda.transportadora.nome,
                    "fluxo": "Fluxo não selecionado",
                    # "prazofluxo": "",
                    "data": s.data,
                    "acao": "Ação não selecionada",
                    # "coracao": coracao,
                    # "prazoacao": "",
                }
            )

    # if request.POST.get("pesquisa"):
    #     context["pesquisa"] = pesquisa = request.POST.get("pesquisa")
    #     try:
    #         listagemsuporte = Suporte.objects.filter(
    #             Q(venda__cliente__nome__icontains=pesquisa)
    #             | Q(venda__id=pesquisa)
    #             | Q(venda__numero_nf=pesquisa)
    #         ).order_by("-id")
    #     except:
    #         listagemsuporte = Suporte.objects.filter(
    #             venda__cliente__nome__icontains=pesquisa
    #         ).order_by("-id")

    context = {
        "dados_timeline": dados_timeline,
    }
    return render(request, template_name, context)


@login_required
def suporteClientCreate(request, venda):
    if not Suporte.objects.filter(venda=venda).exists():
        suporteCreated = Suporte.objects.create(
            venda=Venda.objects.get(pk=venda),
            responsavel=request.user,
            # responsavelAtual=request.user.username,
        )
        suporteCreated.save()
    return redirect("cliente:clienteSuporteProduto", venda)


@login_required
def clienteSuporteProduto(request, venda):
    template_name = "cliente/suporte/clienteSuporte.html"
    suporte = Suporte.objects.get(venda=venda)
    produtos = VendaProduto.objects.filter(venda=venda)
    dados = Suporte.objects.filter(venda=venda)
    timeline = Timeline.objects.filter(suporte=suporte).order_by("-id")
    last_timeline = timeline.first()
    bd_conclusao = ProblemaSuporte.objects.filter(suporte=suporte)

    inicioDias = suporte.data
    fimDias = today
    dias = 0
    dias = abs((fimDias.date() - inicioDias.date()).days)

    prazolimite_suporte = 0
    try:
        if last_timeline.fluxo.tempo:
            prazolimite_suporte = suporte.data + timedelta(
                days=last_timeline.fluxo.tempo
            )
    except:
        pass

    total = 0
    for p in produtos:
        total = p.venda.subtotal

    show_modal = []
    if not timeline:
        show_modal = True

    users = User.objects.all()
    responsavel = []
    for user in users:
        if not Cliente.objects.filter(email=user):
            responsavel.append({"id": user.id, "username": user.username})

    if request.method == "POST":
        wf = request.POST.get("fluxo")
        if wf == None:
            for fl in timeline:
                wf = fl.fluxo.id
        fluxo = WorkFlow.objects.get(id=wf)
        desc_fluxo = request.POST.get("desc_fluxo")
        descricao = request.POST.get("descricao")
        resp = request.POST.get("responsavel")
        responsavel = User.objects.get(id=resp)
        logado = request.user.username
        ac = request.POST.get("acao")
        acao = Acoes.objects.get(id=ac)

        time_line = Timeline.objects.create(
            suporte=suporte,
            fluxo=fluxo,
            desc_fluxo=desc_fluxo,
            responsavel=responsavel,
            descricao=descricao,
            logado=logado,
            acao=acao,
        )
        time_line.save()

        # finaliza o atendimento registrando o problema e subproblema
        input_prob = request.POST.get("problema")
        if input_prob:
            prob = Problema.objects.get(id=input_prob)
            desc_problema = request.POST.get("descProblema")
            input_subprob = request.POST.get("subproblema")
            subprob = Subproblema.objects.get(id=input_subprob)
            desc_subproblema = request.POST.get("descSubProblema")

            problema = ProblemaSuporte.objects.create(
                suporte=suporte,
                problema=prob,
                prodescricao=desc_problema,
                subproblema=subprob,
                subprodescricao=desc_subproblema,
            )
            problema.save()
            timeline_conclusao = Timeline.objects.filter(suporte=suporte)
            for timeline in timeline_conclusao:
                timeline.conclusao = today
                timeline.save()
            suporte.conclusao = today

        # suporte.responsavelAtual = responsavel.username
        suporte.save()

        return HttpResponseRedirect(f"/{venda}/assistencia/produto/")
    else:
        bd_conclusoes = (
            ProblemaSuporte.objects.filter(suporte=suporte)
            .exclude(suporte__conclusao=None)
            .values_list("suporte__conclusao", flat=True)
        )
        if bd_conclusoes:
            conclusoes = ProblemaSuporte.objects.filter(suporte=suporte)
        else:
            conclusoes = []

        context = {
            "total": total,
            "venda": Venda.objects.get(id=venda),
            "fluxo": WorkFlow.objects.all().order_by("id"),
            "responsavel": responsavel,
            "acoes": Acoes.objects.all(),
            "selectProdutos": VendaProduto.objects.filter(venda=venda),
            "show_modal": show_modal,
            "dias": dias,
            "dados": dados,
            "suporte": suporte,
            "timeline": timeline,
            "prazotimeline": prazolimite_suporte,
            "last_timeline": last_timeline,
            "produtos": produtos,
            "problema": Problema.objects.all(),
            "subproblema": Subproblema.objects.all(),
            "concluido": suporte.conclusao,
            "conclusao": bd_conclusao,
            "conclusoes": conclusoes,
        }
        return render(request, template_name, context)
