from os import name
import paho.mqtt.client as mqtt
import numpy as np
from PyQt5 import QtGui, QtCore
import sys
import pyqtgraph as pg

def convolutional_mean_average(signal, w):
    #Criação da máscara
    mask=np.ones((1,w))/w
    mask=mask[0,:]

    # Convolução da máscara com o sinal para gerar a média móvel
    #                            np.convolve(a, v, mode='full')
    #                            (a * v)[n] = \sum_{m = -\infty}^{\infty} a[m] v[n - m]
    convolved_data=np.convolve(signal, mask,'same')

    return convolved_data


app = pg.mkQApp()
mw = QtGui.QMainWindow()
mw.setWindowTitle('Monitoramento de potencia')
mw.resize(1600,800)
cw = QtGui.QWidget()
mw.setCentralWidget(cw)
# l = QtGui.QVBoxLayout()
l = QtGui.QGridLayout()
cw.setLayout(l)


pw = pg.PlotWidget(title = "Potência", name='Plot1')  ## giving the plots names allows us to link their axes together
l.addWidget(pw, 0,1,3,2)
pw2 = pg.PlotWidget(title = "Tensão", name='Plot2')
l.addWidget(pw2,3,1,1,1)
pw3 = pg.PlotWidget(title = "Corrente")
l.addWidget(pw3,3,2,1,1)


textedit = QtGui.QLineEdit()
textedit.setValidator(QtGui.QDoubleValidator())
l.addWidget(textedit,0,0)
enter = QtGui.QPushButton('CONFIGURAR NOVA TARIFA')
l.addWidget(enter,1,0)
textview = QtGui.QTextEdit()
textview.setReadOnly(True)
l.addWidget(textview,2,0)
topicslist = QtGui.QTextEdit()
topicslist.setReadOnly(True)
l.addWidget(topicslist,3,0,2,1)
pkv = QtGui.QPushButton('HABILITAR VISUALIZAÇÃO DE PACOTES')
l.addWidget(pkv,4,0)

mw.show()

p1 = pw.plot()
p4 = pw.plot()
# p1.setPen('w')
pw.setLabel('left', 'Potência', units='W')
pw.setLabel('bottom', 'Time', units='s')
pw.enableAutoRange(True, True)


p2 = pw2.plot()
# p2.setPen((200,200,100))
pw2.setLabel('left', 'Tensão RMS', units='V')
pw2.setLabel('bottom', 'Time', units='s')
pw2.enableAutoRange(True, True)

p3 = pw3.plot()
# p3.setPen((200,200,100))
pw3.setLabel('left', 'Corrente', units='A')
pw3.setLabel('bottom', 'Time', units='s')
pw3.enableAutoRange(True, True)

tarifa = 0.727870
v = 0
i = 0
att = -1


P = []
V = []
I = []
Pmm = []
index = []

vmed = 0
imed = 0
pmed = 0
cmed = 0
gmed = 0


def enterFun():
    global tarifa
    if len(textedit.text()) != 0:
        tarifa = round(np.float(textedit.text()),6)
        textedit.clear()

def update_consumo():
    textview.clear()
    textview.setText(f'\t-- Consumo médio atual --\n \
                        \nPotência média: \t\t {pmed} W\
                        \nTensão Média: \t\t {vmed} Vac\
                        \nCorrente Média: \t {imed} A\
                        \n\nConsumo Atual médio: \t {round(cmed,4)} kW/h\
                        \nTarifa: \t\t R$ {tarifa} kW/h\
                        \nValor a pagar /hora: \t R$ {round(gmed,3)} \
                        \n\n\t-- Estimativas /mês --\n\
                        \nValor a pagar /mês 1h/dia: \t R$ {round(gmed*30,3)} \
                        \nValor a pagar /mês 5h/dia: \t R$ {round(gmed*5*30,3)} \
                        \nValor a pagar /mês 10h/dia: \t R$ {round(gmed*10*30,3)} \
                        \nValor a pagar /mês 15h/dia: \t R$ {round(gmed*15*30,3)}')

def calcula_medias():
    global P, V, I, index
    global vmed,imed,pmed,cmed,gmed
    if index[-1] >120:
        pmed = np.mean(P[index[-120]: index[-1]]).round(3)
        vmed = np.mean(V[index[-120]: index[-1]]).round(3)
        imed = np.mean(I[index[-120]: index[-1]]).round(3)
        if (index[-1] % 60) == 0:
            cmed = np.mean(Pmm[index[-85]: index[-15]]).round(3)
            cmed = cmed/1000
            gmed = (cmed * tarifa)
    else:
        pmed = np.mean(P[: index[-1]]).round(3)
        vmed = np.mean(V[: index[-1]]).round(3)
        imed = np.mean(I[: index[-1]]).round(3)
    
    
pkvon = 0
def packetviewbt():
    global pkvon
    if pkvon == 0:
        pkvon = 1
    else:
        pkvon = 0
        topicslist.clear()

def packetview(msg1, msg2):
    m1 = np.float(msg1.payload.decode("utf-8"))
    m2 = np.float(msg2.payload.decode("utf-8"))
    topicslist.append(f"'{msg1.topic}' : {m1} \t '{msg2.topic}' : {m2} ")
    


        
        
#conecta os slots dos botões a uma função
enter.clicked.connect(enterFun)
pkv.clicked.connect(packetviewbt)

msg1 = None
msg2 = None

def update_data(msg):
    global v, i, att
    global P, V, I, Pmm, index
    global p1, p2, p3, p4
    global pw, pw2, pw3
    global pkv, msg1, msg2
    # Verificar qual o sensor que está sendo lido
    if msg.topic[-1] == "1":
        v = np.float(msg.payload.decode("utf-8"))
        msg1 = msg
        if att == 1:
            att = 0
        else:
            att = 1
        
    elif msg.topic[-1] == "2":
        i = np.float(msg.payload.decode("utf-8"))
        msg2 = msg
        if att == 0:
            att = 1
        else:
            att = 0
    
    if att == 1:
        if len(index) >0:
            index.append(index[-1]+1) 
        else:
            index.append(0)  

        V.append(v)
        I.append(i)
        P.append(v * i)
        
        t = np.array(index) * 0.15
        p1.setData(x=t, y=P, pen = ('r'))
        p2.setData(x=t, y=V, pen = ('g'))
        p3.setData(x=t, y=I, pen = "b")
        
        w = 30
        if len(P) > w:
            Pmm = convolutional_mean_average(P, w)
            p4.setData(x=t, y=Pmm, pen = ('y'))

        if index[-1] >61:
            pw.setXRange(t[-60], t[-1], padding = 1)
            pw3.setXLink('Plot1')
            pw2.setXLink('Plot1')
            

        calcula_medias()
        update_consumo()

        if pkvon==1:
            packetview(msg1, msg2)

        app.processEvents()


def mqttleitura():
    #config topic
    TOPIC = "sensor/#"

    # função chamada quando a conexão for realizada, sendo
    # então realizada a subscrição
    def on_connect(client, data, rc,properties=None):
        client.subscribe([(TOPIC,0)])

    # função chamada quando uma nova mensagem do tópico é gerada
    def on_message(client, userdata, msg):
        update_data(msg)

    # cria um cliente para supervisão
    client = mqtt.Client(client_id = 'Monitoramento', protocol = mqtt.MQTTv31)

    # faz o login no broker
    client.username_pw_set(username = "Monitor", password = "332451")

    try:
        # estabelece as funções de conexão e mensagens
        client.on_connect = on_connect
        client.on_message = on_message
        
        # conecta no broker
        client.connect("192.168.100.117", 1883)
        
        # permace em loop, recebendo mensagens
        client.loop_forever()

    except KeyboardInterrupt:
        print("Fechando aplicação")
        sys.exit(0)




if __name__== "__main__":
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        mqttleitura()
        QtGui.QApplication.instance().exec_()
        