import dht
import ujson
from machine import Pin
from time import sleep


def readSensor():
    global tem_percentage
    sensor = dht.DHT22(Pin(5))
    
    while True:
        
        try:
            sensor.measure()
            tem = sensor.temperature()
            hum = sensor.humidity()
        
            hum = round(hum, 2)
            
            data = {"Temperature": tem, "Humidity": hum}
            json_data = ujson.dumps(data)
            
            print(json_data)
            sleep(10)
            return json_data
        except OSError as e:
            print("Failed to read dht11")
           
           
        
    
        
        