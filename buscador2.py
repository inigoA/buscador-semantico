import json 
from busca_nivel2 import *
import numpy as np
from topicsclient import *
class Buscador:
	
  def buscador_semantico2(self,cadena):
    with open('final3.json','rU') as  data_file:
      data=json.load(data_file)
    p=cadena.split(" ")    
    textA=textAlytics()
    html_script="<script src=\"//cdn.embedly.com/widgets/platform.js\"></script>"
    #e,r,t=analizador(cadena)
    response_text=textA.sendPost(cadena)
    datos = response_text.read()
    r = json.loads(datos)
    pal=[]
    result=[]
    res=[]
    noticias=[]
    for j in range(len(p)):
      if (len(p[j])>3):
        pal.append(p[j])
    factor=1.0/(len(r['entity_list'])+len(pal))
    for j in range(len(data)):
      aux=[]
      for k in range(len(data[j]["entidades"])):
        for i in range(len(r['entity_list'])):
          if (data[j]["entidades"][k].find(r['entity_list'][i]['form'].lower())!=-1):
            if (self.encuentra(data[j]["entidades"][k], data[j]["entidades"][k].find(r['entity_list'][i]['form'].lower()),len(r['entity_list'][i]['form']))==1):
              aux.append(factor)
        for i in range(len(pal)):
          if (data[j]["entidades"][k].find(pal[i].lower())!=-1):
            if (self.encuentra(data[j]["entidades"][k], data[j]["entidades"][k].find(pal[i].lower()),len(pal[i]))==1):
              aux.append(factor)
		  
      for k in range(len(data[j]["keywords"])):
        for i in range(len(r['entity_list'])):
          if (data[j]["keywords"][k].find(r['entity_list'][i]['form'].lower())!=-1):
            if (self.encuentra(data[j]["keywords"][k], data[j]["keywords"][k].find(r['entity_list'][i]['form'].lower()),len(r['entity_list'][i]['form']))==1):
              aux.append(factor)

        for i in range(len(pal)):
          if (data[j]["keywords"][k].find(pal[i].lower())!=-1):
            if (self.encuentra(data[j]["keywords"][k], data[j]["keywords"][k].find(pal[i].lower()),len(pal[i]))==1):
              aux.append(factor)

      for i in range(len(r['entity_list'])):
        if (data[j]["seccion"].find(r['entity_list'][i]['form'].lower())!=-1):
          if (self.encuentra(data[j]["seccion"], data[j]["seccion"].find(r['entity_list'][i]['form'].lower()),len(r['entity_list'][i]['form']))==1):
            aux.append(factor)

      for i in range(len(pal)):
        if (data[j]["seccion"].find(pal[i].lower())!=-1):
          if (self.encuentra(data[j]["seccion"], data[j]["seccion"].find(pal[i].lower()),len(pal[i]))==1):
            aux.append(factor)
      result.append(aux)
      noticias.append("")

    for i in range(len(result)):
      res.append([sum(result[i]),i])
    cont=0
    res1=np.ones((len(res),1),dtype=np.int)
    #val=np.ones((len(res),1),dtype=np.int)
    val=[]
    res.sort()
    res=sorted(res, reverse=True)
    for i in range(len(res)):
      
      if res[i][0]>0:
        val.append(res[i][1])
        
    
    busca=Buscador_nivel2()
    res=busca.buscador_nivel2(data,val,factor,res)
    for i in range(len(res)):
      res1[res[i][1]]=i
    for i in range(len(data)):
      if (res[res1[i]][0]!=0):
        htmlcard="<a class=\"embedly-card\" href=\""+data[i]["url"]+"\">prueba<a/>\n"
        htmlcard=htmlcard+html_script
        noticias[res1[i]]=htmlcard
        cont+=1
    if cont>30:
      noti=noticias[:30]
    else:
      noti=noticias[:cont]
    return noti

  def encuentra(self,cadena,pos,tam):
    if (len(cadena)<pos+tam+1):
      return 1
    else:
      if cadena[pos+tam]==" ":
        return 1
      else:
        return 0
