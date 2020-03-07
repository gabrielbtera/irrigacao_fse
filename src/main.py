import machine
import time

#Função para leitura do ADC através do pino D3 do NodeMCU
from machine import Pin

#ler o potenciomentro
################# variaveis globais ########################
atuador_sole1 = Pin(15, Pin.OUT) 
atuador_sole2 = Pin(16, Pin.OUT)
umidade = 1000 # input do usuario
pino_sensor1 = 0
pino_sensor2 = 2
############################################################

#ler o potenciomentro 
"""def ler_ADC():
    adc = machine.ADC(0)
    var= adc.read()
    adc_1 = machine.ADC(pino_sensor1)
    var = adc_1.read()
    print('ADC VALUE.. = %.2f' % var)
"""


# retorna o valor do sensor 
def rtrn_valor_sensor1():
    """ 
        Falta adicionar outro potenciometro(sensor) para monitorar cada quadra
        ao todo serao duas quadras.
    """
    adc = machine.ADC(pino_sensor1)
    var_temp = adc.read()
    print('ADC VALUE.. = %.2f' % (10000/var_temp))
    return var_temp


atuador_sole1.value(0)

while True:
    value = rtrn_valor_sensor1()
    
    if value >= umidade:
        atuador_sole1.value(1)
    else:
      atuador_sole1.value(0)
      
    ler_ADC()
    time.sleep_ms(50) 
  
