import paho.mqtt.client as mqtt
from struct import pack
from random import uniform
from time import sleep
 
userid = 1
 
# Topicos a serem publicados
V = "sensor/1"
I = "sensor/2"

# cria um identificador baseado no id do sensor
client = mqtt.Client(client_id = "Client %d" % (userid), protocol = mqtt.MQTTv31)

#seta senha e usuario
client.username_pw_set(username = "Monitor", password = "332451")

# conecta no broker
client.connect("192.168.100.117", 1883)
 
while True:
    # gera um valor de tensão e corrente aleatórios
    v = round(uniform(216,224),3)
    i = round(uniform(1,5),3)

    #monta os pacotes a serem enviados
    payload = f"{v}"
    payload2 = f"{i}"
    
    # envia a publicação
    client.publish(V,payload,qos=0)
    client.publish(I, payload2,qos=0)
    print(f"{V} : payload\t {I} : payload2")
    
    sleep(0.1)
