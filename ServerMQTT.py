# -*- coding: cp1252 -*-
import paho.mqtt.client as mqtt
from struct import unpack
from time import sleep
import numpy as np
 
#config topic
TOPIC = "/teste/#"
 
# função chamada quando a conexão for realizada, sendo
# então realizada a subscrição
def on_connect(client, data, rc,properties=None):
    client.subscribe([(TOPIC,0)])
 
# função chamada quando uma nova mensagem do tópico é gerada
def on_message(client, userdata, msg):
    # decodificando o valor recebido
    # v = unpack(">H",msg.payload)[0]
    v = msg.payload.decode("utf-8")
    v = np.fromstring(v, dtype=np.float, sep=' ')
    print(v, type(v))
 
# clia um cliente para supervisã0
client = mqtt.Client(client_id = 'SCADA',
                     protocol = mqtt.MQTTv31)

client.username_pw_set(username = "MonitorPotencia", password = "332451")
# estabelece as funçõe de conexão e mensagens
client.on_connect = on_connect
client.on_message = on_message
 
# conecta no broker
client.connect("192.168.100.117", 1883)
 
# permace em loop, recebendo mensagens
client.loop_forever()
