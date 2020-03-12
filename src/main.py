import machine
import time

from machine import Pin

################# variaveis globais ########################
atuador_sole1 = Pin(19, Pin.OUT) 
atuador_sole2 = Pin(18, Pin.OUT)
umidade = 4050 # input do usuario
pino_sensor1 = Pin(34, Pin.IN) 
pino_sensor2 = Pin(35, Pin.IN)
############################################################


# retorna o valor do sensor 
def retorna_valores_sensores():
    adc1 = machine.ADC(pino_sensor1) 
    adc1 = adc1.read()
    adc2 = machine.ADC(pino_sensor2)
    adc2 = adc2.read()
    return (adc1, adc2)


atuador_sole1.value(0)

while True:
    valor_sensor = retorna_valores_sensores()
    
    if valor_sensor[0] >= umidade:
        atuador_sole1.value(1)
    else:
      atuador_sole1.value(0)
    if valor_sensor[1] >= umidade:
        atuador_sole2.value(1)
    else:
        atuador_sole2.value(0)
    time.sleep_ms(50) 
  
