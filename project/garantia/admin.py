from django.contrib import admin


from .models import StatusGarantia, Garantia, StatusTimeLineGarantia, GarantiaTimeLine


@admin.register(StatusGarantia)
class StatusGarantiaAdmin(admin.ModelAdmin):
    ...


@admin.register(Garantia)
class GarantiaAdmin(admin.ModelAdmin):
    ...


@admin.register(StatusTimeLineGarantia)
class StatusTimeLineGarantiaAdmin(admin.ModelAdmin):
    ...


@admin.register(GarantiaTimeLine)
class GarantiaTimeLineAdmin(admin.ModelAdmin):
    ...
