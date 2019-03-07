from django.test.client import Client
from django.contrib.auth.models import User
from core_app.models import Inmueble, Elemento, Proyecto, Activo
from .base import FunctionalTest

class EstadoInmueble(FunctionalTest):#TestCase
    nombre = "Inmueble test"
    estado_inicial_inmueble = 2
    estado_final_inmueble = 1

    estado_inicial_elemento = 2
    estado_final_elemento = 1
    username = "user_test"
    password = "pass"
    email = "test"
    
    
    def setUp(self):
        self.client = Client()
        
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.proyecto = Proyecto.objects.create(nombre="Proyecto_test")

        self.activo_to_inmueble = Activo.objects.create(user=self.user)
        self.inmueble = Inmueble(activo_ptr=self.activo_to_inmueble, proyecto = self.proyecto)
        self.inmueble.name = self.nombre
        self.inmueble.estado = self.estado_inicial_inmueble
        
        self.activo_to_elemento = Activo.objects.create(user=self.user)
        self.elemento = Elemento(activo_ptr=self.activo_to_elemento, inmueble = self.inmueble)
        self.elemento.name = self.nombre
        self.elemento.estado = self.estado_inicial_elemento

    #Método que verifica que el estado del inmueble cambie cuando se hace un set en el estado del inmueble
    def test_estado_inmueble(self):
        self.inmueble.set_estado(self.estado_final_inmueble)
        self.assertTrue(self.estado_final_inmueble == self.inmueble.estado)

    #Método que verifica que el estado del elemento cambie cuando se hace un set en el estado del inmueble
    def test_estado_elemento(self):
        self.elemento.set_estado(self.estado_final_elemento)
        self.assertTrue(self.estado_final_elemento == self.elemento.estado)

    #Método que verifica que el estado del elemento cambie cuando se hace un set en el estado del inmueble
    def test_estado_elemento_inmueble(self):
        self.elemento.set_estado(self.estado_final_elemento)
        self.assertTrue(self.estado_final_inmueble <= self.elemento.inmueble.estado)
    
        
    def tear_down(self):
        self.user.delete()
        self.proyecto.delete()
        self.inmueble.delete()
        self.elemento.delete()
        self.client.logout()