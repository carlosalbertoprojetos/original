from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from datetime import datetime
from django.utils import timezone
from django.db.models import Q


from .models import Suporte, Status, Timeline
from .forms import TimelineForm
from venda.models import Venda, VendaProduto


date_time = datetime.now().strftime(("%d/%m/%y %H:%M"))
today = timezone.now()


@login_required
def suporteGeralList(request):
    context = {}
    template_name = "suporte/suporteList.html"
    listagemsuporte = Suporte.objects.all().exclude(status="Concluído")

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

    context["suportes"] = listagemsuporte
    return render(request, template_name, context)


@login_required
def suporteCreate(request, venda):
    if not Suporte.objects.filter(venda=venda).exists():
        suporteCreated = Suporte.objects.create(
            venda=Venda.objects.get(pk=venda),
            responsavel=request.user,
            responsavelAtual=request.user.username,
        )
        suporteCreated.save()
    return redirect("suporte:suporteTimeLineCreate", venda)


@login_required
def suporteTimeLineCreate(request, venda):
    template_name = "suporte/suporteTimelineCreate.html"
    suporte = Suporte.objects.get(venda=venda)
    produtos = VendaProduto.objects.filter(venda=venda)
    status = Status.objects.all()
    dados = Suporte.objects.filter(venda=venda)
    timeLine = Timeline.objects.filter(suporte=suporte).order_by("-id")

    inicioDias = suporte.data
    fimDias = today
    concluido = ""
    dias = 0
    for i in timeLine:
        if i.status.nome == "Concluído":
            fimDias = concluido = i.data

    dias = abs((fimDias.date() - inicioDias.date()).days)

    total = 0
    for p in produtos:
        total = p.venda.subtotal

    show_modal = []
    if not timeLine:
        show_modal = True

    form = TimelineForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form = form.save(commit=False)
            form.suporte = suporte
            form.logado = request.user.username
            form.save()
            return HttpResponseRedirect(f"/suporte/{venda}/timeline/create/")
        else:
            context = {
                "total": total,
                "form": form,
                "show_modal": show_modal,
                "status": status,
                "dias": dias,
                "dados": dados,
                "suporte": suporte,
                "timeLine": timeLine,
                "produtos": produtos,
                "concluido": concluido,
            }
            return render(request, template_name, context)
    else:
        context = {
            "total": total,
            "form": form,
            "show_modal": show_modal,
            "status": status,
            "dias": dias,
            "dados": dados,
            "suporte": suporte,
            "timeLine": timeLine,
            "produtos": produtos,
            "concluido": concluido,
        }
        return render(request, template_name, context)


@login_required
def suporteTimeLineUpdate(request, timeline):
    template_name = "suporte/suporteTimelineUpdate.html"
    objeto = get_object_or_404(Timeline, pk=timeline)
    timeLine = Timeline.objects.filter(pk=timeline).order_by("-id")

    venda = 0
    inicioDias = 0
    fimDias = today
    concluido = ""
    dias = 0
    for i in timeLine:
        venda = i.suporte.venda
        inicioDias = i.suporte.data
        if i.status.nome == "Concluído":
            fimDias = concluido = i.data

    dias = abs((fimDias.date() - inicioDias.date()).days)

    form = TimelineForm(request.POST or None, instance=objeto)
    if request.method == "POST":
        if form.is_valid():
            form = form.save(commit=False)
            form.logado = request.user.username
            form.save()
            return HttpResponseRedirect(f"/suporte/{venda}/timeline/create/")
        else:
            context = {
                "form": form,
                "dias": dias,
                "dados": timeLine,
                "concluido": concluido,
            }
            return render(request, template_name, context)
    else:
        form = TimelineForm(instance=objeto)
        context = {
            "form": form,
            "dias": dias,
            "dados": timeLine,
            "concluido": concluido,
        }
        return render(request, template_name, context)
