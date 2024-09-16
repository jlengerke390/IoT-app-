import network
import time
from accesspoint import accessPoint
from webPage import initializeWebPage
from blink import blinkLed, onLed

def connectNetwork():
    with open("data.txt", "r") as file:
        for line in file:
            ssid = line.find("SSID: ")
            password = line.find("Password: ")
            if ssid != -1:
                ssid_value = line[ssid + 6:].strip()
                print(ssid_value)
                
            if password != -1:
                password_value = line[password + 9:].strip()
                print(str(password_value))
                
    ssid = str(ssid_value)
    password = str(password_value)
    
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)
    
    attemps = 10
    while attemps > 0:
        print("Not connected to network")
        blinkLed(4, 1)
        if station.isconnected()==True:
            onLed(4)
            print("Connection Succefuly")
            print(station.ifconfig())
            break
        else:
            attemps -= 1
            
    if attemps == 0:
        print("Created esp own network")
        accessPoint()
        initializeWebPage()
        onLed(2)
    