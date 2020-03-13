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

def renderizador():
  html = """ <!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Controle de Irrigação</title>
    <style>
      .quadrante {
        height: 350px;
        width: 350px;
        line-height: 350px;
        margin: auto;
        margin-bottom: 10px;
      }
      .button {
        background-color: #4CAF50; /* Green */
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        transition: background-color 1ms;
      }
      button:hover{
        background-color: darkgreen ;
      }
    </style>
  </head>
  <body>
    <div style="text-align: center;">
      <h1>IRRIGAÇÃO INTELIGENTE, RESPONSIVA E FORMIDÁVEL</h1>
      <h2>VÁVULA CENTRAL:<strong id="state">OFF</strong></h2>
      <button class="button" onclick="lock()">TRAVA MANUAL</button>
      <h2><strong>QUADRANTES</strong></h2>
      <h1 class="quadrante" style="background-color: rgb(67, 133, 2);"><strong>Q1</strong></h1>
      <h1 class="quadrante" style="background-color: rgb(67, 133, 2);"><strong>Q2</strong></h1>
    </div>
    <script>
      function lock(){
        fetch('/?lock').then(function(response){
          response.text().then(function(text){
            state = document.getElementById('state');
            if (state.innerHTML === 'ON'){
              state.innerHTML = 'OFF';
            } else {
              state.innerHTML = 'ON';
            }
          });
        });
      };
    </script>
  </body>
</html> """

  return html


def percentual(leitura):
    return 100* leitura / 4095


# retorna o valor do sensor 
def retorna_valores_sensores():
    adc1 = machine.ADC(pino_sensor1) 
    adc1 = adc1.read()
    adc2 = machine.ADC(pino_sensor2)
    adc2 = adc2.read()
    return (percentual(adc1), percentual (adc2))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

umidade = percentual(umidade)

while True:
    valor_sensor = retorna_valores_sensores()
    conn, addr = s.accept()
    conn.send('HTTP/1.1 200 OK\n')
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)

    if valor_sensor[0] >= umidade:
        atuador_sole1.value(0)
    
    else:
      atuador_sole1.value(1)
    
    if valor_sensor[1] >= umidade:
        atuador_sole2.value(0)
    
    else:
        atuador_sole2.value(1)
    
    if atuador_sole1.value() == 0 and atuador_sole2.value() == 0: # VALVULA CENTRAL
        atuador_central.value(0)
    
    else:
        atuador_central.value(1)
    
    time.sleep_ms(50)
    
    response = renderizador()
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
