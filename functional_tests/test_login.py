from django.test.client import Client
from django.contrib.auth.models import User
from .base import FunctionalTest
      

class LoginTest(FunctionalTest):#TestCase
    username = 'hernan'
    password = '000000'
    email = 'hernan@uniandes.com'
        
    def setUp(self):
        # Cada uno de los test necesita ser ejecutado en un cliente
        self.client = Client()
        #Para verificar el login, se debe primero crea el usuario con el que se va a probar
        self.user = User.objects.create_user(self.username, self.email, self.password)
    
    #Método que verifica el proceso de login cuando se accede al API directo del cliente
    def test_login_by_client(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login)
    
    #Método que verifica el proceso de login cuando no se ingresan las credenciales correctas
    def test_login_error_by_client(self):
        login = self.client.login(username='userNonExist', password=self.password)
        self.assertFalse(login)
    
    #Método que verifica el proceso de login cuando se accede directamente a la url de login
    def test_login_by_url(self):
        response = self.client.post('/login/', {'username': self.username, 'password': self.password}, follow=True)
        self.assertEqual(response.status_code, 200, "Se esperaba un OK (200) en el response")
        
        #Se verifica que se tenga acceso al inicio de la app
        response = self.client.get('/app/')
        self.assertEqual(response.status_code, 200)
        
    
        
    

