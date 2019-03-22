# -*- coding: utf-8 -*- 
import smtplib 
from email.mime.text import MIMEText
from core_app.correo.sms_sender import SenderSMS
import datetime

 
class MyCorreo:

# Construimos el mensaje simple
    mensaje = MIMEText("""Correo electronico de pruebas
    Verificacion de envio exitosa. Por favor No contestar""")
    mensaje['From']="mysmarthome4101@gmail.com"
    mensaje['To']="jhonyt37@gmail.com" #
    mensaje['Subject']="Correo de pruebas"

    def set_remitente(self,remitente):
        self.mensaje['From']=remitente

    def set_destinatario(self,dest):
        self.mensaje['To']=dest

    def enviar_gmail(self,tipo_alarma,destinatario,activo,user,nombre_alarma):
        
        mi_mensaje= self.mensaje
        mail_server = smtplib.SMTP('smtp.gmail.com',587)
        mail_server.ehlo()        
        mail_server.starttls()
        
        mail_server.ehlo()
        
        mail_server.login(self.mensaje['From'],"zvjktuetqawucpqk")

        

        print("enviado a : "+ mi_mensaje['To'])

        if tipo_alarma == "2" or tipo_alarma == 2:
            tipo_sms = "Critica"
        elif tipo_alarma == "1" or tipo_alarma == 1:
            tipo_sms = "Seguridad"
        elif tipo_alarma == "0" or tipo_alarma == 0:
            tipo_sms = "Evento"
        
        mi_mensaje = MIMEText("Correo electronico generado por el activo " + activo +
        ". Verificacion de envio exitosa. Alarma activada tipo "+tipo_sms)

        if tipo_alarma == "2" or tipo_alarma == 2:
            mi_mensaje['Subject']="Alerta critica registrada"
        elif tipo_alarma == "1" or tipo_alarma == 1:
            mi_mensaje['Subject']="Alerta de Seguridad registrada"
        elif tipo_alarma == "0" or tipo_alarma == 0:
            mi_mensaje['Subject']="Notificacion de evento registrado"

        mi_mensaje['From']=self.mensaje['From']
        mi_mensaje['To']=destinatario
        #print (mail_server.ehlo())

        # Envio del mensaje
        mail_server.sendmail(mi_mensaje['From'],
	                mi_mensaje['To'],
                     mi_mensaje.as_string())
        myuser = user.first_name
        if myuser == "":
            myuser = user.username
        sms_mensaje = "Hola " + myuser + ", Se ha activado la alarma " + nombre_alarma + " tipo: "+ tipo_sms + ". Originado por " +activo + " el " + datetime.datetime.now().strftime("%d/%m/%y") +" a las "+ datetime.datetime.now().strftime("%H:%M")

        # Envio del sms
        #para enviar my_sms_client = SenderSMS(testing_mode=False)
        #sms_mensaje:string mensaje 
        #user.last_name numero telefonico con indicador de pais
        #para enviar my_sms_client.send_sms(sms_mensaje, user.last_name)

        # Cierre de la conexion
        mail_server.close()
