# -*- coding: cp1252 -*-
import paho.mqtt.client as mqtt
from struct import pack
from random import randint
from time import sleep
 
userid = 10
 
# topicos providos por este sensor
tt = "/teste"
 
# cria um identificador baseado no id do sensor
client = mqtt.Client(client_id = "Client %d" % (userid),
                     protocol = mqtt.MQTTv31)

#seta senha e usuario
client.username_pw_set(username = "mqttserver", password = "332451")

# conecta no broker
client.connect("192.168.100.117", 1883)
 
while True:
    # gera um valor de temperartura aleatório
    t = randint(0,50)
    # codificando o payload como big endian, 2 bytes
    payload = f"{t}"
    print(payload)
    # envia a publicação
    client.publish(tt,payload,qos=0)
    
    sleep(1)
