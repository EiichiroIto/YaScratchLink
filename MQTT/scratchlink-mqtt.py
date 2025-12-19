from websocket_server import WebsocketServer
import json
import base64
import time
import sys
import random
from threading import Timer
from serial import Serial, SerialException
from serial.tools import list_ports
import paho.mqtt.client as mqtt

MQTT_PORT = 1883
BROKER = ''
TOPIC = ''
MAX_SECOND_CONECT = 60
QOS = 0
WEBSOCKET_PORT = 20111

mqttClient = None
scratchLink = None
scratchSensor = None

class ScratchLink:
    def __init__(self):
        self.close()
    def open(self):
        self.connected = True
    def close(self):
        self.connected = False
    def is_connected(self):
        return self.connected
    def characteristicDidChange(self, server, client, buf):
        response = '{"jsonrpc":"2.0","method":"characteristicDidChange","params":{"serviceId":61445,"characteristicId":"5261da01-fa7e-42ab-850b-7c80220097cc","encoding":"base64","message":"%s"}}' % (base64.b64encode(bytes(buf)).decode('utf-8'),)
        server.send_message(client, response)
    def result(self, server, client, id, ok):
        if ok:
            response = '{"jsonrpc":"2.0","id":%d,"result":null}' % id
        else:
            response = '{"jsonrpc":"2.0","id":%d,"error":{}}' % id
        server.send_message(client, response)
    def didDiscoverPeripheral(self, server, client, name, rssi, peripheralId):
        response = '{"jsonrpc":"2.0","method":"didDiscoverPeripheral","params":{"name":"%s","rssi":%d,"peripheralId":%d}}' % (name, rssi, peripheralId)
        server.send_message(client, response)

class ScratchLinkSensor:
    def __init__(self):
        self._data = bytearray(10)
    def data(self):
        return self._data
    def accelX(self, v):
        if v < 0:
            v = 65536 + v
        v = v % 65536
        self._data[0] = (v >> 8) % 256
        self._data[1] = v % 256
    def accelY(self, v):
        if v < 0:
            v = 65536 + v
        v = v % 65536
        self._data[2] = (v >> 8) % 256
        self._data[3] = v % 256
    def buttonA(self, v):
        self._data[4] = v % 2
    def buttonB(self, v):
        self._data[5] = v % 2
    def touch0(self, v):
        self._data[6] = v % 2
    def touch1(self, v):
        self._data[7] = v % 2
    def touch2(self, v):
        self._data[8] = v % 2
    def gesture(self, v):
        self._data[9] = v % 256

def update(client, server):
    print("Update start")
    time.sleep(2)
    scratchLink.characteristicDidChange(server, client, scratchSensor.data())
    time.sleep(2)
    scratchLink.characteristicDidChange(server, client, scratchSensor.data())
    last_time = time.time()
    while scratchLink.is_connected():
        if time.time() - last_time > 1:
            last_time = time.time()
            #print(last_time)
            scratchLink.characteristicDidChange(server, client, scratchSensor.data())
        time.sleep(0.01)
    print("Update exited")

def new_client(client, server):
    print("New client connected: %d" % client['id'])

def client_left(client, server):
    print("Client disconnected: %d" % client['id'])
    scratchLink.close()

def message_received(client, server, message):
    print("Client(%d) said: %s" % (client['id'], message))
    dict = json.loads(message)
    if dict['method'] == 'discover':
        print("method: discover")
        id = dict['id']
        scratchLink.result(server, client, id, True)
        scratchLink.didDiscoverPeripheral(server, client, "mqtt", -70, 65536)
    if dict['method'] == 'connect':
        print("method: connect")
        id = dict['id']
        ret = True
        scratchLink.result(server, client, id, ret)
        if ret:
            scratchLink.open()
    if dict['method'] == 'read':
        print("method: read")
        timer = Timer(1, update, (client, server))
        timer.start()
    if dict['method'] == 'write':
        print("method: write")
        message = base64.b64decode(dict['params']['message'])
        if message[0] == 0x81:
            converted = message[1:].decode()
            print("publish:" + converted)
            mqttClient.publish(TOPIC+'/say', converted, qos=QOS)
        elif message[0] == 0x82:
            converted = ''
            for x in list(message[1:]):
                converted = converted + format(x,"05b")[::-1]
            print("publish:" + converted)
            mqttClient.publish(TOPIC+'/led', converted, qos=QOS)
        id = dict['id']
        scratchLink.result(server, client, id, True)

def on_connect(client, obj, flags, rc):
    print('MQTT: Connection Success' if rc == 0 else 'Connection refuse')

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("MQTT: Unexpected disconnection.")

def on_publish(client, obj, mid):
    print("MQTT: publish=" + str(mid))

def on_message(client, obj, msg):
    print(f'TOPIC: {msg.topic}, QOS: {msg.qos}, PAYLOAD: {msg.payload}')
    if msg.topic == TOPIC + '/button/a':
        scratchSensor.buttonA(int(msg.payload))
    if msg.topic == TOPIC + '/button/b':
        scratchSensor.buttonB(int(msg.payload))
    if msg.topic == TOPIC + '/touch/0':
        scratchSensor.touch0(int(msg.payload))
    if msg.topic == TOPIC + '/touch/1':
        scratchSensor.touch1(int(msg.payload))
    if msg.topic == TOPIC + '/touch/2':
        scratchSensor.touch2(int(msg.payload))
    if msg.topic == TOPIC + '/accel/x':
        scratchSensor.accelX(int(msg.payload))
    if msg.topic == TOPIC + '/accel/y':
        scratchSensor.accelY(int(msg.payload))

def on_subscribe(client, obj, mid, granted_qos):
    print("MQTT: subscribed=" + str(mid) + " " + str(granted_qos))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("python %s broker topic" % (sys.argv[0]))
        exit()
    BROKER = sys.argv[1]
    TOPIC = sys.argv[2]

    scratchLink = ScratchLink()
    scratchSensor = ScratchLinkSensor()

    mqttClient = mqtt.Client()
    mqttClient.on_connect = on_connect
    mqttClient.on_publish = on_publish
    mqttClient.on_message = on_message
    mqttClient.on_subscribe = on_subscribe
    mqttClient.connect(BROKER, MQTT_PORT, MAX_SECOND_CONECT)
    mqttClient.subscribe(TOPIC+'/#')
    mqttClient.loop_start()

    server = WebsocketServer(port = WEBSOCKET_PORT)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    server.set_fn_message_received(message_received)
    server.run_forever()
