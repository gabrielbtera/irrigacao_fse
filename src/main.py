import machine
import time
 
#Função para leitura do ADC através do pino D3 do NodeMCU

#ler o potenciomentro
def ler_ADC():
    adc = machine.ADC(0)
    var= adc.read()
    print('ADC VALUE.. = %.2f' % var)
  
while(True):
    ler_ADC()
    time.sleep_ms(1000)