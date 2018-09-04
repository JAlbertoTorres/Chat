
# coding: utf-8

# In[1]:


import json
import pika
import uuid


# In[2]:


with open('robotejemplo.json') as json_data:
    d = json.load(json_data)
    #print(d)
    data=json.dumps(d)
    Robot=json.loads(data)
    #for i in Robot.keys():
     #   print(i)
      #  print(Robot[i])    


# In[3]:


def mensInf(state):
    n=  {"Respuesta": [{"content":" ","next_id":" ", "blockType":" ", "contentType":" ",
                         "typingTime":" ","payload":[]}]}
    data_string = json.dumps(n)
    decoded = json.loads(data_string)

    decoded["Respuesta"][0]["content"] = str(Robot[state]["content"])
    decoded["Respuesta"][0]["next_id"] = str(Robot[state]["next_id"])
    decoded["Respuesta"][0]["blockType"]= str(Robot[state]["blockType"])
    decoded["Respuesta"][0]["contentType"]= str(Robot[state]["contentType"])
    decoded["Respuesta"][0]["typingTime"]= str(Robot[state]["typingTime"])
    payload={"content":"","state":state, "entities":{}}
    pay=json.dumps(payload)
    decoded["Respuesta"][0]["payload"].append(json.loads(pay))
    return decoded


# In[4]:


def mensQr(state):
    n=  {"Respuesta": [{"content":" ","next_id":" ", "blockType":" ", "contentType":" ",
                         "typingTime":" ","payload":[]}]}
    data_string = json.dumps(n)
    decoded = json.loads(data_string)

    decoded["Respuesta"][0]["content"] = str(Robot[state]["content"])
    decoded["Respuesta"][0]["options"] = list(Robot[state]["options"])
    decoded["Respuesta"][0]["next_id"] = str(Robot[state]["next_id"])
    decoded["Respuesta"][0]["blockType"]= str(Robot[state]["blockType"])
    decoded["Respuesta"][0]["typingTime"]= str(Robot[state]["typingTime"])
    payload={"content":"","state":state, "entities":{}}
    pay=json.dumps(payload)
    decoded["Respuesta"][0]["payload"].append(json.loads(pay))
    return decoded


# In[5]:


def mensInp(state):
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
    payload={"content":"","state":state, "entities":{}}
    pay=json.dumps(payload)
    decoded["Respuesta"][0]["payload"].append(json.loads(pay))
    return decoded


# In[6]:


def envia(ch,props, method, data_string):    
    
    ch.basic_publish(exchange='',
                 routing_key=props.reply_to,
                 properties=pika.BasicProperties(correlation_id = \
                                                     props.correlation_id),
                 body=str(data_string))
    ch.basic_ack(delivery_tag = method.delivery_tag)
    
    


# In[ ]:


def confirma(ch,props, method, state):
    cont=1        
    print("Siguiente estado...", state)    
    if(Robot[state]["blockType"]=="informativo"):
        if(state=="Salida"):
            print("Terminando conversación...")
            cont=-100
        resp=mensInf(state)
        data_string = json.dumps(resp)        

    elif(Robot[state]["blockType"]=="quickReply"):
        resp=mensQr(state)
        data_string = json.dumps(resp)

    else:
        resp=mensInp(state)
        data_string = json.dumps(resp)
    
    print(" [x] Enviando... ", str(data_string))
    #mensaje=
    envia(ch,props, method, data_string)
    #print("llegó esto: ",mensaje["payload"])
    return cont #,mensaje;


# In[ ]:


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='chatbotV2')

def on_request(ch, method, props, body):
    mensaje= json.loads(body)
    print(mensaje)
    
    if(mensaje["payload"][0]["state"]=='none'):
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
        payload={"content":"","state":"Saludo", "entities":{}}
        pay=json.dumps(payload)
        decoded["Respuesta"][0]["payload"].append(json.loads(pay))
        data_string = json.dumps(decoded)

        print(" [x] Enviando... ", str(data_string))

        envia(ch, props, method,data_string)
    else:
        
        if(Robot[mensaje["payload"][0]["state"]]["blockType"]=="informativo"):
            state=str(Robot[mensaje["payload"][0]["state"]]["next_id"])
            cont=confirma(ch,props, method, state)


        elif(Robot[mensaje["payload"][0]["state"]]["blockType"]=="quickReply"):
            if(mensaje["payload"][0]["content"] in Robot[mensaje["payload"][0]["state"]]["options"]):
                state=str(Robot[mensaje["payload"][0]["state"]]["next_id"][mensaje["payload"][0]["content"]])
            else:
                state=str(Robot[mensaje["payload"][0]["state"]]["Default_id"])

            cont=confirma(ch,props, method, state)

        elif(Robot[mensaje["payload"][0]["state"]]["blockType"]=="input"): 
            state=str(Robot[mensaje["payload"][0]["state"]]["next_id"])
            cont=confirma(ch,props, method, state)           


channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='chatbotV2')

print(" [x] Comenzando conversación...")
channel.start_consuming()


# In[ ]:


import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("www.google.com", 80))
s.listen(5)
conn, addr = s.accept()


# In[ ]:


import urllib
CLIENT_ID= '1350_2w3ssw2c0f40swwkgs8gccscs844wsksksow8o40sw0g4g4wo0'
CLIENT_SECRET='3a8ig9dxlm80ok4koc0w40cssgsg00ggcwkgw4oc88kgs8gcc0'

urllib.request.urlopen('https://pubsbapi.smartbike.com/oauth/v2/token?client_id=1350_2w3ssw2c0f40swwkgs8gccscs844wsksksow8o40sw0g4g4wo0&client_secret=3a8ig9dxlm80ok4koc0w40cssgsg00ggcwkgw4oc88kgs8gcc0&grant_type=client_credentials').read()


# In[ ]:


print(urllib.request.Request('http://google.com'))

