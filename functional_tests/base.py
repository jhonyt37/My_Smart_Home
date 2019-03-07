from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.client import Client
from django.contrib.auth.models import User

# Create your tests here.
class FunctionalTest(StaticLiveServerTestCase):
    username = 'hernan'
    password = '000000'
    email = 'hernan@uniandes.com'
    
    @classmethod
    def setUpClass(cls):
        super(FunctionalTest, cls).setUpClass()
        
    @classmethod
    def tear_down_class(cls):
        super(FunctionalTest, cls).tearDownClass()
        
    #Método que se ejecuta al inicio de cada uno de los métodos de prueba
    def setUp(self):
        # Cada uno de los test necesita ser ejecutado en un cliente
        self.client = Client()
        #Para verificar el login, se debe primero crea el usuario con el que se va a probar
        self.user = User.objects.create_user(self.username, self.email, self.password)
    
    #Método que se ejecuta al final de cada uno de los métodos de prueba    
    def tearDown(self):
        self.user.delete()
        self.client.logout()
