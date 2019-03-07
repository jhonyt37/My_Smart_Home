from django.conf.urls import url, re_path
from django.contrib.auth.decorators import login_required
from core_app import views

app_name = 'core_app'

urlpatterns = [
    # ex: /app/
    re_path(r'^$', login_required(views.HomeListView.as_view()), name='home_list'),
    # ex: /grupo/
    re_path(r'^correo/$', login_required(views.HomeListView.as_view(template_name='core_app/correo_index.html')), name='correo_index'),

    re_path(r'^api/$', views.SimuladorView.as_view(template_name='core_app/api_index.html'), name='api_index'),

    re_path(r'^eventos/$', login_required(views.EventosView.as_view(template_name='core_app/even_list.html')), name='even_list'),

    re_path(r'^history/$', login_required(views.AlarmReportsView.as_view(template_name='core_app/alarmas_history.html')), name='alarmas_history'),
    
    re_path(r'^tipo_alarmas/$', login_required(views.TipoAlarmsView.as_view(template_name='core_app/tipo_alarmas.html')),name='tipo_alarmas'),
    re_path(r'^alarmas/$', login_required(views.AlarmsListView.as_view(template_name='core_app/alarmas_lista.html')), name='alarmas_lista'),
    re_path(r'^alarmas/editar_alarmas/$', login_required(views.AlarmsEditView.as_view(template_name='core_app/alarmas_detalle.html')), name='alarmas_detalle'),
    re_path(r'^alarmas/crear_alarmas/$', login_required(views.AlarmsView.as_view(template_name='core_app/crear_alarma.html')), name='alarmas_lista'),

    # ex: /elemento/create/
     re_path(r'^create/$', login_required(views.CrearElementoView.as_view(template_name='core_app/crear_elemento.html')), name='crear_elemento'),
     re_path(r'^elemento/$', login_required(views.HomeListView.as_view()), name='home_list'),
     re_path(r'^elemento/delete/$', login_required(views.BorrarElementoView.as_view(template_name='core_app/borrar_elemento.html')), name='borrar_elemento'),
    
    # ex: /agenda/5/
    re_path(r'^(?P<pk>\d+)/$', login_required(views.ElemDetailView.as_view()), name='elem_detail'),
    # ex: /agenda/1/update/
    re_path(r'^(?P<pk>\d+)/update/$', login_required(views.ElemUpdateView.as_view()), name='elem_update'),


    re_path(r'^correo/envio/$', login_required(views.CorreoView.as_view(template_name='core_app/correo_detail.html')), name='correo_envio'),

    re_path (r'^alarms/$', login_required(views.AlarmsListView.as_view(template_name='core_app/alarms_list.html')), name='alarms_list'),

]