from django.contrib import admin
from core_app.models import Proyecto, Inmueble, Elemento, TipoSensor, Sensor, Evento, AlarmaHumo, AlarmaAcceso, AlarmaEstado, AlarmaReportada

# Register your models here.
#admin.site.register(Contact, ContactAdmin)
#admin.site.register(Agenda, AgendaAdmin)

admin.site.register(Proyecto)
admin.site.register(Inmueble)
admin.site.register(Elemento)
admin.site.register(TipoSensor)
admin.site.register(Sensor)
admin.site.register(Evento)
admin.site.register(AlarmaHumo)
admin.site.register(AlarmaAcceso)
admin.site.register(AlarmaEstado)
admin.site.register(AlarmaReportada)
