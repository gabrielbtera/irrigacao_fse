import machine
import time
from machine import Pin

################# variaveis globais ########################
atuador_sole1 = Pin(19, Pin.OUT) 
atuador_sole2 = Pin(18, Pin.OUT)
atuador_sole3 = Pin(5, Pin.OUT)
atuador_sole4 = Pin(4, Pin.OUT)
atuador_sole5 = Pin(22, Pin.OUT)
atuador_sole6 = Pin(2, Pin.OUT)
atuador_central = Pin(21, Pin.OUT)
umidade = 4050 # input do usuario

# sensores
pino_sensor1 = Pin(34, Pin.IN) 
pino_sensor2 = Pin(35, Pin.IN)
pino_sensor3 = Pin(32, Pin.IN)
pino_sensor4 = Pin(33, Pin.IN)
pino_sensor5 = Pin(39, Pin.IN)
pino_sensor6 = Pin(36, Pin.IN)


arq = open("saida.txt", "w")

arq.write(pino_sensor6)
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
        margin-right: 10px;
        display:inline-block;
      }
      .quadrante01 {
        height: 350px;
        width: 350px;
        line-height: 350px;
        margin-right: 10px;
        display:inline-block;
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
      <h1 id="block01" class="quadrante" style="background-color: rgb(0, 0, 0);"><strong>Q1</strong></h1>
      <h1 id="block02" class="quadrante" style="background-color: rgb(0, 0, 0);"><strong>Q2</strong></h1>
      <h1 id="block03" class="quadrante" style="background-color: rgb(0, 0, 0);"><strong>Q3</strong></h1>
    <div>
      <h1 id="block04" class="quadrante01" style="background-color: rgb(0, 0, 0);"><strong>Q3</strong></h1>
      <h1 id="block05" class="quadrante01" style="background-color: rgb(0, 0, 0);"><strong>Q3</strong></h1>
      <h1 id="block06" class="quadrante01" style="background-color: rgb(0, 0, 0);"><strong>Q3</strong></h1>
    </div>
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
      
      async function changeColor(){
        let response = await fetch('/?color');
        
        if (response.ok){
          let newColor = await response.json();
          document.getElementById("block01").style.background = newColor["a"];
          document.getElementById("block02").style.background = newColor["b"];
          document.getElementById("block03").style.background = newColor["c"];
          document.getElementById("block04").style.background = newColor["d"];
          document.getElementById("block05").style.background = newColor["e"];
          document.getElementById("block06").style.background = newColor["f"];
        };
      };

      setInterval(changeColor, 250);
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
    adc3 = machine.ADC(pino_sensor3)
    adc3 = adc3.read()
    adc4 = machine.ADC(pino_sensor4)
    adc4 = adc4.read()
    adc5 = machine.ADC(pino_sensor5)
    adc5 = adc5.read()
    adc6 = machine.ADC(pino_sensor6)
    adc6 = adc6.read()
    return (percentual(adc1), percentual(adc2), percentual(adc3), percentual(adc4), percentual(adc5), percentual(adc6))


""" def getrgb():
  red = 0
  green = 0
  blue = 0
 
  for i in range(256):
    red += 1
    rgb = red, green, blue
    string = 'rgb' + str(rgb)
    yield string """


def per_rgb(percent):
  green = (255 * percent) // 100
  red = 255 - green
  blue = 0
  rgb = 'rgb(%d, %d, %d)' % (red, green, blue)
  return rgb


s = socket(AF_INET, SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

umidade = percentual(umidade)
# rgb = getrgb()
central_valv = False

while True:
  valor_sensor = retorna_valores_sensores()
  print(valor_sensor)
  conn, addr = s.accept()
  conn.send('HTTP/1.1 200 OK\n')
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  change_color = request.find('/?color')
  lock = request.find('/?lock')
  

  if lock != -1:
    if not central_valv:
      atuador_central.value(0)
      atuador_sole1.value(0)
      atuador_sole2.value(0)
      atuador_sole3.value(0)
      atuador_sole4.value(0)
      atuador_sole5.value(0)
      atuador_sole6.value(0)
      central_valv = True
    else:
      central_valv = False

  if not central_valv:
    
    if valor_sensor[0] >= umidade:
        atuador_sole1.value(0)

    else:
      atuador_sole1.value(1)

    if valor_sensor[1] >= umidade:
        atuador_sole2.value(0)

    else:
        atuador_sole2.value(1)

    if valor_sensor[2] >= umidade:
        atuador_sole3.value(0)

    else:
        atuador_sole3.value(1)

    if valor_sensor[3] >= umidade:
        atuador_sole4.value(0)

    else:
        atuador_sole4.value(1)

    if valor_sensor[4] >= umidade:
        atuador_sole5.value(0)

    else:
        atuador_sole5.value(1)
    
    if valor_sensor[5] >= umidade:
        atuador_sole6.value(0)

    else:
        atuador_sole6.value(1)

    if atuador_sole1.value() == 0 and atuador_sole2.value() == 0 and atuador_sole3.value() == 0 and atuador_sole4.value() == 0 and atuador_sole5.value() == 0 and atuador_sole6.value() == 0: # VALVULA CENTRAL
        atuador_central.value(0)

    else:
        atuador_central.value(1)
  
  # time.sleep_ms(50)
  
  if change_color != -1:
    conn.send('Content-type:application/json\r\n\r\n')
    # aux = next(rgb)
    quadrantes = '{"a":"' + per_rgb(valor_sensor[0]) + '","b":"' + per_rgb(valor_sensor[1]) + '","c":"' + per_rgb(valor_sensor[2]) + '","d":"' + per_rgb(valor_sensor[3]) + '","e":"'+ per_rgb(valor_sensor[4]) + '","f":"' + per_rgb(valor_sensor[5]) + '"}' 
    conn.sendall(quadrantes)
  else:
    response = renderizador()
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
  
  conn.close()
