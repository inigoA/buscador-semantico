#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from buscador2 import Buscador
#import web
import cyclone.web
import sys
#import cyclone.escape
#import cyclone.websocket
from twisted.internet import reactor
from twisted.python import log
#from twisted.web import server, resource
import json
from crea3 import Creador
import requests
from datetime import *
#from datetime import datetime
import time
listaNoticias=[]
class MainHandler (cyclone.web.RequestHandler):
    
    def get (self):
        
        self.render("prueba.html",noticias=[],error="",titulo="DNow")
    
    def post (self):
      #realizar la busqueda
      
      if self.get_argument('busqueda',''):
        aux=self.get_argument('buscado','')
        global listaNoticias
        
        if len(aux)==0:
          if len(listaNoticias)<30:
            self.render("prueba.html",noticias=listaNoticias,error="No hay criterio de busqueda", titulo="Error")
          else:
            self.render("prueba.html",noticias=listaNoticias[:30],error="No hay criterio de busqueda", titulo="Error")
        else:
          busca = Buscador()
          a=busca.buscador_semantico2(aux)
          if len(a)==0:
            if len(listaNoticias)<30:
              self.render("prueba.html",noticias=listaNoticias,error="No hay noticias relacionadas", titulo="Error")
            else:
              self.render("prueba.html",noticias=listaNoticias[:30],error="No hay noticias relacionadas", titulo="Error")
          else: 
            
            listaNoticias=a+listaNoticias
            if len(listaNoticias)<30:
              self.render("prueba.html",noticias=listaNoticias,error="", titulo=aux)
            else:
              self.render("prueba.html",noticias=listaNoticias[:30],error="", titulo=aux)
      elif self.get_argument('limpiar',''):
        listaNoticias=[]
        self.render("prueba.html",noticias=listaNoticias,error="Búsquedas limpiadas", titulo="DNow")
      elif self.get_argument('actualizar',''):

        if os.path.exists('ultima_actualizacion.txt'):
          actualiza=open('ultima_actualizacion.txt','r')
          actu=actualiza.readline()
          d=date.today()
          #dt=datetime.combine(d,datetime.min.time())
          fecha_act=time.mktime(d.timetuple())
          #fecha_act=datetime.combine(d,datetime.min.time())
          
          peticion="http://www.diariodenavarra.es/movil.php?query=tipo:noticia&fechaTimeStamps%20BETWEEN%20"+actu+"%20AND%20"+str(fecha_act)
          r=requests.get(peticion)  

          r= r.text.encode('UTF-8')
          with open('nuevas.json','w') as outfich:
            outfich.write(r)
          creador= Creador()
          creador.crea_archivo_completo3()
          with open('ultima_actualizacion.txt','w') as outfich:
            outfich.write(str(fecha_act))
          if len(listaNoticias)<30:
            self.render("prueba.html",noticias=listaNoticias,error="Noticias actualizadas", titulo="Actualizado")
          else:
            self.render("prueba.html",noticias=listaNoticias[:30],error="Noticias actualizadas", titulo="Actualizado")
      else:
        self.render("prueba.html",noticias=[],error="Error")

if __name__ == "__main__":
    #sys.exit(main(sys.argv))
    #cache=cardCache()
    
    settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        autoescape=None
        )
    application = cyclone.web.Application([
        (r"/", MainHandler)
        #(r"/realtime", RealTimeSocketHandler,dict(cache=cache))
    ],**settings)
    log.startLogging(sys.stdout)
    reactor.listenTCP(8888, application, interface="127.0.0.1")
    reactor.run()
