from django.test.client import Client
from django.contrib.auth.models import User
from core_app.models import Inmueble, Elemento, Proyecto, Activo, Sensor, TipoSensor, AlarmaAcceso,AlarmaReportada
from .base import FunctionalTest
import datetime
from core_app.sensores import  alarmas
      

class AlarmasPendientes(FunctionalTest):#TestCase
    nombre = "Alarma test"
    descripcion = "descripcion alarma"
    nivel_alerta = 2
    leida = 0
    activa = 1
    notifica = 1
    
    
    def setUp(self):
        c = Client()
        c.login(username="test_user_last", password='pass')

        self.user = User.objects.create(username="test_user_al", password="pass", email="test@test.co")
        self.proyecto = Proyecto.objects.create(nombre="Proyecto_test")
        self.inmueble = Inmueble.objects.create(nombre="inmueble_test",
                                           proyecto=self.proyecto,
                                           user = self.user)
        self.activoCreado = Activo.objects.create(nombre = "activo_test",user = self.user,estado=2)
        self.elementoCreado = Elemento.objects.create(inmueble=self.inmueble,user = self.user,estado=2)
        self.inmueble.proyecto = self.proyecto
        self.tipo = TipoSensor.objects.create(nombre="electrico")

        self.sensorCreado = Sensor.objects.create(
            #Objeto/Inmueble al que se asocia el sensor
            activo = self.elementoCreado,
            tipo_sensor = self.tipo
            )
        self.hora_fin = 0
        self.hora_ini = 0
        self.nivel_alerta = 2
        self.alarmaCreada= AlarmaAcceso.objects.create(nombre=self.nombre,                
                nivel_alarma=self.nivel_alerta,
                hora_fin=datetime.datetime.today(), 
                hora_inicio=datetime.datetime.today(),
                descripcion = "hola mundo",
                sensor = self.sensorCreado,
                activa = self.activa,
                notifica = self.notifica,
                eliminada = self.notifica
                
                )
        self.alarma = AlarmaReportada.objects.create(nombre=self.nombre,
                nivel_alerta=self.nivel_alerta, 
                alarma=self.alarmaCreada, 
                fecha_hora = datetime.datetime.today(),
                leida = self.leida)

    #Método que verifica que no existen Notificaciones en la DB
    def test_no_hay_notificaciones(self):

        i = alarmas.Alarma()

        self.alarma.delete()

        num_alarma = AlarmaReportada.objects.all().filter(
                    alarma__sensor__activo__user_id=self.user.id)

        if num_alarma.__len__() > 0:
            num = num_alarma.__len__()
        else:
            num = 0

        res = i.hay_nuevas_notificaciones(self.user.id)
        self.assertTrue(res==num)

    #Método que verifica que todas las Notificaciones de ese usuario esten leidas
    def test_todas_noti_leidas(self):

        i = alarmas.Alarma()

        self.alarma.leida=1
        self.alarma.save()

        num_alarma = AlarmaReportada.objects.all().filter(
                    alarma__sensor__activo__user_id=self.user.id,
                    leida=0)

        if num_alarma.__len__() > 0:
            num = num_alarma.__len__()
        else:
            num = 0

        res = i.hay_nuevas_notificaciones(self.user.id)
        self.assertTrue(res==num)

    #Método que verifica si tiene notificaciones pendientes por leer ese usuario
    def test_pendiente_notifica_leidas(self):

        i = alarmas.Alarma()

        num_alarma = AlarmaReportada.objects.all().filter(
                    alarma__sensor__activo__user_id=self.user.id,
                    leida=0)

        if num_alarma.__len__() > 0:
            num = num_alarma.__len__()
        else:
            num = 0

        res = i.hay_nuevas_notificaciones(self.user.id)
        #simulando el retorno de la funcion res = 1
        self.assertTrue(res==num)

    #Método que obtiene el numero de Notificaciones No leidas de ese usuario
    def test_contar_no_leidas(self):

        i = alarmas.Alarma()

        self.alarma.leida=1
        self.alarma.save()

        num_alarma = AlarmaReportada.objects.all().filter(
                    alarma__sensor__activo__user_id=self.user.id,
                    leida=0)

        if num_alarma.__len__() > 0:
            num = num_alarma.__len__()
            #simulando numero de alarmas num = 5
        else:
            num = 0

        res = i.contar_nuevas_notificaciones(self.user.id)
        self.assertTrue(res==num)

    def tearDown(self):
        self.proyecto.delete()
        self.user.delete()
        self.client.logout()



    
    
        
    

