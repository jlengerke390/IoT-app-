from umqtt.simple import MQTTClient
import time
import machine
from sensorRead import readSensor

def awsIoTCommunication():

    THING_NAME = b'Esp32_Device'
    AWS_ENDPOINT = b'SECRET_ENDPOINT'

    #AWS IoT core publish topic
    PUB_TOPIC = b'device/1/data'
    #AWS IoT core subscribe topic
    SUB_TOPIC = b'esp32/sub'

    #Reading private key and certificate
    with open('/certs/key.der', 'rb') as f:
        DEV_KEY = f.read()
        
    with  open('/certs/cert.der', 'rb') as f:
        DEV_CRT = f.read()


    #Callback function for all subscriptions
    def mqtt_subscribe_callback(topic, msg):
        print("Received message from topic: %s message: %s" %(topic, msg))


    #Set AWS IoT Core connection details
    mqtt = MQTTClient(
        client_id = THING_NAME,
        server = AWS_ENDPOINT,
        port = 8883,
        keepalive = 5000,
        ssl = True,
        ssl_params = {"key":DEV_KEY, "cert":DEV_CRT, "server_side":False})


    #Establish connection to AWS IoT core
    try:
        print("Attempting to connect to AWS IoT Core...")
        mqtt.connect()
        print("Connected to AWS IoT Core")
    except Exception as e:
        print("Failed to connect to AWS IoT Core:", e)
        return

        
    
    #set callback for subscriptions
    mqtt.set_callback(mqtt_subscribe_callback)
    mqtt.subscribe(SUB_TOPIC)

    while True:
        message = readSensor()
        print('Publishing message to topic %s message %s' % (PUB_TOPIC, message))
        mqtt.publish(topic=PUB_TOPIC, msg=message, qos=0)
        
        #check subscription for message
        mqtt.check_msg()
        time.sleep(5) 