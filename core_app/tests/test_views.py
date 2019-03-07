from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core import mail
from core_app.models import Inmueble, Elemento

class CorreoTest(TestCase):    
    def test_enviar_gmail(self):
        # Send message.
        mail.send_mail('Correo de pruebas', 'Here is the message.',
            'mysmarthome4101@gmail.com', ['jhonyt37@gmail.com'],
            fail_silently=False)
        
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)
        
        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Correo de pruebas')


class HomeListTest(TestCase):        
    username = 'admin'#self.request.user
    password = 'admin'
    email = 'ing.rojas.m@gmail.com'#self.request.mail() #'hernan@uniandes.com'
    
    #Método que se ejecuta al inicio de cada uno de los métodos de prueba
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(self.username, self.email, self.password)
        
    def test_displays_all_items(self):
        items = Inmueble.objects.first()
        self.assertEqual(items, None) #assertTrue(items == None)
        
    def test_displays_all_elems(self):
        elems = Elemento.objects.first()  
        self.assertEqual(elems, None)        
        
    def tearDown(self):
        self.user.delete()
        self.client.logout()

