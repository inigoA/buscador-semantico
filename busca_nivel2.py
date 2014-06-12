import json 
import numpy as np
class Buscador_nivel2:
  def buscador_nivel2(self,data,val,fact,res):
    for i in val:
      factor=fact/(len(data[i]["entidades"])+len(data[i]["keywords"]))
      for j in range(len(data)):
        if (i!=j):
          for k in range(len(data[i]["entidades"])):
            for l in range(len(data[j]["entidades"])):
              if (data[i]["entidades"][k].find(data[j]["entidades"][l])!=-1):
                if (self.encuentra(data[i]["entidades"][k], data[i]["entidades"][k].find(data[j]["entidades"][l]),len(data[j]["entidades"][l]))==1):
                  res[j][0]+=factor
            for l in range(len(data[j]["keywords"])):
              if (data[i]["entidades"][k].find(data[j]["keywords"][l])!=-1):
                if (self.encuentra(data[i]["entidades"][k], data[i]["entidades"][k].find(data[j]["keywords"][l]),len(data[j]["keywords"][l]))==1):
                  res[j][0]+=factor

          for k in range(len(data[i]["keywords"])):
            for l in range(len(data[j]["entidades"])):
              if (data[i]["keywords"][k].find(data[j]["entidades"][l])!=-1):
                if (self.encuentra(data[i]["keywords"][k], data[i]["keywords"][k].find(data[j]["entidades"][l]),len(data[j]["entidades"][l]))==1):
                  res[j][0]+=factor
            for l in range(len(data[j]["keywords"])):
              if (data[i]["keywords"][k].find(data[j]["keywords"][l])!=-1):
                if (self.encuentra(data[i]["keywords"][k], data[i]["keywords"][k].find(data[j]["keywords"][l]),len(data[j]["keywords"][l]))==1):
                  res[j][0]+=factor

    res.sort()
    res=sorted(res, reverse=True)
    return res

  def encuentra(self,cadena,pos,tam):
    if (len(cadena)<pos+tam+1):
      return 1
    else:
      if cadena[pos+tam]==" ":
        return 1
      else:
        return 0

