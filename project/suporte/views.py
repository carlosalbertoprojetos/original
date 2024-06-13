from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models import Max


from .models import (
    Acoes,
    Suporte,
    Timeline,
    WorkFlow,
    Problema,
    Subproblema,
    ProblemaSuporte,
    ArquivosSuporte,
)

from cliente.models import Cliente
from venda.models import Venda, VendaProduto


date_time = datetime.now().strftime(("%d/%m/%y %H:%M"))
today = timezone.now()
hoje = today.date()


@login_required
def suporteList(request):
    template_name = "suporte/suporteList.html"
    # venc = (today - timedelta(days=3)).strftime("%d/%m/%y")

    if request.user.is_superuser:
        listagemsuporte = (
            Suporte.objects.all().exclude(status="Concluído").order_by("data")
        )
    else:
        listagemsuporte = (
            Suporte.objects.all().exclude(status="Concluído").order_by("data")
        )

    # somente a última timeline de cada suporte
    timeline = Timeline.objects.all().exclude(suporte__status="Concluído")

    # informações dos suporte e das timelines listadas
    dados_timeline = []
    acvencidas = acvencendo = flvencidos = flvencendo = 0
    for s in listagemsuporte:
        prazofluxo = ""
        texto_acao = "Ação não selecionada"
        prazoacao = ""
        coracao = "#ffc107"
        pwfred = ""
        pacred = ""
        pwfyellow = ""
        pacyellow = ""
        sup = Timeline.objects.filter(suporte__id=s.id).aggregate(Max("id"))
        if sup["id__max"] != None:
            id = sup["id__max"]
            timeline = Timeline.objects.filter(id=id)
            for tl in timeline:
                try:
                    if tl.acao:
                        texto_acao = tl.acao.nome
                        prazoacao = (tl.data + timedelta(days=tl.acao.tempo)).date()
                        coracao = tl.acao.cor
                except:
                    pass

                prazofluxo = (tl.suporte.data + timedelta(days=tl.fluxo.tempo)).date()
                if prazofluxo < hoje:
                    pwfred = "vencido"

                if prazoacao and prazoacao < hoje:
                    pacred = "vencido"

                for i in range(0, 3):
                    hoje_ = hoje + timedelta(days=i)
                    if prazofluxo == hoje_:
                        pwfyellow = "vencendo"

                    if prazoacao == hoje_:
                        pacyellow = "vencendo"

                dados_timeline.append(
                    {
                        "id": tl.suporte.id,
                        "venda": tl.suporte.venda.id,
                        "nf": tl.suporte.venda.numero_nf,
                        "cliente": tl.suporte.venda.cliente.nome,
                        "criadopor": tl.suporte.responsavel.username,
                        "responsavelatual": tl.responsavel.username,
                        "transportadora": tl.suporte.venda.transportadora.nome,
                        "fluxo": tl.fluxo.nome,
                        "prazofluxo": prazofluxo.strftime("%d/%m/%y"),
                        "data": tl.data,
                        "acao": texto_acao,
                        "coracao": coracao,
                        "prazoacao": prazoacao,
                        "pwfred": pwfred,
                        "pwfyellow": pwfyellow,
                        "pacred": pacred,
                        "pacyellow": pacyellow,
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
                    "responsavelatual": s.responsavel.username,
                    "transportadora": s.venda.transportadora.nome,
                    "fluxo": "Fluxo não selecionado",
                    "prazofluxo": "",
                    "data": s.data,
                    "acao": "Ação não selecionada",
                    "coracao": coracao,
                    "prazoacao": "",
                }
            )

        if prazofluxo and prazofluxo < hoje:
            flvencidos += 1
        if prazofluxo and prazofluxo == hoje:
            flvencendo += 1
        if prazoacao and prazoacao < hoje:
            acvencidas += 1
        if prazoacao and prazoacao == hoje:
            acvencendo += 1

    if request.POST.get("pesquisa"):
        context["pesquisa"] = pesquisa = request.POST.get("pesquisa")
        try:
            listagemsuporte = Suporte.objects.filter(
                Q(venda__cliente__nome__icontains=pesquisa)
                | Q(venda__id=pesquisa)
                | Q(venda__numero_nf=pesquisa)
            ).order_by("-id")
        except:
            listagemsuporte = Suporte.objects.filter(
                venda__cliente__nome__icontains=pesquisa
            ).order_by("-id")

    context = {
        # "venc": venc,
        "flvencidos": flvencidos,
        "flvencendo": flvencendo,
        "acvencidas": acvencidas,
        "acvencendo": acvencendo,
        "lista": dados_timeline,
    }
    return render(request, template_name, context)


@login_required
def suporteCreate(request, venda):
    if not Suporte.objects.filter(venda=venda).exists():
        suporteCreated = Suporte.objects.create(
            venda=Venda.objects.get(pk=venda),
            responsavel=request.user,
        )
        suporteCreated.save()
    return redirect("suporte:suporteTimeLineCreate", venda)


def acoesFluxoAjax(request):
    fluxo = request.GET.get("fluxo")
    acoes = Acoes.objects.filter(workflow__id=fluxo)
    bd_tempo = WorkFlow.objects.get(id=fluxo)
    tempo = bd_tempo.tempo
    # Converte os objetos de ação em um formato JSON serializável
    acoes_json = [{"id": acao.id, "nome": acao.nome, "cor": acao.cor} for acao in acoes]
    return JsonResponse({"acoes": acoes_json, "tempo": tempo})


def subproblemasAjax(request):
    problema_id = request.GET.get("problema_id")
    subproblemas = Subproblema.objects.filter(problema_id=problema_id).values(
        "id", "nome"
    )
    return JsonResponse(list(subproblemas), safe=False)


@login_required
def suporteTimeLineCreate(request, venda):
    suporte = Suporte.objects.get(venda=venda)
    timeline = Timeline.objects.filter(suporte=suporte).order_by("-id")
    try:
        for tll in timeline:
            if str(tll.responsavel) == str(request.user) and tll.visualizacao == False:
                tll.visualizacao = True
                tll.save()
    except:
        pass

    template_name = "suporte/suporteTimelineCreate.html"
    produtos = VendaProduto.objects.filter(venda=venda)
    dados = Suporte.objects.filter(venda=venda)
    last_timeline = timeline.first()
    bd_conclusao = ProblemaSuporte.objects.filter(suporte=suporte)

    inicioDias = suporte.data
    fimDias = today
    dias = 0
    dias = abs((fimDias.date() - inicioDias.date()).days)

    prazolimite_suporte = 0
    vencendo = ""
    vencido = ""
    try:
        if last_timeline.fluxo.tempo:
            prazolimite_suporte = suporte.data + timedelta(
                days=last_timeline.fluxo.tempo
            )
            vencimento = prazolimite_suporte.strftime("%d/%m/%y")
            for i in range(0, 3):
                hoje_ = (today + timedelta(days=i)).strftime("%d/%m/%y")
                if vencimento == hoje_:
                    vencendo = "vencendo"

            if vencimento < hoje:
                vencido = "vencido"
    except:
        pass

    total = 0
    for p in produtos:
        total = p.venda.subtotal

    users = User.objects.all()
    responsavel = []
    for user in users:
        if not Cliente.objects.filter(email=user):
            responsavel.append({"id": user.id, "username": user.username})

    bd_arquivos = ArquivosSuporte.objects.all()

    if request.method == "POST":

        arquivo = request.FILES.getlist("arquivo")
        for arquivo in arquivo:
            bd_arquivos.create(arquivo=arquivo, suporte=suporte)

        cliente = request.POST.get("cliente_final")
        telefone = request.POST.get("tel_cliente_final")

        wf = request.POST.get("fluxo")
        if wf == None:
            for fl in timeline:
                wf = fl.fluxo.id
        fluxo = WorkFlow.objects.get(id=wf)
        desc_fluxo = request.POST.get("desc_fluxo")
        descricao = request.POST.get("descricao")

        if not descricao:
            descricao = desc_fluxo
        logado = request.user.username

        resp = request.POST.get("responsavel")
        if not resp:
            resp = request.user.id
        responsavel = User.objects.get(id=resp)

        # informação para sininho de notificação
        visualizacao = False
        if str(responsavel) == str(request.user.username):
            visualizacao = True

        ac = request.POST.get("acao")
        if not ac:
            acao = None
        elif not ac:
            acao = last_timeline.acao
        else:
            acao = Acoes.objects.get(id=ac)

        # finaliza o atendimento registrando o problema e subproblema
        input_prob = request.POST.get("problema")

        if input_prob:
            prob = Problema.objects.get(id=input_prob)
            desc_problema = request.POST.get("descProblema")
            input_subprob = request.POST.get("subproblema")
            subprob = Subproblema.objects.get(id=input_subprob)

            ProblemaSuporte.objects.create(
                suporte=suporte,
                problema=prob,
                prodescricao=desc_problema,
                subproblema=subprob,
            )

            timeline_conclusao = Timeline.objects.filter(suporte=suporte)
            for timeline in timeline_conclusao:
                timeline.conclusao = today
                timeline.visualizacao = visualizacao
                timeline.save()
                suporte.status = "Concluído"
                suporte.statusAtual = "Concluído"

            suporte.conclusao = today
            suporte.concluir = True
            descricao = "Atendimento concluído"

        Timeline.objects.create(
            suporte=suporte,
            fluxo=fluxo,
            desc_fluxo=desc_fluxo,
            responsavel=responsavel,
            descricao=descricao,
            logado=logado,
            acao=acao,
            visualizacao=visualizacao,
        )

        suporte.cliente_final = cliente
        suporte.tel_cliente_final = telefone
        suporte.save()

        return HttpResponseRedirect(f"/suporte/{venda}/timeline/create/")
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

        responsavel_atual = []
        try:
            if last_timeline.responsavel:
                responsavel_atual = last_timeline.responsavel
        except:
            responsavel_atual = suporte.responsavel

        arquivos = ArquivosSuporte.objects.filter(suporte=suporte)

        context = {
            "total": total,
            "venda": Venda.objects.get(id=venda),
            "fluxo": WorkFlow.objects.all().order_by("id"),
            "responsavel": responsavel,
            "acoes": Acoes.objects.all(),
            "selectProdutos": VendaProduto.objects.filter(venda=venda),
            "dias": dias,
            "vencendo": vencendo,
            "vencido": vencido,
            "dados": dados,
            "suporte": suporte,
            "timeline": timeline,
            "prazotimeline": prazolimite_suporte,
            "last_timeline": last_timeline,
            "responsavel_atual": responsavel_atual,
            "produtos": produtos,
            "problema": Problema.objects.all(),
            "subproblema": Subproblema.objects.all(),
            "concluido": suporte.conclusao,
            "conclusao": bd_conclusao,
            "conclusoes": conclusoes,
            "arquivos": arquivos,
        }
        return render(request, template_name, context)


@login_required
def reabrirAtendimento(request, suporte):
    user = request.user.email

    suporte = Suporte.objects.get(id=suporte)
    suporte.concluir = "False"
    suporte.conclusao = None
    suporte.status = "aberto"
    suporte.statusAtual = "Reiniciado"
    suporte.save()

    descricao = "Atendimento reaberto"

    Timeline.objects.create(
        suporte=suporte,
        descricao=descricao,
        responsavel=request.user,
        logado=user,
    )

    return HttpResponseRedirect(f"/suporte/{suporte.venda}/timeline/create/")
