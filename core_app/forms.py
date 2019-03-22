from django import forms
from core_app.models import Alarma,AlarmaHumo,AlarmaEstado,AlarmaAcceso, Elemento, Evento


class AlarmForm(forms.Form):

	class Meta:
		model = Alarma
		exclude = ('eliminada',)

class AlarmaHumoForm(forms.ModelForm):

	sensor = forms.ChoiceField(required=False)
	nivel = forms.ChoiceField(required=False)
	class Meta:
		model = AlarmaHumo
		exclude = ('eliminada','sensor','nivel_alarma')

class AlarmaEstadoForm(forms.ModelForm):
	
	sensor = forms.ChoiceField(required=False)
	estado = forms.BooleanField(required=False,help_text='Cerrado=[] Abierto=[X]')
	nivel = forms.ChoiceField(required=False)
	
	class Meta:
		model = AlarmaEstado
		exclude = ('eliminada', 'estado_sensor','nivel_alarma','sensor')

class AlarmaEstado2Form(forms.ModelForm):
	sensor = forms.ChoiceField(required=False)
	estado = forms.BooleanField(required=False, help_text='apagado=[] Encendido=[X]')
	nivel = forms.ChoiceField(required=False)
	hora_inicio = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
	hora_fin = forms.TimeField(widget=forms.TimeInput)

	class Meta:
		model = AlarmaEstado
		exclude = ('eliminada', 'estado_sensor','nivel_alarma','sensor', 'hora_inicio','hora_fin')

class AlarmaAccesoForm(forms.ModelForm):
	sensor = forms.ChoiceField(required=False)
	nivel = forms.ChoiceField(required=False)
	class Meta:
		model = AlarmaAcceso
		exclude = ('eliminada', 'estado_sensor','nivel_alarma','sensor')

class ElementoForm(forms.ModelForm):
	class Meta:
		model = Elemento
		exclude = ('inmueble', 'user','estado')


class EventoForm(forms.ModelForm):
	mensaje = forms.CharField(max_length=10, min_length=1)
	fecha_hora = forms.DateTimeField()
	class Meta:
		model = Evento
		exclude = ( 'fecha_hora_sistema', 'fecha_hora_evento', 'trama','codigo')
		