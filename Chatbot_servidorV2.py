
# coding: utf-8

# In[1]:


import json
import pika
import uuid
import pybars
import requests

nameVar="vacio"
dataVar="vacio"
r={}


# In[2]:


with open('robotejemploECOBICI_InpDin.json') as json_data:
    d = json.load(json_data)
    #print(d)
    data=json.dumps(d)
    Robot=json.loads(data)  


# In[3]:


def mensInf(state, entities):
    n=  {"Respuesta": [{"content":" ","next_id":" ", "blockType":" ", "contentType":" ",
                         "typingTime":" ","payload":[]}]}
    data_string = json.dumps(n)
    decoded = json.loads(data_string)

    decoded["Respuesta"][0]["content"] = str(Robot[state]["content"])
    decoded["Respuesta"][0]["next_id"] = str(Robot[state]["next_id"])
    decoded["Respuesta"][0]["blockType"]= str(Robot[state]["blockType"])
    decoded["Respuesta"][0]["contentType"]= str(Robot[state]["contentType"])
    decoded["Respuesta"][0]["typingTime"]= str(Robot[state]["typingTime"])
    payload={"content":"","state":state, "entities":entities}
    pay=json.dumps(payload)
    decoded["Respuesta"][0]["payload"].append(json.loads(pay))
    return decoded


# In[4]:


def mensQr(state, entities):
    n=  {"Respuesta": [{"content":" ","next_id":" ", "blockType":" ", "contentType":" ",
                         "typingTime":" ","payload":[]}]}
    data_string = json.dumps(n)
    decoded = json.loads(data_string)

    decoded["Respuesta"][0]["content"] = str(Robot[state]["content"])
    decoded["Respuesta"][0]["options"] = list(Robot[state]["options"])
    decoded["Respuesta"][0]["next_id"] = str(Robot[state]["next_id"])
    decoded["Respuesta"][0]["blockType"]= str(Robot[state]["blockType"])
    decoded["Respuesta"][0]["typingTime"]= str(Robot[state]["typingTime"])
    payload={"content":"","state":state, "entities":entities}
    pay=json.dumps(payload)
    decoded["Respuesta"][0]["payload"].append(json.loads(pay))
    return decoded


# In[5]:


def mensInp(state, entities):
    n=  {"Respuesta": [{"content":" ","next_id":" ", "blockType":" ", "contentType":" ",
                         "typingTime":" ","payload":[]}]}
    data_string = json.dumps(n)
    decoded = json.loads(data_string)

    decoded["Respuesta"][0]["content"] = str(Robot[state]["content"])
    decoded["Respuesta"][0]["next_id"]= str(Robot[state]["next_id"])
    decoded["Respuesta"][0]["blockType"]= str(Robot[state]["blockType"])
    decoded["Respuesta"][0]["contentType"]= str(Robot[state]["contentType"])
    decoded["Respuesta"][0]["typingTime"]= str(Robot[state]["typingTime"])
    decoded["Respuesta"][0]["validacion"]= str(Robot[state]["validacion"])
    decoded["Respuesta"][0]["Default_id"]= str(Robot[state]["Default_id"])
    decoded["Respuesta"][0]["save_var"]= str(Robot[state]["save_var"])
    payload={"content":"","state":state, "entities":entities}
    pay=json.dumps(payload)
    decoded["Respuesta"][0]["payload"].append(json.loads(pay))
    return decoded


# In[6]:


def mensInpDin(state, entities):
    n=  {"Respuesta": [{"content":" ","next_id":" ", "blockType":" ", "contentType":" ",
                         "typingTime":" ","payload":[]}]}
    output=ingresarVar(Robot[state]["content"], Robot[state]["save_var"]["nameVar"])
    data_string = json.dumps(n)
    decoded = json.loads(data_string)   

    decoded["Respuesta"][0]["content"] = output
    decoded["Respuesta"][0]["next_id"]= str(Robot[state]["next_id"])
    decoded["Respuesta"][0]["blockType"]= str(Robot[state]["blockType"])
    decoded["Respuesta"][0]["contentType"]= str(Robot[state]["contentType"])
    decoded["Respuesta"][0]["typingTime"]= str(Robot[state]["typingTime"])
    decoded["Respuesta"][0]["validacion"]= str(Robot[state]["validacion"])
    decoded["Respuesta"][0]["Default_id"]= str(Robot[state]["Default_id"])
    decoded["Respuesta"][0]["save_var"]= list(Robot[state]["save_var"])
    payload={"content":"","state":state, "entities":entities}
    pay=json.dumps(payload)
    decoded["Respuesta"][0]["payload"].append(json.loads(pay))
    print(decoded)
    return decoded


# In[7]:


def mensInfDin(state, entities): 
    global nameVar
    global dataVar
    
    n=  {"Respuesta": [{"content":" ","next_id":" ", "blockType":" ", "contentType":" ",
                         "typingTime":" ","payload":[]}]}
   
    content=""
    consultarAPIs(Robot[state]["links"], Robot[state]["credenciales"], Robot[state]["content"], nameVar, dataVar)
    if(Robot[state]["content"]!=""):
        output=ingresarVar(Robot[state]["content"], Robot[state]["save_var"]["nameVar"])
        content=crearRespuesta(output, nameVar, dataVar)
    data_string = json.dumps(n)
    decoded = json.loads(data_string)

    decoded["Respuesta"][0]["content"] = content
    decoded["Respuesta"][0]["links"] = list(Robot[state]["links"])
    decoded["Respuesta"][0]["credenciales"] = list(Robot[state]["credenciales"])
    decoded["Respuesta"][0]["next_id"] = str(Robot[state]["next_id"])
    decoded["Respuesta"][0]["blockType"]= str(Robot[state]["blockType"])
    decoded["Respuesta"][0]["contentType"]= str(Robot[state]["contentType"])
    decoded["Respuesta"][0]["typingTime"]= str(Robot[state]["typingTime"])
    decoded["Respuesta"][0]["save_var"]= list(Robot[state]["save_var"])
    payload={"content":"","state":state, "entities":entities}
    pay=json.dumps(payload)
    decoded["Respuesta"][0]["payload"].append(json.loads(pay))
    nameVar="vacio"
    dataVar="vacio"
    print(decoded)
    return decoded


# In[8]:


def mensQRDin(state, entities):
    n=  {"Respuesta": [{"content":" ","next_id":" ", "blockType":" ", "contentType":" ",
                         "typingTime":" ","payload":[]}]}
    
    ata_string = json.dumps(n)
    decoded = json.loads(data_string)

    decoded["Respuesta"][0]["content"] = str(Robot[state]["content"])
    decoded["Respuesta"][0]["options"] = list(Robot[state]["options"])
    decoded["Respuesta"][0]["next_id"] = str(Robot[state]["next_id"])
    decoded["Respuesta"][0]["blockType"]= str(Robot[state]["blockType"])
    decoded["Respuesta"][0]["typingTime"]= str(Robot[state]["typingTime"])
    payload={"content":"","state":state, "entities": entities}
    pay=json.dumps(payload)
    decoded["Respuesta"][0]["payload"].append(json.loads(pay))
    return decoded   


# In[9]:


def ingresarVar(content,nameVariable):
    
    global r
    global nameVar
    prueba1={}
    prueba2={}
    principal=""
    re=r.json()
    
    if(len(re)>1):
        print("RE[0]")
    else:
        for raiz in re:
            key=raiz
            for i in re[key][0]:
                principal=i
                break
        output=completarURL(content, prueba1, prueba2, nameVariable, principal)
        nameVar=principal
    
    return output


# In[10]:


def consultarAPIs(links, tockens, content, nameVar, dataVar):
    global r
    re={}
    prueba1={}
    prueba2={}
    if(len(links)>0): 
        for link in links:        
            urlF=completarURL(links[link], tockens, re, nameVar, dataVar)           
            r = requests.get(urlF)
            print(urlF)
            re=r.json() 


# In[11]:


def crearRespuesta(content, nameVar, dataVar):
    
    global r
    re=r.json()
    if(len(re)>1):
        source = content
        compiler = pybars.Compiler()
        template = compiler.compile(source)
        output = template(r.json())    
    else:
        for raiz in re:
            key=raiz
        general=r.json()[key]
        posicion=buscarDatos(general, nameVar, dataVar)        
        print("CONTENT= ", content) 
        if(content[len(content)-1]=='+'):
            content=content[:len(content)-1]
            for elemento in r.json()[key][posicion]:
                content+=elemento+" {{"+elemento+"}}, "
        source = content
        compiler = pybars.Compiler()
        template = compiler.compile(source)
        output = template(r.json()[key][posicion]) 
        
    return output


# In[12]:


def completarURL(url, tockens, consulta, nameVar, dataVar):
    print("urlInicio=  ", url, "tockens=   ", tockens, "consulta=  ", consulta, "nameVar=  ", nameVar, "dataVar=  ", dataVar)
    pos1=1
    pos2=0
    posAux=0
    c1=0
    c2=0
    cadAux=url
    while(pos1>-1):  
        if(posAux<len(url)):
            pos1=cadAux.find('{')
            if(url[posAux+pos1+1]=='{' and pos1>-1):
                pos2=cadAux.find('}')  
                cadAux=url[pos2+posAux+2:]
                if(nameVar.lower()==url[posAux+pos1+2:pos2+posAux].lower()):
                    res=len(dataVar)-len(nameVar)
                    url=url[:posAux+pos1+2]+dataVar+url[pos2+posAux:]
                    posAux=pos1+posAux+res+2
                else:
                    posAux=pos2+posAux+2
            elif(pos1>-1):
                pos2=cadAux.find('}')
                cadAux=url[pos2+posAux+1:]
                for credencial in tockens:            
                    if(credencial.lower()==url[pos1+posAux+1:pos2+posAux].lower()):
                        url=url[:pos1+posAux]+tockens[credencial]+url[pos2+1+posAux:]
                        cadAux=url[pos1+posAux:]
                        posAux=pos1+posAux
                        c1=1
                        break
                    else:
                        c1=0
                for datos in consulta:
                    if(datos.lower()==url[pos1+posAux+1:pos2+posAux].lower()):
                        url=url[:pos1+posAux]+consulta[datos]+url[pos2+1+posAux:]
                        cadAux=url[pos1+posAux:]
                        posAux=pos1+posAux
                        c2=1
                        break
                    else:
                        c2=0
                if(nameVar.lower()==url[pos1+posAux+1:pos2+posAux].lower()):
                    url=url[:pos1+posAux]+dataVar+url[pos2+1+posAux:]
                    cadAux=url[pos1+posAux:]
                    posAux=pos1+posAux
                elif(c1==0 and c2==0):
                    posAux=pos2+posAux+1
        else:
            pos1=-1
        
    return url


# In[13]:


def buscarDatos(general, nameVar, dataVar): 
    cont=0    
    #print("Entrando al no se que ")
    if nameVar in 'vacio' or nameVar in 'vacio':
        print("vacio")
    else:
        for dato in general:        
            if(type(dato[nameVar])==int):
                dataVar=int(dataVar)
            if(dato[nameVar]==dataVar):
                break       
            cont+=1
    return cont
        


# In[14]:


def envia(ch,props, method, data_string):    
    
    ch.basic_publish(exchange='',
                 routing_key=props.reply_to,
                 properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                 body=str(data_string))
    ch.basic_ack(delivery_tag = method.delivery_tag)
    
    


# In[15]:


def confirma(ch,props, method, state, entities):
    cont=1        
    print("Siguiente estado...", state)    
    if(Robot[state]["blockType"]=="informativo"):
        if(state=="Salida"):
            print("Terminando conversación...")
            cont=-100
        resp=mensInf(state, entities)
        data_string = json.dumps(resp)        

    elif(Robot[state]["blockType"]=="quickReply"):
        resp=mensQr(state, entities)
        data_string = json.dumps(resp)
    
    elif(Robot[state]["blockType"]=="input"):
        resp=mensInp(state, entities)
        data_string = json.dumps(resp)
        
    elif(Robot[state]["blockType"]=="informativoDinamico"):
        resp=mensInfDin(state, entities)
        data_string = json.dumps(resp)
        
    elif(Robot[state]["blockType"]=="inputDinamico"):
        resp=mensInpDin(state, entities)
        data_string = json.dumps(resp)
    
    print(" [x] Enviando... ", str(data_string))
    #mensaje=
    envia(ch,props, method, data_string)
    #print("llegó esto: ",mensaje["payload"])
    return cont #,mensaje;


# In[16]:


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='chatbotV3')



def on_request(ch, method, props, body):
    global nameVar
    global dataVar
    mensaje= json.loads(body)
    print(mensaje)
    
    if(mensaje["payload"][0]["state"]=='none' ):
        #print("Entrando al caso 1 :(")
        #print(mensaje)
        n=  {"Respuesta": [{"content":" ","next_id":" ", "blockType":" ", "contentType":" ",
                         "typingTime":" ","payload":[]}]}
        data_string = json.dumps(n)
        decoded = json.loads(data_string)

        decoded["Respuesta"][0]["content"] = str(Robot["Saludo"]["content"])
        decoded["Respuesta"][0]["next_id"] = str(Robot["Saludo"]["next_id"])
        decoded["Respuesta"][0]["blockType"]= str(Robot["Saludo"]["blockType"])
        decoded["Respuesta"][0]["contentType"]= str(Robot["Saludo"]["contentType"])
        decoded["Respuesta"][0]["typingTime"]= str(Robot["Saludo"]["typingTime"])
        payload={"content":"","state":"Saludo", "entities":[]}
        pay=json.dumps(payload)
        decoded["Respuesta"][0]["payload"].append(json.loads(pay))
        data_string = json.dumps(decoded)

        print(" [x] Enviando... ", str(data_string))

        envia(ch, props, method,data_string)
    else:
        
        if(Robot[mensaje["payload"][0]["state"]]["blockType"]=="informativo"):
            state=str(Robot[mensaje["payload"][0]["state"]]["next_id"])
            entities= mensaje["payload"][0]["entities"]
            cont=confirma(ch,props, method, state, entities)


        elif(Robot[mensaje["payload"][0]["state"]]["blockType"]=="quickReply"):
            if(mensaje["payload"][0]["content"] in Robot[mensaje["payload"][0]["state"]]["options"]):
                state=str(Robot[mensaje["payload"][0]["state"]]["next_id"][mensaje["payload"][0]["content"]])
                entities= mensaje["payload"][0]["entities"]
            else:
                state=str(Robot[mensaje["payload"][0]["state"]]["Default_id"])
                entities= mensaje["payload"][0]["entities"]

            cont=confirma(ch,props, method, state, entities)

        elif(Robot[mensaje["payload"][0]["state"]]["blockType"]=="input"):
            dataVar=mensaje["payload"][0]["content"]
            nameVar=Robot[mensaje["payload"][0]["state"]]["save_var"]["nameVar"]
            state=str(Robot[mensaje["payload"][0]["state"]]["next_id"])
            entities= mensaje["payload"][0]["entities"]
            cont=confirma(ch,props, method, state, entities)   
            
        elif(Robot[mensaje["payload"][0]["state"]]["blockType"]=="informativoDinamico"):   
            state=str(Robot[mensaje["payload"][0]["state"]]["next_id"])
            entities= mensaje["payload"][0]["entities"]
            cont=confirma(ch,props, method, state,entities)
        
        elif(Robot[mensaje["payload"][0]["state"]]["blockType"]=="inputDinamico"):
            dataVar=mensaje["payload"][0]["content"]
            nameVar=Robot[mensaje["payload"][0]["state"]]["save_var"]["nameVar"]
            state=str(Robot[mensaje["payload"][0]["state"]]["next_id"])
            entities= mensaje["payload"][0]["entities"]
            cont=confirma(ch,props, method, state,entities)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='chatbotV3')

print(" [x] Comenzando conversación...")
channel.start_consuming()
