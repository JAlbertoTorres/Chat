
# coding: utf-8

# In[ ]:


import json
import pika
import uuid


# In[ ]:


def conv(msj):
    #print(msj)
    contenido=msj["Respuesta"][0]["content"]
    estado=msj["Respuesta"][0]["payload"][0]["state"]
    entidad= msj["Respuesta"][0]["payload"][0]["entities"]
    tipo= msj["Respuesta"][0]["blockType"]
    print(str(contenido))
    #print(estado)
   
    if(tipo=="quickReply"):
        print("Elija una de las siguientes opciones...\n")
        for op in msj["Respuesta"][0]["options"]:
            print(op)
        ans= input()
        return entidad, ans, estado
    elif(tipo=="input"):
        ans= input()
        return entidad, ans, estado
    elif(tipo=="informativo"):
        return entidad, str('next'), estado
    else:
        return entidad, str('hey'), estado
    
class conversacion(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
            
    def call(self):
        cont=0
        #data_string = json.loads(body)
        #print(data_string)
        #print(n)
        #print(" [.] fib(%s)" % n)
        #while (not ("adios") in n):
        while(cont>=0):
            if cont==0:
                entidad={}
                resp="hi"
                estado = "none"
            
            

            n=  {"payload": [{"content":" ","state":" ", "entitites":" "}]}

            data=json.dumps(n)
            decoded=json.loads(data)

            decoded["payload"][0]["content"]=resp
            decoded["payload"][0]["state"]=estado
            decoded["payload"][0]["entities"]= entidad

            data_string=json.dumps(decoded)

            self.response = None
            self.corr_id = str(uuid.uuid4())
            self.channel.basic_publish(exchange='',
                                       routing_key='chatbotV2',
                                       properties=pika.BasicProperties(
                                             reply_to = self.callback_queue,
                                             correlation_id = self.corr_id,
                                             ),
                                       body=str(data_string))
            while self.response is None:
                                    self.connection.process_data_events()
            data = json.loads(self.response)
            entidad, resp, estado= conv(data)
            #print("LLego esto: ", data)
            if(data["Respuesta"][0]["payload"][0]["state"]=="Salida"):
                cont=-1
            else:
                cont+=1

  
chat = conversacion()


response = chat.call()
print(" [.] Got %r", response)   

