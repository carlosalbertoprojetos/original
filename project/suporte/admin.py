from django.contrib import admin


from .models import (
    Suporte,
    Status,
    Timeline,
)


@admin.register(Suporte)
class SuporteAdmin(admin.ModelAdmin):
    ...


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    ...


@admin.register(Timeline)
class TimelineAdmin(admin.ModelAdmin):
    ...
