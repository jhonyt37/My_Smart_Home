from django.views.generic import ListView, CreateView, TemplateView, DetailView, UpdateView
from django.shortcuts import render
from core_app.correo import  correo
from core_app.sensores import  alarmas
from core_app.models import Inmueble, Elemento, Evento, Alarma, Sensor, TipoSensor
from MySmartHome.settings import DB_NAME, DB_USER, DB_HOST, DB_PWD
import psycopg2
import datetime
from core_app.forms import AlarmaHumoForm,AlarmaEstadoForm, AlarmaEstado2Form, AlarmaAccesoForm, ElementoForm, EventoForm
from django.forms.formsets import formset_factory, BaseFormSet
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from core_app.models import AlarmaHumo,AlarmaEstado,AlarmaAcceso
from django.http import HttpResponseRedirect


class CorreoListView(ListView):
    context_object_name = 'app_list' 
    
    @staticmethod
    def get_queryset(self):
        return [];

class CorreoView(ListView):
    context_object_name = 'correo_envio' 
    def get_queryset(self):        
        user = self.request.user
        resultado = {}

        inmuebles = Inmueble.objects.all().filter(user_id = user.id)

        if inmuebles.__len__() > 0:
            resultado['inmuebles'] = inmuebles

            primer_inmueble = inmuebles[0]
            resultado['elementos'] = Elemento.objects.all().filter(
                 inmu_id = primer_inmueble.id, user_id = user.id).order_by('-estado')

            if resultado['elementos'].__len__() > 0:
                primer_elemento = resultado['elementos'][0]

                c = correo.MyCorreo()
                c.enviar_gmail(tipo_alarma=self.request.GET['alerta_id'],
                          destinatario=user.email,activo=primer_elemento.nombre,
                          user=user)

                connection=psycopg2.connect("host=" + DB_HOST + " dbname=" + DB_NAME + " user=" + DB_USER + " password=" + DB_PWD )
                cursor=connection.cursor()

                cursor.execute("UPDATE core_app_activo SET estado =" + str(self.request.GET['alerta_id']) + " WHERE id =" + str(primer_elemento.id))
                connection.commit()

        else:
            c = correo.myCorreo()
            c.enviarGmail(tipo_alarma=self.request.GET['alerta_id'],
                          destinatario=user.email,activo="Activo Ejemplo")
        
    
#==========================================================
#Clase que gestiona los atributos requeridos por el home
#==========================================================
class HomeListView(ListView):
    context_object_name = 'info'
    template_name = 'core_app/home_list.html'
    
    def get_queryset(self):
        user = self.request.user
        inmuebles = Inmueble.objects.all().filter(user_id = user.id).order_by('-estado')
        resultado = {}

        i = alarmas.Alarma()
        res = i.hay_nuevas_notificaciones(user)
        print('resultado de la funcion '+str(res))
        if res == True:
            num_alarmas = i.contar_nuevas_notificaciones(user)
            resultado['pendientes'] = num_alarmas
        
        if inmuebles.__len__() > 0:
            resultado['inmuebles'] = inmuebles
            
            if 'inmu_id' in self.request.GET:
                inmueble_param_id = self.request.GET['inmu_id']
                resultado['elementos'] = Elemento.objects.all().filter(
                     inmu_id = inmueble_param_id, user_id = user.id).order_by('-estado')

                resultado['inmueble_actual'] = Inmueble.objects.get(pk=inmueble_param_id)

            else:
                primer_inmueble = inmuebles[0]
                print ("paso 0")
                print (primer_inmueble.id)
                print ("paso 1")
                print (user.id)
                resultado['elementos'] = Elemento.objects.all().filter(inmu_id = primer_inmueble.id, user_id = user.id).order_by('-estado')
                resultado['inmueble_actual'] = Inmueble.objects.get(pk=primer_inmueble.id)
        
        return resultado

class EventosView(ListView):
    context_object_name = 'info'
    template_name = 'core_app/even_list.html'
    
    def get_queryset(self):
                    
        user = self.request.user
        inmuebles = Inmueble.objects.all().filter(user_id = user.id).order_by('-estado')
        fecha1  = None#'2015-01-19' #self.request.GET['fech_1']
        fecha2  = None#'2015-03-19'# '2015-02-18''2015-03-01'#self.request.GET['fech_1']

        resultado = {}
        i = alarmas.Alarma()
        res = i.hay_nuevas_notificaciones(user)
        if res == True:
            num_alarmas = i.contar_nuevas_notificaciones(user)
            resultado['pendientes'] = num_alarmas

        resultado['inmuebles'] = inmuebles  
        if ('inmu_id' in self.request.GET) and self.request.GET['inmu_id'] != "":
            inmb_id = self.request.GET['inmu_id']
            resultado['inmueble_actual'] = Inmueble.objects.get(pk=inmb_id)
            resultado['elementos'] = Elemento.objects.all().filter(inmu_id = inmb_id, user_id = user.id).order_by('-estado')
            eventos = i.consul_events_inmb(inmueb_id = inmb_id, fecha1 = fecha1, fecha2 = fecha2)
        else:
            if ('elemento_id' in self.request.GET) and self.request.GET['elemento_id'] != "":
                elm_id = self.request.GET['elemento_id']
                resultado['elemento_actual'] = Elemento.objects.get(pk=elm_id)
                resultado['inmueble_actual'] = resultado['elemento_actual'].inmueble
                resultado['elementos'] = Elemento.objects.all().filter(inmu_id = resultado['inmueble_actual'].id, user_id = user.id).order_by('-estado')
                eventos = i.consul_events_elem(elem_id = elm_id, fech_1 = fecha1, fech_2 = fecha2)
            else:
                if user.id != None:
                    eventos = i.consul_events(user_id = user.id, fech_1 = fecha1, fech_2 = fecha2)
                    resultado['elementos'] = Elemento.objects.all().filter(user_id = user.id).order_by('-estado')
        
        resultado['eventos'] = eventos 
        maxdatetime = datetime.datetime.today()
        for evento in eventos:
            if evento.get('fecha_hora_evento').date() > maxdatetime.date():
                maxdatetime = evento.get('fecha_hora_evento')
        resultado['maxdatetime'] = maxdatetime
        return resultado

class ElemCreateView(CreateView):
    model = Elemento
    fields = ['nombre', 'estado']
    success_url = '/app/'

    obj=10

    success_url = '/core_app/'

    
    
    def form_valid(self, form):

        form.instance.user      = self.request.user
        inmb_id = self.request.session['inmu_id']
        form.instance.inmueble = Inmueble.objects.get(pk=inmb_id)
        
        return super(ElemCreateView, self).form_valid(form)
    
class ElemDetailView(DetailView):
    model = Elemento

class ElemUpdateView(UpdateView):
    model = Elemento
    
    def get_success_url(self):
        return reverse('app:elem_detail', kwargs={'pk': self.object.pk,})
    
#Este es un cambio de prueba para el Codeship
class CodeShipTest(ListView):
    context_object_name = 'info'
    template_name = 'core_app/home_list.html'


#vista de alarmas
class AlarmsListView(TemplateView):
    template_name = 'core_app/alarmas_lista.html'
    
    def get(self,request):
        

        user = self.request.user
        inmuebles = Inmueble.objects.all().filter(user_id = user.id).order_by('-estado')
        i = alarmas.Alarma()
        info = {}
        
        res = i.hay_nuevas_notificaciones(user)
        if res == True :
            num_alarmas = i.contar_nuevas_notificaciones(user)
            info['pendientes'] = num_alarmas

        if inmuebles.__len__() > 0:
            info['inmuebles'] = inmuebles
            info['inmueble_actual'] = info['inmuebles'][0]
            
            if 'inmu_id' in self.request.GET:
                inmueble_param_id = self.request.GET['inmu_id']
                info['elementos'] = Elemento.objects.all().filter(
                     inmu_id = inmueble_param_id, user_id = user.id).order_by('-estado')
                alarma = i.consul_alarms_inmb(inmueb_id = inmueble_param_id,tipo_sensor_id='0')

                info['inmueble_actual'] = Inmueble.objects.get(pk=inmueble_param_id)

            else:
                primer_inmueble = inmuebles[0]
                info['elementos'] = Elemento.objects.all().filter(
                     inmu_id = primer_inmueble.id, user_id = user.id).order_by('-estado')

                if user.id != None:

                    info['inmueble_actual'] = info['inmuebles'][0]
                    inmueble_param_id = info['inmueble_actual'].id
                    alarma = i.consul_alarms_inmb(inmueb_id = inmueble_param_id,tipo_sensor_id='0')
                    info['elementos'] = Elemento.objects.all().filter(user_id = user.id).order_by('-estado')
                    
                
        info['alarmas'] = alarma

        return  render(request,self.template_name,locals())
        #return  render_to_response(self.template_name, locals(),
        #                RequestContext(request))


    

#vista de alarmas
class AlarmsEditView(TemplateView):
    template_name = 'core_app/alarmas_detalle.html'
    
    @staticmethod
    def set_data_alarma(tipo_alarma,alarma):
        if tipo_alarma==2 or tipo_alarma==4:
            alarma.estado_sensor=form['estado']

    def post(self,request,contact_id):
        

        class RequiredFormSet(BaseFormSet):
            def __init__(self, *args, **kwargs):
                super(RequiredFormSet, self).__init__(*args, **kwargs)
                for form in self.forms:
                    form.empty_permitted = False


        tipo_alarma = int(self.request.POST['tipo_alarma'])
        

        if tipo_alarma==1 :
            contact = get_object_or_404(AlarmaHumo, pk=contact_id)
            alarm_form_set = formset_factory(AlarmaHumoForm, extra=0, max_num=10, formset=RequiredFormSet)
        elif tipo_alarma==2:
            contact = get_object_or_404(AlarmaEstado, pk=contact_id)
            alarm_form_set = formset_factory(AlarmaEstado2Form, extra=0, max_num=10, formset=RequiredFormSet)
        elif tipo_alarma==3:
            contact = get_object_or_404(AlarmaAcceso, pk=contact_id)
            alarm_form_set = formset_factory(AlarmaAccesoForm, extra=0, max_num=10, formset=RequiredFormSet)    
        elif tipo_alarma==4:
            contact = get_object_or_404(AlarmaEstado, pk=contact_id)
            alarm_form_set = formset_factory(AlarmaEstadoForm, extra=0, max_num=10, formset=RequiredFormSet)
        
        alarma_formset = alarm_form_set(request.POST, request.FILES, instance=contact)
        sensor_id = self.request.POST.get('sensor_select',False)
        nivel_id = self.request.POST.get('nivel_select',False)

        
        if alarma_formset.is_valid():
            if sensor_id != '0':
                set_form_data()
                for form in alarma_formset.forms:
                    alarma = form.save(commit=False)
                    sensor = Sensor.objects.all().filter(id = sensor_id)
                    alarma.sensor = sensor[0]
                    alarma.nivel_alarma = nivel_id
                    self.set_data_alarma(tipo_alarma,alarma)
                    
                    alarma.save()
            else:
                error_sensor= '* This field is required.'
                i = alarmas.Alarma()
                sensores = i.consul_elementos_sensor( tipo_sensor = tipo_alarma)

                return  render(request,self.template_name,locals())
                #return  render_to_response(self.template_name, locals(),
                #        RequestContext(request))
                    
        else:
            
            i = alarmas.Alarma()
            sensores = i.consul_elementos_sensor( tipo_sensor = tipo_alarma)
            
            return  render(request,self.template_name,locals())
            #return  render_to_response(self.template_name, locals(),
            #        RequestContext(request))

        return HttpResponseRedirect('../')


    def get(self,request):
        class RequiredFormSet(BaseFormSet):
            def __init__(self, *args, **kwargs):
                super(RequiredFormSet, self).__init__(*args, **kwargs)
                for form in self.forms:
                    form.empty_permitted = False

        a = request.session.get('a',  None)

        if 'alarma_id' in self.request.GET:
            alarma_id = self.request.GET['alarma_id']            
        else:
            return  render(request,'core_app/home_list.html',locals())
            #return  render_to_response('core_app/home_list.html', locals(),
            #            RequestContext(request))



        alarma_id = self.request.GET['alarma_id']
        alarm = Alarma.objects.all().filter(id=alarma_id)
        tipo_alarma = alarm[0].sensor.tipo_sensor.id
        sensor = alarm[0].sensor


        i = alarmas.Alarma()
        sensores = i.consul_elementos_sensor( tipo_sensor = tipo_alarma)

        if tipo_alarma==1 or tipo_alarma=='1':
            alarm_form_set = formset_factory(AlarmaHumoForm, extra=0, max_num=10, formset=RequiredFormSet)
            alarm = AlarmaHumo.objects.all().filter(id=alarma_id)
            my_alarma = alarm[0]
            hora_ini = 0
            hora_fin = 0
            estado = 0
            contact = get_object_or_404(AlarmaHumo, pk=alarma_id)

        elif tipo_alarma==2 or tipo_alarma=='2':
            alarm_form_set = formset_factory(AlarmaEstado2Form, extra=0, max_num=10, formset=RequiredFormSet)
            alarm = AlarmaEstado.objects.all().filter(id=alarma_id)
            my_alarma = alarm[0]
            hora_ini = my_alarma.hora_inicio
            hora_fin = my_alarma.hora_fin
            estado = my_alarma.estado_sensor
            contact = get_object_or_404(AlarmaEstado, pk=alarma_id)
        elif tipo_alarma==3 or tipo_alarma=='3':
            alarm_form_set = formset_factory(AlarmaAccesoForm, extra=0, max_num=10, formset=RequiredFormSet)    
            alarm = AlarmaAcceso.objects.all().filter(id=alarma_id)
            my_alarma = alarm[0]
            hora_ini = my_alarma.hora_inicio
            hora_fin = my_alarma.hora_fin
            estado = 0
            contact = get_object_or_404(AlarmaAcceso, pk=alarma_id)
        elif tipo_alarma==4 or tipo_alarma=='4':
            alarm_form_set = formset_factory(AlarmaEstadoForm, extra=0, max_num=10, formset=RequiredFormSet)            
            alarm = AlarmaEstado.objects.all().filter(id=alarma_id)
            my_alarma = alarm[0]
            hora_ini = my_alarma.hora_inicio
            hora_fin = my_alarma.hora_fin
            estado = my_alarma.estado_sensor
            contact = get_object_or_404(AlarmaEstado, pk=alarma_id)
        else:
            return  render(request,'core_app/home_list.html',locals())
            #return  render_to_response('core_app/home_list.html', locals(),
            #            RequestContext(request))
    
        
        alarma_id = self.request.GET['alarma_id']
        alarm = Alarma.objects.all().filter(id=alarma_id)
        

        alarma_formset = alarm_form_set(instance=contact,initial=[{
            'nombre': my_alarma.nombre,
            'descripcion': my_alarma.descripcion,
            'sensor':my_alarma.sensor,
            'activa':my_alarma.activa,
            'notifica':my_alarma.notifica,
            'nivel_alarma':my_alarma.nivel_alarma,
            'hora_inicio': hora_ini,
            'hora_fin': hora_fin,
            'estado_sensor':estado,
            }])

        nivel_alarma = my_alarma.nivel_alarma

        return  render(request,self.template_name,locals())
        #return  render_to_response(self.template_name, locals(),
        #                RequestContext(request))


#creacion de alarmas
class AlarmsView(TemplateView):

    @staticmethod
    def set_data_alarma(tipo_alarma,alarma):
        if tipo_alarma=='2' or tipo_alarma=='4':
            alarma.estado_sensor=int(form.cleaned_data['estado'])


    def post(self,request):

        class RequiredFormSet(BaseFormSet):
            def __init__(self, *args, **kwargs):
                super(RequiredFormSet, self).__init__(*args, **kwargs)
                for form in self.forms:
                    form.empty_permitted = False

        tipo_alarma = int(self.request.POST['tipo_alarma'])
        print('alarma '+str(tipo_alarma))

        if tipo_alarma==1 :
            alarm_form_set = formset_factory(AlarmaHumoForm, extra=1, max_num=10, formset=RequiredFormSet)
        elif tipo_alarma==2:
            alarm_form_set = formset_factory(AlarmaEstado2Form, extra=1, max_num=10, formset=RequiredFormSet)
        elif tipo_alarma==3:
            alarm_form_set = formset_factory(AlarmaAccesoForm, extra=1, max_num=10, formset=RequiredFormSet)    
        elif tipo_alarma==4:
            alarm_form_set = formset_factory(AlarmaEstadoForm, extra=1, max_num=10, formset=RequiredFormSet)
        
        alarma_formset = alarm_form_set(request.POST, request.FILES)
        sensor_id = self.request.POST.get('sensor_select',False)
        nivel_id = self.request.POST.get('nivel_select',False)
        inmu_id = self.request.POST.get('inmueble_actual',0)
        

        i = alarmas.Alarma()
        
        user = self.request.user
        inmuebles = Inmueble.objects.all().filter(user_id = user.id).order_by('-estado')
        info = {}
    
        res = i.hay_nuevas_notificaciones(user)
        if res == True:
            num_alarmas = i.contar_nuevas_notificaciones(user)
            info['pendientes'] = num_alarmas

        


        if alarma_formset.is_valid():
            
            if sensor_id != '0':
            
                for form in alarma_formset.forms:
                    alarma = form.save(commit=False)
                    sensor = Sensor.objects.all().filter(id = sensor_id)
                    alarma.sensor = sensor[0]
                    alarma.nivel_alarma = nivel_id
                    self.set_data_alarma(tipo_alarma,alarma)
            
                    alarma.save()
            else:
            
                error_sensor= '* This field is required.'
                i = alarmas.Alarma()
                sensores = i.consul_sensores_inmb( inmueb_id = inmu_id,tipo_sensor = tipo_alarma)

                return  render(request,'core_app/crear_alarma.html', locals())
            
                #return  render_to_response('core_app/crear_alarma.html', locals(),
                #        RequestContext(request))
                    
        else:
            
            i = alarmas.Alarma()
            sensores = i.consul_sensores_inmb( inmueb_id = inmu_id,tipo_sensor = tipo_alarma)
            
            return  render(request,'core_app/crear_alarma.html', locals())
                    

            #return  render_to_response('core_app/crear_alarma.html', locals(),
            #        RequestContext(request))


        
        return HttpResponseRedirect('../')

    def get(self,request):
        
        class RequiredFormSet(BaseFormSet):
            def __init__(self, *args, **kwargs):
                super(RequiredFormSet, self).__init__(*args, **kwargs)
                for form in self.forms:
                    form.empty_permitted = False

        if 'tipo_alarma' in self.request.GET:
            alarma_id = self.request.GET['tipo_alarma']
        else:
            return  render(request,'core_app/home_list.html', locals())
            #return  render_to_response('core_app/home_list.html', locals(),
            #                    RequestContext(request))

        tipo_alarma = self.request.GET['tipo_alarma']

        i = alarmas.Alarma()
        
        user = self.request.user
        inmuebles = Inmueble.objects.all().filter(user_id = user.id).order_by('-estado')
        info = {}
    
        res = i.hay_nuevas_notificaciones(user)
        if res == True:
            num_alarmas = i.contar_nuevas_notificaciones(user)
            info['pendientes'] = num_alarmas

        if inmuebles.__len__() > 0:
            info['inmuebles'] = inmuebles
            
            if 'inmu_id' in self.request.GET:
        
                inmueble_param_id = self.request.GET['inmu_id']
                info['elementos'] = Elemento.objects.all().filter(
                     inmu_id = inmueble_param_id, user_id = user.id).order_by('-estado')

                info['inmueble_actual'] = Inmueble.objects.get(pk=inmueble_param_id)
                inmueble_actual = info['inmueble_actual'].id

            else:
        
                primer_inmueble = inmuebles[0]
                info['elementos'] = Elemento.objects.all().filter(
                     inmu_id = primer_inmueble.id, user_id = user.id).order_by('-estado')
                info['inmueble_actual'] = Inmueble.objects.get(pk=primer_inmueble.id)
                inmueble_actual = info['inmueble_actual'].id

        sensores = i.consul_sensores_inmb( inmueb_id = info['inmueble_actual'].id,tipo_sensor = tipo_alarma)

        if tipo_alarma=='1' :
            alarm_form_set = formset_factory(AlarmaHumoForm, extra=1, max_num=10, formset=RequiredFormSet)
        elif tipo_alarma=='2':
            alarm_form_set = formset_factory(AlarmaEstado2Form, extra=1, max_num=10, formset=RequiredFormSet)
        elif tipo_alarma=='3':
            alarm_form_set = formset_factory(AlarmaAccesoForm, extra=1, max_num=10, formset=RequiredFormSet)    
        elif tipo_alarma=='4':
            alarm_form_set = formset_factory(AlarmaEstadoForm, extra=1, max_num=10, formset=RequiredFormSet)

            
        else:


            return  render(request,'core_app/home_list.html', locals())
            #return  render_to_response('core_app/home_list.html', locals(),
            #                    RequestContext(request))
    
        alarma_formset = alarm_form_set()


        return  render(request,'core_app/crear_alarma.html', locals())
        #return  render_to_response('core_app/crear_alarma.html', locals(),
        #                        RequestContext(request))

class TipoAlarmsView(TemplateView):
    template_name = 'core_app/tipo_alarmas.html'
    
    def get(self,request):
        

        user = self.request.user
        inmuebles = Inmueble.objects.all().filter(user_id = user.id).order_by('-estado')
        i = alarmas.Alarma()
        info = {}
        
        res = i.hay_nuevas_notificaciones(user)
        if res == True:
            num_alarmas = i.contar_nuevas_notificaciones(user)
            info['pendientes'] = num_alarmas

        if inmuebles.__len__() > 0:
            info['inmuebles'] = inmuebles
            
            if 'inmu_id' in self.request.GET:
                inmueble_param_id = self.request.GET['inmu_id']
                info['elementos'] = Elemento.objects.all().filter(
                     inmu_id = inmueble_param_id, user_id = user.id).order_by('-estado')
                alarma = i.consul_alarms_inmb(inmueb_id = inmueble_param_id,tipo_sensor_id='0')

                info['inmueble_actual'] = Inmueble.objects.get(pk=inmueble_param_id)

            else:
                primer_inmueble = inmuebles[0]
                info['elementos'] = Elemento.objects.all().filter(
                     inmu_id = primer_inmueble.id, user_id = user.id).order_by('-estado')

                if user.id != None:
                    alarma = i.consul_alarms(user_id = user.id,tipo_sensor_id='0')
                    info['elementos'] = Elemento.objects.all().filter(user_id = user.id).order_by('-estado')
        
        
        info['alarmas'] = alarma

        return  render(request,self.template_name, locals())
        #return  render_to_response(self.template_name, locals(),
        #                RequestContext(request))        



class AlarmReportsView(ListView):
    context_object_name = 'info'
    template_name = 'core_app/alarmas_history.html'
    
    def get_queryset(self):
                    
        user = self.request.user
        inmuebles = Inmueble.objects.all().filter(user_id = user.id).order_by('-estado')
        fecha1  = None#'2015-01-19' #self.request.GET['fech_1']
        fecha2  = None#'2015-03-19'# '2015-02-18''2015-03-01'#self.request.GET['fech_1']

        resultado = {}
        i = alarmas.Alarma()
        res = i.hay_nuevas_notificaciones(user)
        if res == True:
            num_alarmas = i.contar_nuevas_notificaciones(user)
            resultado['pendientes'] = num_alarmas

        resultado['inmuebles'] = inmuebles  
        if 'inmu_id' in self.request.GET and self.request.GET['inmu_id'] != "":
            inmb_id = self.request.GET['inmu_id']
            resultado['inmueble_actual'] = Inmueble.objects.get(pk=inmb_id)
            resultado['elementos'] = Elemento.objects.all().filter(inmu_id = inmb_id, user_id = user.id).order_by('-estado')
        
            eventos = i.consul_history_inmb(inmueb_id = inmb_id, fecha1 = fecha1, fecha2 = fecha2)
        else:
            if 'elemento_id' in self.request.GET and self.request.GET['elemento_id'] != "":
                elm_id = self.request.GET['elemento_id']
                resultado['elemento_actual'] = Elemento.objects.get(pk=elm_id)
                resultado['inmueble_actual'] = resultado['elemento_actual'].inmueble
                resultado['elementos'] = Elemento.objects.all().filter(inmu_id = resultado['inmueble_actual'].id, user_id = user.id).order_by('-estado')
                
                eventos = i.consul_history_elem(elem_id = elm_id, fech_1 = fecha1, fech_2 = fecha2)
            else:
                if user.id != None:
                    
                    eventos = i.consul_history(user_id = user.id, fech_1 = fecha1, fech_2 = fecha2)
                    resultado['elementos'] = Elemento.objects.all().filter(user_id = user.id).order_by('-estado')
        
        resultado['reporte'] = eventos
        maxdatetime = datetime.datetime.today()
        for evento in eventos:
            if evento.get('fecha_hora').date() > maxdatetime.date():
                maxdatetime = evento.get('fecha_hora')
        resultado['maxdatetime'] = maxdatetime
        return resultado


#creacion de elementos
class CrearElementoView(TemplateView):
    state = 0
    def post(self,request):
        print("paso 1")

        class RequiredFormSet(BaseFormSet):
            def __init__(self, *args, **kwargs):
                super(RequiredFormSet, self).__init__(*args, **kwargs)
                for form in self.forms:
                    form.empty_permitted = False


        print("paso 2")
        info = {}
        user = self.request.user
        i = alarmas.Alarma()
        print("paso 3")

        res = i.hay_nuevas_notificaciones(user)
        if res == True:
            num_alarmas = i.contar_nuevas_notificaciones(user)
            info['pendientes'] = num_alarmas
            print("paso 4")

        if 'inmu_id' in self.request.POST:

            inmueble_param_id = self.request.POST['inmu_id']
            info['elementos'] = Elemento.objects.all().filter(
                 inmu_id = inmueble_param_id, user_id = user.id).order_by('-estado')

            info['inmueble_actual'] = Inmueble.objects.get(pk=inmueble_param_id)
            print("paso 5")


        else:

            return  render(request,'core_app/home_list.html', locals())
            #return  render_to_response('core_app/home_list.html', locals(),
            #                RequestContext(request))
        
        alarm_form_set = formset_factory(ElementoForm, extra=1, max_num=10, formset=RequiredFormSet)
    
        alarma_formset = alarm_form_set(request.POST, request.FILES)
        
        if alarma_formset.is_valid():            
            
            for form in alarma_formset.forms:

                nombre = form.cleaned_data['nombre']
                elemento = Elemento(nombre = nombre,estado=0,inmu=info['inmueble_actual'],user = self.request.user)
                elemento.save()
                tipo = TipoSensor.objects.get(pk=2)
                sensor = Sensor(nombre = nombre,activo=elemento,tipo_sensor=tipo)
                sensor.save()
                
        else:
            
            return  render(request,'core_app/crear_elemento.html', locals())
            #return  render_to_response('core_app/crear_elemento.html', locals(),
            #        RequestContext(request))

        return HttpResponseRedirect('../')

    def get(self,request):
        
        class RequiredFormSet(BaseFormSet):
            def __init__(self, *args, **kwargs):
                super(RequiredFormSet, self).__init__(*args, **kwargs)
                for form in self.forms:
                    form.empty_permitted = False

        
        alarm_form_set = formset_factory(ElementoForm, extra=1, max_num=10, formset=RequiredFormSet)
            
    
        user = self.request.user
        inmuebles = Inmueble.objects.all().filter(user_id = user.id).order_by('-estado')
        info = {}

        i = alarmas.Alarma()

        res = i.hay_nuevas_notificaciones(user)
        if res == True:
            num_alarmas = i.contar_nuevas_notificaciones(user)
            info['pendientes'] = num_alarmas

    
        if inmuebles.__len__() > 0:
            info['inmuebles'] = inmuebles
            
            if 'inmu_id' in self.request.GET:
                inmueble_param_id = self.request.GET['inmu_id']
                info['elementos'] = Elemento.objects.all().filter(
                     inmu_id = inmueble_param_id, user_id = user.id).order_by('-estado')

                info['inmueble_actual'] = Inmueble.objects.get(pk=inmueble_param_id)

            else:
                primer_inmueble = inmuebles[0]
                info['elementos'] = Elemento.objects.all().filter(
                     inmu_id = primer_inmueble.id, user_id = user.id).order_by('-estado')
                info['inmueble_actual'] = Inmueble.objects.get(pk=primer_inmueble.id)

        alarma_formset = alarm_form_set()



        return  render(request,'core_app/crear_elemento.html',locals())
        #return  render_to_response('core_app/crear_elemento.html', locals(),
        #                        RequestContext(request))



#Borrado de elementos
class BorrarElementoView(TemplateView):
    state = 0

    def get(self,request):
        
        
        if 'elemento_id' in self.request.GET:
            elemento_id = self.request.GET['elemento_id']
            elemento = Elemento.objects.get(pk=elemento_id)
            elemento.delete()


        else:
            return HttpResponseRedirect('../')

        return HttpResponseRedirect('../')


#creacion de alarmas
class SimuladorView(TemplateView):

    def post(self,request):

        class RequiredFormSet(BaseFormSet):
            def __init__(self, *args, **kwargs):
                super(RequiredFormSet, self).__init__(*args, **kwargs)
                for form in self.forms:
                    form.empty_permitted = False

        event_form_set = formset_factory(EventoForm, extra=1, max_num=1, formset=RequiredFormSet)
        
        alarma_formset = event_form_set(request.POST, request.FILES)

        if alarma_formset.is_valid():
                
       
                for form in alarma_formset.forms:
                    
                    evento = Evento(
                    nombre = form.cleaned_data['nombre'],
                    codigo  = form.cleaned_data['mensaje'],
                    trama   = form.cleaned_data['mensaje'],
                    fecha_hora_evento = form.cleaned_data['fecha_hora'],
                    fecha_hora_sistema = form.cleaned_data['fecha_hora'],
                    sensor   = form.cleaned_data['sensor'])

                    if evento.codigo == 0 or evento.codigo == '0':
                        evento.codigo == '0'
                    else:
                        evento.codigo == '1'

                    evento.save()

                    i = alarmas.Alarma()
                    i.validar_alarma(evento,evento.sensor.activo.user)
        else:
            
            
            return  render(request,'core_app/api_index.html',locals())
            #return  render_to_response('core_app/api_index.html', locals(),
            #        RequestContext(request))
        
        
        return HttpResponseRedirect('../')

    def get(self,request):
        
        class RequiredFormSet(BaseFormSet):
            def __init__(self, *args, **kwargs):
                super(RequiredFormSet, self).__init__(*args, **kwargs)
                for form in self.forms:
                    form.empty_permitted = False
        
        user = self.request.user
        inmuebles = Inmueble.objects.all().filter(user_id = user.id).order_by('-estado')
        resultado = {}
    
        evento_form_set = formset_factory(EventoForm, extra=0, max_num=10, formset=RequiredFormSet)
    
        alarma_formset = evento_form_set(
            initial=[{
            'fecha_hora': datetime.datetime.today(),
            }])
            


        return  render(request,'core_app/api_index.html',locals())
        #return  render_to_response('core_app/api_index.html', locals(),
        #                        RequestContext(request))
