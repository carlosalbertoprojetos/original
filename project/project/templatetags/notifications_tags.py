from django import template
from django.db.models import Max
from datetime import date

from suporte.models import Timeline

hoje = date.today()
register = template.Library()


@register.inclusion_tag("includes/notifications.html")
def show_notifications(user):
    timelines = Timeline.objects.filter(visualizacao=False)
    ultimos_registros = timelines.values("suporte_id").annotate(ultima_data=Max("data"))

    ultimos_timeline_por_suporte = Timeline.objects.filter(responsavel=user).filter(
        suporte_id__in=ultimos_registros.values("suporte_id"),
        data__in=ultimos_registros.values("ultima_data"),
    )

    dias = []
    for i in ultimos_timeline_por_suporte:
        ano = i.data.year
        mes = i.data.month
        dia = i.data.day
        data = date(ano, mes, dia)
        dias_ = hoje - data
        dias.append({i.suporte.id: dias_.days})

    return {"timeline": ultimos_timeline_por_suporte, "user": user, "dias": dias}
