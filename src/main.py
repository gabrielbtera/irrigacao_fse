import machine
import time
from machine import Pin

################# variaveis globais ########################
atuador_sole1 = Pin(15, Pin.OUT) 
atuador_sole2 = Pin(16, Pin.OUT)
umidade = float(input("Digite a humidade:"))
pino_sensor1 = 0
pino_sensor2 = 2
############################################################

#ler o potenciomentro 
def ler_ADC():
    adc_1 = machine.ADC(pino_sensor1)
    var = adc_1.read()
    print('ADC VALUE.. = %.2f' % var)


# retorna o valor do sensor 
def rtrn_valor_sensor1():
    """ 
        Falta adicionar outro potenciometro(sensor) para monitorar cada quadra
        ao todo serao duas quadras.
    """
    adc = machine.ADC(pino_sensor1)
    var_temp = adc.read()
    return var_temp


def retrn_valor_sensor2():
    pass


atuador_sole1.value(1)
while(True):
    if rtrn_valor_sensor1 == umidade:
        atuador_sole1.value(0)
    ler_ADC()
    time.sleep_ms(1000)
