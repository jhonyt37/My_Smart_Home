from django.conf.urls import  include, url, re_path
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.contrib.auth import views
admin.autodiscover()


app_name = 'MySmartHome'

urlpatterns = [
    #url(r'^$', login_required(TemplateView.as_view(template_name='index.html'))),
    re_path(r'^$', RedirectView.as_view(url='/app/')),
    re_path(r'^app/', include('core_app.urls', namespace='core_app')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^login/$', views.LoginView.as_view(template_name='registration/login.html')),
    re_path(r'^logout/$',views.LogoutView.as_view(),{'next_page': '/'}), 
]
