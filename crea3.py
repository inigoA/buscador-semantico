#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import json
import os.path
import httplib
import urllib
from topicsclient import *
class Creador:
  def crea_archivo_completo3(self):
    if os.path.exists('final3.json'):
      final=open('final3.json','rU')
      arch=final.readline()
      arch1=arch[:len(arch)-3]
      arc_fin=arch1+','
      final.close()
    else:
      arc_fin='[ '
		
    arc_fin=arc_fin.decode('UTF-8')
    with open('nuevas.json','rU') as  data_file:
      data=json.load(data_file)
		 
    j=0
    textA=textAlytics()
    for j in range(len(data["response"]["docs"])-1):
      if len(data["response"]["docs"][j]["texto"])>1:
        response_text=textA.sendPost(data["response"]["docs"][j]["texto"].encode('UTF-8'))
        datos = response_text.read()
        r = json.loads(datos)
        arc_fin+='{"url":"'+data["response"]["docs"][j]["link"]+'", '
        arc_fin+='"titulo":"'+self.comprueba(data["response"]["docs"][j]["titulo"]) +'", '
        arc_fin+='"fecha":'+str(data["response"]["docs"][j]["fechaTimestamp"]) +', '
        arc_fin+='"keywords":['
        if data["response"]["docs"][j]["taxonomias"][0]=='sin_taxonomia':
          arc_fin+='], '
        else:
          for k  in range(len(data["response"]["docs"][j]["taxonomiasName"])-2):
            arc_fin+='"'+data["response"]["docs"][j]["taxonomiasName"][k].lower()+'",'
          arc_fin+='"'+data["response"]["docs"][j]["taxonomiasName"][len(data["response"]["docs"][j]["taxonomiasName"])-1].lower() +'"], '
		      
        arc_fin+='"seccion":"'+data["response"]["docs"][j]["categoriaNombre"].lower() +'", '
        entities=[]
        arc_fin+='"entidades":['
        if len(r['entity_list']) > 0:
          entities = r['entity_list']
          for index in range(len(entities)-2):
            arc_fin += '"'+ entities[index]['form'].lower()+'", '
          arc_fin+='"'+entities[len(entities)-1]['form'].lower()+'"] '
        else:
          arc_fin+=']'
        arc_fin+='}, '
	  
    j=len(data)-1
    if len(data["response"]["docs"][j]["texto"])>1:
      response_text=textA.sendPost(data["response"]["docs"][j]["texto"].encode('UTF-8'))
      datos = response_text.read()
      r = json.loads(datos)
      arc_fin+='{"url":"'+data["response"]["docs"][j]["link"]+'", '
      arc_fin+='"titulo":"'+self.comprueba(data["response"]["docs"][j]["titulo"]) +'", '
      arc_fin+='"fecha":'+str(data["response"]["docs"][j]["fechaTimestamp"]) +', '
      arc_fin+='"keywords":['
      if data["response"]["docs"][j]["taxonomiasName"][0]=='Sin Taxonomía':
        arc_fin+='], '
      else:
        for k  in range(len(data["response"]["docs"][j]["taxonomiasName"])-2):
          arc_fin+='"'+data["response"]["docs"][j]["taxonomiasName"][k].lower()+'",'
        arc_fin+='"'+data["response"]["docs"][j]["taxonomiasName"][len(data["response"]["docs"][j]["taxonomiasName"])-1].lower() +'"], '
      arc_fin+='"seccion":"'+data["response"]["docs"][j]["categoriaNombre"].lower() +'", '
      arc_fin+='"entidades":['
      if len(r['entity_list']) > 0:
        entities = r['entity_list']
        for index in range(len(entities)-2):
          arc_fin += '"'+ entities[index]['form']+'", '
        arc_fin+='"'+entities[len(entities)-1]['form']+'"] '
      else:
        arc_fin+=']'
      arc_fin+='}  '
    else:
      arc_fin=arc_fin[len(arc_fin)-2]
      arc_fin+=' ]'

		
    arc= arc_fin.encode('UTF-8')
    with open('final3.json','w') as outfich:
      outfich.write(arc)
    return arc_fin


  def comprueba(self,r):
    if r.find('"')!=-1:
      r=r[:r.find('"')]+r[r.find('"')+1:]
      r=self.comprueba(r)
    return r
