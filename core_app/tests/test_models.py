from django.contrib.auth.models import User
from core_app.models import Proyecto, Activo, HistoryAlarmas, Inmueble, Elemento
import datetime
from functional_tests.base import FunctionalTest

class HistoryAlarmasTest(FunctionalTest):#TestCase
    
    def test_history_alarmas(self):
        histalm = HistoryAlarmas()
        histalm.fecha = datetime.datetime.now() #datetime.timedelta(days=1) # 1 day ago
        self.assertNotEqual(histalm.estado, False)
        self.assertTrue(histalm.is_over())

class InmuebleTest(FunctionalTest):
    nom_inm = "Inmueble test"
    estado_inicial_inmueble = 2
    estado_final_inmueble = 1
    
    nom_elm = "Elemento test"
    estado_inicial_elemento = 2
    estado_final_elemento = 1

    def test_inmueble(self):

        self.user = User.objects.create(username="test_user_al", password="pass", email="test@test.co")
        self.proyecto = Proyecto.objects.create(nombre="Proyecto_test")
        self.activo_to_inmueble = Activo.objects.create(user=self.user)
        self.activo_to_elemento = Activo.objects.create(user=self.user)
        self.inmueble = Inmueble(activo_ptr=self.activo_to_inmueble, proyecto = self.proyecto)
        self.inmueble.name = self.nom_inm
        self.inmueble.estado = self.estado_inicial_inmueble
        
        self.assertNotEqual(self.inmueble.name, '')
        self.assertEqual(self.inmueble.estado, 2)
        
        self.elemento = Elemento(activo_ptr=self.activo_to_elemento, inmueble = self.inmueble)
        self.elemento.name = self.nom_elm
        self.elemento.estado = self.estado_inicial_elemento
        
        self.assertNotEqual(self.elemento.name, '')
        self.assertEqual(self.elemento.estado, 2)

    