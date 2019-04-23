from simple import MQTTClient
import time
import network
import neopixel,machine
import socket

wifi_essid = 'BeContinue'
wifi_password = 'xxxx'

port = 4242

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0',port))
s.settimeout(0)
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(wifi_essid,wifi_password)
time.sleep(10)
pin = machine.Pin(4)

def sub_cb(topic, msg):
  global pin
  chunks = [msg[i:i + 3] for i in range(0, len(msg), 3)]
  np = neopixel.NeoPixel(pin,len(chunks))
  i = 0
  for chunk in chunks:
      if len(chunk)==3:
          np[i] = (chunk[0],chunk[1],chunk[2])
      i = i + 1
  np.write()
   
client_id = "lampjes"
mqtt_server = "192.168.142.66"
def connect_and_subscribe():
  global client_id, mqtt_server
  client = MQTTClient(client_id, mqtt_server)
  client.connect()
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  client.publish('hack42/lounge-ledjes', str(sta_if.ifconfig()), retain=True)
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    client.check_msg()
    try:
        data,addr=s.recvfrom(1500)
        if len(data)>2:
            sub_cb('lampjes',data)
    except:
        pass
  except OSError as e:
    restart_and_reconnect()
