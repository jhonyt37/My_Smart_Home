from core_app.models import HistoryAlarmas, AlarmaReportada, Inmueble, Elemento, Evento, Sensor,Alarma as MyAlarm,AlarmaEstado,AlarmaAcceso #,AlarmaHumo
from MySmartHome.settings import DB_NAME, DB_USER, DB_HOST, DB_PWD
import psycopg2
from core_app.correo import  correo

class Alarma:        
    
    def reg_act_alarmas(self, id_estado, fech, id_inmb, id_elemen):
        
        ha = HistoryAlarmas(estado = id_estado, fecha = fech, user = self.request.user, inmueble  = id_inmb, 
                            elemento = id_elemen)
        ha.save()
        
    def consul_events(self, user_id, fech_1, fech_2):
        result = []

        inmbs = Inmueble.objects.all().filter(user = user_id)
        
        for im in inmbs:
            result.extend(list(self.consul_events_inmb(inmueb_id = im.id, fecha1 = fech_1, fecha2 = fech_2)))
        
        return result 
    
    def consul_events_inmb(self, inmueb_id, fecha1, fecha2): 
        result = []

        elems = Elemento.objects.all().filter(inmu = inmueb_id)
        if elems.__len__() > 0:           
            for e in elems:
                result.extend(list(self.consul_events_elem(elem_id = e.id , fech_1 = fecha1, fech_2 = fecha2)))                       

        return result

    @staticmethod
    def consultar_fecha_ini(elem_id, fech_1):

        result  = []
        for x in list(Evento.objects.all().filter(sensor__activo__id = elem_id, fecha_hora_evento__gte = fech_1
                        ).select_related('evento__sensor__activo__inmu', 'evento__sensor__tiposensor'
                        ).values('nombre', 'fecha_hora_evento', 'codigo', 'sensor__tipo_sensor__nombre', 
                                 'sensor__activo__inmu__nombre', 'sensor__activo__nombre', 'sensor__nombre'
                        ).order_by('-fecha_hora_evento')[:20]):
                        #'prioridad', 
                result.append(x)
        return result

    @staticmethod
    def consultar_fecha_fin(elem_id, fech_2):

        result  = []
        for x in list(Evento.objects.all().filter(sensor__activo__id = elem_id, fecha_hora_evento__lte = fech_2
                            ).select_related('evento__sensor__activo__inmu', 'evento__sensor__tiposensor'
                            ).values('nombre', 'fecha_hora_evento', 'codigo', 'sensor__tipo_sensor__nombre', 
                                     'sensor__activo__inmu__nombre', 'sensor__activo__nombre', 'sensor__nombre'
                            ).order_by('-fecha_hora_evento')[:20]):
                #Evento.objects.get(Q(question__startswith='Who'), Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6)))
                    result.append(x)
        
        return result

    @staticmethod
    def consultar_fecha_rango(elem_id, fech_1, fech_2):

        result  = []
        for x in list(Evento.objects.all().filter(sensor__activo__id = elem_id, fecha_hora_evento__range = [fech_1, fech_2]
                            ).select_related('evento__sensor__activo__inmu', 'evento__sensor__tiposensor'
                            ).values('nombre', 'fecha_hora_evento', 'codigo', 'sensor__tipo_sensor__nombre', 
                                     'sensor__activo__inmu__nombre', 'sensor__activo__nombre', 'sensor__nombre'
                            ).order_by('-fecha_hora_evento')[:20]):
                
                    result.append(x)
        return result

    @staticmethod
    def consultar_sin_fecha(elem_id):

        result  = []
        for x in list(Evento.objects.all().filter(sensor__activo__id = elem_id
                            ).select_related('evento__sensor__activo__inmu', 'evento__sensor__tiposensor'
                            ).values('nombre', 'fecha_hora_evento', 'codigo', 'sensor__tipo_sensor__nombre', 
                                     'sensor__activo__inmu__nombre', 'sensor__activo__nombre', 'sensor__nombre'
                            ).order_by('-fecha_hora_evento')[:20]):
                    result.append(x)
        return result


    @classmethod
    def consul_events_elem(cls, elem_id, fech_1, fech_2):
        result  = []
        
        if fech_1 != None and fech_2 == None:
            result = cls.consultar_fecha_ini(elem_id=elem_id, fech_1=fech_1)
                                                         
        elif fech_2 != None and fech_1 != None:
            result = cls.consultar_fecha_rango(elem_id=elem_id, fech_1=fech_1,fech_2=fech_2)
            
        elif fech_1 == None and fech_2 != None:
            result = cls.consultar_fecha_fin(elem_id=elem_id,fech_2=fech_2)
        else:
            result = cls.consultar_sin_fecha(elem_id=elem_id)

        return result


    def consul_sensores(self, user_id, tipo_sensor):
        result = []

        inmbs = Inmueble.objects.all().filter(user = user_id)
        
        for im in inmbs:
            result.extend(list(self.consul_sensores_inmb(inmueb_id = im.id, tipo_sensor = tipo_sensor)))
        
        return result 

    def consul_sensores_inmb(self, inmueb_id, tipo_sensor ): 
        result = []

        print(" debug " +str(inmueb_id) +" tipo"+ str(tipo_sensor)+"--")

        elems = Elemento.objects.all().filter(inmu = inmueb_id)
        if elems.__len__() > 0:
            for e in elems:
                result.extend(list(self.consul_elementos_sensor(elem_id = e.id,  tipo_sensor = tipo_sensor)))

        return result

    @staticmethod
    def consul_elementos_sensor( elem_id, tipo_sensor):
        result  = []
        
        
        for x in list(Sensor.objects.all().filter(activo__id = elem_id, tipo_sensor__id = tipo_sensor
                    ).select_related('sensor__activo', 'sensor__tiposensor'
                    ).values().order_by('-id')[:20]):
            result.append(x)

        return result




    @staticmethod
    def consul_alarms( user_id,tipo_sensor_id):
        result = []

        inmbs = Inmueble.objects.all().filter(user = user_id)
        
        for im in inmbs:
            result.extend(list(consul_alarms_inmb(inmueb_id = im.id, tipo_sensor_id = tipo_sensor_id)))
        
        return result 
    
    @classmethod
    def consul_alarms_inmb(cls, inmueb_id,tipo_sensor_id): 
        result = []

        elems = Elemento.objects.all().filter(inmu = inmueb_id)
        
        if elems.__len__() > 0:
            for e in elems:
                result.extend(list(cls.consul_alarms_elem(elem_id = e.id,tipo_sensor_id=tipo_sensor_id )))

        return result

    @staticmethod
    def consul_alarms_elem( elem_id,tipo_sensor_id):

        result  = []
        if tipo_sensor_id != 0 and tipo_sensor_id != '' and tipo_sensor_id != '0':
            
            for x in list(MyAlarm.objects.all().filter(sensor__activo__id = elem_id, sensor__tipo_sensor__id= tipo_sensor_id
                    ).select_related('alarma__sensor__activo__inmu', 'alarma__sensor__tiposensor'
                    ).values('id','nombre', 'descripcion', 'sensor__tipo_sensor__nombre', 'sensor__tipo_sensor_id'
                             'sensor__activo__inmu__nombre', 'sensor__activo__nombre', 'sensor__nombre','nivel_alarma'
                    ).order_by('-id')[:20]):
                result.append(x)
        else:
            for x in list(MyAlarm.objects.all().filter(sensor__activo__id = elem_id
                    ).select_related('alarma__sensor__activo__inmu', 'alarma__sensor__tiposensor'
                    ).values('id','nombre', 'descripcion', 'sensor__tipo_sensor__nombre', 
                             'sensor__activo__inmu__nombre', 'sensor__activo__nombre', 'sensor__nombre','nivel_alarma'
                    ).order_by('-id')[:20]):
                result.append(x)

        return result


               
    def consul_history(self, user_id, fech_1, fech_2):
        result = []

        inmbs = Inmueble.objects.all().filter(user = user_id)
        
        for im in inmbs:
            result.extend(list(self.consul_history_inmb(inmueb_id = im.id, fecha1 = fech_1, fecha2 = fech_2)))
        
        return result 
    
    def consul_history_inmb(self, inmueb_id, fecha1, fecha2): 
        result = []

        elems = Elemento.objects.all().filter(inmu = inmueb_id)
        if elems.__len__() > 0:
            for e in elems:
                result.extend(list(self.consul_history_elem(elem_id = e.id , fech_1 = fecha1, fech_2 = fecha2)))                       

        return result
    
    @staticmethod
    def consul_history_elem( elem_id, fech_1, fech_2):
        result  = []
        

        if fech_1 != None and fech_2 == None:
            for x in list(HistoryAlarmas.objects.all().filter(sensor__activo__id = elem_id, fecha__gte = fech_1
                        ).select_related('alarmaReportada__alarma__sensor__activo__inmu', 'alarmaReportada__alarma__sensor__tiposensor'
                                ).values( 'fecha_hora', 'alarma__sensor__tipo_sensor__nombre', 
                                         'alarma__sensor__activo__inmu__nombre', 'alarma__sensor__activo__nombre', 'alarma__sensor__nombre'
                                ).order_by('-fecha_hora')[:20]):
                result.append(x)
                                                         
        elif fech_2 != None and fech_1 != None:
            for x in list(AlarmaReportada.objects.all().filter(alarma__sensor__activo__id = elem_id, fecha_hora__range = [fech_1, fech_2]
                        ).select_related('alarmaReportada__alarma__sensor__activo__inmu', 'alarmaReportada__alarma__sensor__tiposensor'
                            ).values( 'fecha_hora', 'alarma__nivel_alarma', 'alarma__nombre', 'alarma__descripcion', 'alarma__sensor__tipo_sensor__nombre', 
                                     'alarma__sensor__activo__inmu__nombre', 'alarma__sensor__activo__nombre', 'alarma__sensor__nombre'
                            ).order_by('-fecha_hora')[:20]):
        
                result.append(x)
        
        elif fech_1 == None and fech_2 != None:
            for x in list(AlarmaReportada.objects.all().filter(alarma__sensor__activo__id = elem_id, fecha_hora__lte = fech_2
                        ).select_related('alarmaReportada__alarma__sensor__activo__inmu', 'alarmaReportada__alarma__sensor__tiposensor'
                        ).values( 'fecha_hora', 'alarma__nivel_alarma', 'alarma__nombre', 'alarma__descripcion', 'alarma__sensor__tipo_sensor__nombre', 
                                 'alarma__sensor__activo__inmu__nombre', 'alarma__sensor__activo__nombre', 'alarma__sensor__nombre'
                        ).order_by('-fecha_hora')[:20]):
            
                result.append(x)
                
        else:
            for x in list(AlarmaReportada.objects.all().filter(alarma__sensor__activo__id = elem_id
                        ).select_related('alarmaReportada__alarma__sensor__activo__inmu', 'alarmaReportada__alarma__sensor__tiposensor'
                        ).values( 'fecha_hora', 'alarma__nivel_alarma', 'alarma__nombre', 'alarma__descripcion', 'alarma__sensor__tipo_sensor__nombre', 
                                 'alarma__sensor__activo__inmu__nombre', 'alarma__sensor__activo__nombre', 'alarma__sensor__nombre'
                        ).order_by('-fecha_hora')[:20]):
                result.append(x)                    

        return result

    @staticmethod
    def get_sec(s):
        
        l = s.split(':')
        return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])


    @classmethod
    def valida_horarios(cls,alarma,alarma_estado,evento):
        ret = False

        seg_max = cls.get_sec(s='23:59:59')
        seg_ini = cls.get_sec(s=str(alarma_estado.hora_inicio))
        seg_fin = cls.get_sec(s=str(alarma_estado.hora_fin))
        seg_eve = cls.get_sec(s=str(str(evento.fecha_hora_evento.hour)+':'+str(evento.fecha_hora_evento.minute)+':'+str(evento.fecha_hora_evento.second)))


        if seg_ini > seg_fin:
            if seg_eve>=seg_ini and seg_eve<=seg_max:
                print('entra a horario noche')
                ret = True
            elif seg_eve>=0 and seg_eve<=seg_fin:
                print('entra a horario nocturno')
                ret = True
        elif seg_ini < seg_fin:
            if seg_eve>=seg_ini and seg_eve<=seg_fin:
                print('entra a horario diurno')
                ret = True
        elif seg_ini == seg_fin and seg_eve==seg_ini:
                print('entra a horario fijo')
                ret = True

        return ret

    #metodo que actualiza los estados de inmueble y activo
    @staticmethod
    def actualizar_datos(alarma):
        connection=psycopg2.connect("host=" + HOST_DB + " dbname=" + DB_NAME + " user=" + DB_USER + " password=" + DB_PWD )
        cursor=connection.cursor()
        elemento_actual = Elemento.objects.get(pk=alarma.sensor.activo.id)
        inmueble_actual = Inmueble.objects.get(pk=alarma.sensor.activo.inmueble.id)

        if elemento_actual.estado<alarma.nivel_alarma:
            cursor.execute("UPDATE core_app_activo SET estado =" + str(alarma.nivel_alarma) + " WHERE id =" + str(alarma.sensor.activo.id))
            connection.commit()
        if inmueble_actual.estado<alarma.nivel_alarma:
            cursor.execute("UPDATE core_app_activo SET estado =" + str(alarma.nivel_alarma) + " WHERE id =" + str(alarma.sensor.activo.inmueble.id))
            connection.commit()

    #Método que genera la 
    #notificacion de alarma y cambia el estado del activo
    @classmethod
    def genera_alarma(cls,alarma,evento,user):
        print('genera alarma ')
        ##Otras clases
        if alarma.activa == False or alarma.activa == 0 or alarma.activa == '0':
            print('alarma inactiva')
            return 0;

        registro = AlarmaReportada(
            fecha_hora     = evento.fecha_hora_evento,
            alarma   = alarma,
            nivel_alerta = alarma.nivel_alarma,
            descripcion = evento.nombre)
        registro.save()
        if alarma.notifica == 1 or alarma.notifica == '1' or alarma.notifica == True:
            c = correo.MyCorreo()
            c.enviar_gmail(tipo_alarma=alarma.nivel_alarma,
                          destinatario=user.email,
                          activo=alarma.sensor.activo.nombre,
                          user=user,nombre_alarma=alarma.nombre)

            cls.actualizar_datos(alarma)
            
        print('ya genero alarma '+str(registro))

        return 0

    @classmethod
    def validar_alarma(cls,evento,user):
        result  = []
        print('entra a validar alarma '+str(evento.sensor))

        alarms = MyAlarm.objects.all().filter(sensor__id = evento.sensor.id)
        for alarma in alarms:
            tipo_alarma = int(alarma.sensor.tipo_sensor.id)


            if tipo_alarma == 1:
                print('id alarma humo '+ str(alarma.sensor.tipo_sensor.id))
                cls.genera_alarma(alarma,evento,user)
            elif tipo_alarma == 2:
                alarma_estado = AlarmaEstado.objects.get(pk = alarma.id)
                ret = cls.valida_horarios(alarma=alarma,alarma_estado=alarma_estado,evento=evento)
                if ret == True and (int(evento.codigo) == int(alarma_estado.estado_sensor)):
                        cls.genera_alarma(alarma,evento,user)

            elif tipo_alarma == 3:
                print('id alarma ingreso '+ str(alarma.sensor.tipo_sensor.id))
                alarma_acceso = AlarmaAcceso.objects.get(pk = alarma.id)
                ret =  cls.valida_horarios(alarma=alarma,alarma_estado=alarma_acceso,evento=evento)
                if ret == True :
                        cls.genera_alarma(alarma,evento,user)
            elif tipo_alarma == 4:
                print('id alarma estado '+ str(alarma.sensor.tipo_sensor.id))
                alarma_estado = AlarmaEstado.objects.get(pk = alarma.id)
                ret = cls.valida_horarios(alarma=alarma,alarma_estado=alarma_estado,evento=evento)
                if ret == True and (int(evento.codigo) == int(alarma_estado.estado_sensor)):
                    print('id alarma estado '+ str(evento.codigo)+'--'+str(alarma_estado.estado_sensor))
                    cls.genera_alarma(alarma,evento,user)

                print('alarma '+ str(alarma))
                print('id alarma '+ str(alarma.sensor.tipo_sensor.id))
        
        return result

    #metodo que verifica el estado de la notificacion si ya fue leida o no
    @staticmethod
    def hay_nuevas_notificaciones(user_id):

        num_alarma = AlarmaReportada.objects.all().filter(
                    alarma__sensor__activo__user_id=user_id)

        if num_alarma.__len__() > 0:
            num_alarma = AlarmaReportada.objects.all().filter(
                    alarma__sensor__activo__user_id=user_id,
                    leida=0)
            if num_alarma.__len__() > 0:
                res = True
            else:
                res = False
        else:
            res = False
        return res

    #Método que obtiene el numero de Notificaciones No leidas de ese usuario
    @staticmethod
    def contar_nuevas_notificaciones(user_id):
        num_alarma = AlarmaReportada.objects.all().filter(
                    alarma__sensor__activo__user_id=user_id,
                    leida=0)

        if num_alarma.__len__() > 0:
            res = num_alarma.__len__()
        else:
            res = 0
        return res
