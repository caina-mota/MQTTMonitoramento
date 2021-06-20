# Biblioteca utilizada para publicar e ler

PAHO MQTT for Python
https://pypi.org/project/paho-mqtt/

#Broker instalado
Mosquitto


## criando senha e usuario para o broker
// client 3324
// mqttserver 332451

`sudo mosquitto_passwd -c /etc/mosquitto/passwd <username> `
`Password: <senha>`

Depois crie um arquivo de configuração para o mosquitto e que aponte para a senha que acabamos de criar.

`sudo nano /etc/mosquitto/conf.d/default.conf`

Cole o seguinte comando no arquivo que foi criado.

```
allow_anonymous false
password_file /etc/mosquitto/passwd
```

Para terminar salve seu arquivo com o comando de teclado Ctrl+o , Enter e em seguida Ctrl+X e reinicie seu software do Mosquitto MQTT com o Comando.

`sudo systemctl restart mosquitto`


# comandos linha de comando linux

## subcriber do topico no servidor
onde escuta/recebe as mensagens enviadas pelos sensores

`mosquitto_sub -h "ip" -p 1883 -t "topicname" -u "username" -P "password"`

`-h` = hostname, o ip do broker entre aspas

`-p` = porta, para o tcp, a porta é a 1883

`-t` = nome do tópico que esta sendo subscrito

`-u` = username configurado, pode ser o nome do sensor, a fonte, quaisquer coisa

`-P` = password, a senha configurada para o username

## publicação do cliente (Sensores)
publicação das mensagens para o servidor, para quem consome a informação

`mosquitto_pub -h "ip" -p 1883 -t "topicname" -m "message" -u "username" -P "password"`

`-h` = hostname, o ip do broker entre aspas

`-p` = porta, para o tcp, a porta é a 1883

`-t` = nome do tópico que esta sendo subscrito

`-m` = mensagem a ser publicada

`-u` = username configurado, pode ser o nome do sensor, a fonte, quaisquer coisa

`-P` = password, a senha configurada para o username


## publicação pelo paho, cliente que publica / sensor
Exemplos em: 
      - `https://www.embarcados.com.br/mqtt-protocolos-para-iot/`

      - `https://www.embarcados.com.br/raspberry-pi-3-na-iot-mqtt-e-python/`


 - cria um identificador baseado no id do sensor (client_id é o identificador)
 
    `client = mqtt.Client(client_id = "Client %d" % (userid), protocol = mqtt.MQTTv31)`
 - seta o usuário e senha pra permitir a conexão
 
    `client.username_pw_set(username = "username", password = "password")`
 - inicia a conexão mqtt no broker
 
    `client.connect("hostname/ip", 1883)`

 - publicar propriamente dito (qos - quality of service - tratamento de erros e relacionados)
 
    `client.publish(topic,binarypayload,qos=0)`

## sobrescreve e pelo paho, utiliza no cliente que consome

 - cria um cliente para supervisão
 
    `client = mqtt.Client(client_id = 'SCADA', protocol = mqtt.MQTTv31)`

 - seta o usuário e senha pra permitir a conexão
 
    `client.username_pw_set(username = "username", password = "password")` 

 - estabelece as funçõe de conexão e mensagens
 ```
    # função chamada quando a conexão for realizada, sendo então realizada a subscrição
    def on_connect(client, data, rc,properties=None):
        client.subscribe([(TOPIC,0)])
    
    # função chamada quando uma nova mensagem do tópico é gerada, esta é a função que realiza o processamento das mensagens recebidas
    def on_message(client, userdata, msg):
        # decodificando o valor recebido
        v = msg.payload.decode("utf-8")
        print(v)
        
    # roda as funções
    client.on_connect = on_connect
    client.on_message = on_message
```
 - inicia a conexão mqtt no broker
 
    `client.connect("hostname/ip", 1883)`

 - permacer em loop, para receber mensagens como um servidor
 
    `client.loop_forever()`

   try:
      programa
   
   except KeyboardInterrupt:
        print "\nCtrl+C pressionado, encerrando aplicacao e saindo..."
        sys.exit(0)