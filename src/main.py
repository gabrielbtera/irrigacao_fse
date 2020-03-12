import machine
import time
from machine import Pin

################# variaveis globais ########################
atuador_sole1 = Pin(19, Pin.OUT) 
atuador_sole2 = Pin(18, Pin.OUT)
atuador_central = Pin(21, Pin.OUT)
umidade = 4050 # input do usuario
pino_sensor1 = Pin(34, Pin.IN) 
pino_sensor2 = Pin(35, Pin.IN)
############################################################


def percentual(leitura):
    return 100* leitura / 4095

# retorna o valor do sensor 
def retorna_valores_sensores():
    adc1 = machine.ADC(pino_sensor1) 
    adc1 = adc1.read()
    adc2 = machine.ADC(pino_sensor2)
    adc2 = adc2.read()
    return (percentual(adc1), percentual (adc2))


umidade = percentual(umidade)
while True:
    valor_sensor = retorna_valores_sensores()
    
    
    if valor_sensor[0] >= umidade:
        atuador_sole1.value(0)
    else:
      atuador_sole1.value(1)
    if valor_sensor[1] >= umidade:
        atuador_sole2.value(0)
    else:
        atuador_sole2.value(1)
    if atuador_sole1.value() == 0 and atuador_sole2.value() == 0:
        atuador_central.value(0)
    else:
        atuador_central.value(1)
    time.sleep_ms(50)
  
