# -*- encoding: utf-8 -*-
from enum import IntEnum

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import datetime


class GenericModel(models.Model):
    #Representacion como cadena del objeto
    def __str__(self):
        return 'Objeto {className} con Id[{modelId}]'.format(
            className=self.__class__.__name__, modelId=self.id)
    
    class Meta: 
        abstract = True
        
class GenericModelWithName(GenericModel):
    nombre = models.CharField(max_length=255, default='')
    
    class Meta: 
        abstract = True
        
    #Representación como cadena del objeto
    def __str__(self):
        return self.nombre

# Create your models here.
# Clase que representa cada una de las pertenencias de un usuario
class NivelAlerta(IntEnum):
    ROJO = 2
    AMARILLO = 1
    VERDE = 0
    
class Activo(GenericModelWithName):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    #Contiene el estado actual notificado por un evento sobre el activo
    estado = models.IntegerField(default=2, validators=[MinValueValidator(0), MaxValueValidator(2)])
    
    class Meta:
        ordering = ['estado']
        
#Clase que agrupa los inmuebles
class Proyecto(GenericModelWithName):
    pass
    
#Clase que representa las propiedades del usuario fijas como Apto, Oficina, etc 
class Inmueble(Activo):
    proyecto = models.ForeignKey(Proyecto,on_delete=models.CASCADE)
    embebido = models.CharField(max_length=1023, default='')
    def set_estado(self, estado):
        if estado>=0 or estado<3:
            self.estado = estado
            return True
        else:
            return False
    
#Clase que representa los electrodomésticos y demás elementos dentro de un inmueble
class Elemento(Activo):
    inmu = models.ForeignKey(Inmueble,on_delete=models.CASCADE)
    def set_estado(self, estado):
        if estado == 0:
            self.estado = estado
            return True
        elif estado == 1:
            self.estado = estado
            if self.inmueble.estado == 0:
                self.inmueble.set_estado(estado)
            return True
        elif estado == 2:
            self.estado = estado
            if self.inmueble.estado < 2:
                self.inmueble.set_estado(estado)
            return True
        else:
            return False



#Clase que tiene los tipos de sensores
class TipoSensor(GenericModelWithName):
    descripcion = models.CharField(max_length=255,default='')
#Clase que representa a un sensor físico (RFID, Gases, Incendio, etc) 
class Sensor(GenericModelWithName):
    #Objeto/Inmueble al que se asocia el sensor
    activo = models.ForeignKey(Elemento,on_delete=models.CASCADE)
    tipo_sensor = models.ForeignKey(TipoSensor,default=1,on_delete=models.CASCADE)

#Clase que representa los eventos generados por un sensor
class Evento(GenericModelWithName): #GenericModel
    codigo  = models.CharField(max_length=10)
    trama   = models.CharField(max_length=1000)
    fecha_hora_evento = models.DateTimeField(datetime.datetime.today())
    fecha_hora_sistema = models.DateTimeField(datetime.datetime.today())
    sensor   = models.ForeignKey(Sensor,default='',on_delete=models.CASCADE)

    

#Clase que representa las alarmas que pueden ser configuradas para un sensor/evento
class Alarma(GenericModelWithName):
    #Determina si la alarma se encuentra activada
    descripcion = models.CharField(max_length=512,default='')
    sensor = models.ForeignKey(Sensor,on_delete=models.CASCADE)
    activa = models.BooleanField(default=True)
    notifica = models.BooleanField(default=True)
    eliminada = models.BooleanField(default=False)
    nivel_alarma = models.IntegerField(default=2, validators=[MinValueValidator(0), MaxValueValidator(2)])


#Clase que representa alarma de tipo Humo
class AlarmaHumo(Alarma):
    pass
#Clase que representa alarma de tipo Acceso
class AlarmaAcceso(Alarma):
    hora_inicio = models.TimeField(help_text='hh:mm:ss')
    hora_fin = models.TimeField(help_text='hh:mm:ss')

#Clase que representa alarma de tipo Estado
class AlarmaEstado(Alarma):
    
    estado_sensor = models.BooleanField(default=True)
    hora_inicio = models.TimeField(help_text='hh:mm:ss')
    hora_fin = models.TimeField(help_text='hh:mm:ss')

#Alarmas reportadas
class AlarmaReportada(GenericModelWithName):
    descripcion = models.CharField(max_length=512,default='')
    alarma = models.ForeignKey(Alarma,on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(datetime.datetime.today())
    nivel_alerta = models.IntegerField(default=2, validators=[MinValueValidator(0), MaxValueValidator(2)])
    leida = models.BooleanField(default=False)

##Otras clases
class HistoryAlarmas(GenericModel):
    estado    = models.BooleanField(default=True)
    fecha     = models.DateTimeField()
    elemento  = models.ForeignKey(Elemento,on_delete=models.CASCADE)
    inmueble  = models.ForeignKey(Inmueble,on_delete=models.CASCADE)
    sensor   = models.ForeignKey(Sensor,on_delete=models.CASCADE)
    alarma   = models.ForeignKey(Alarma,on_delete=models.CASCADE)
    
    def is_over(self):
        return datetime.datetime.now() > self.fecha #<=
