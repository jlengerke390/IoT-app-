import network

def accessPoint():
    ssid = "Esp32-Test Wifi"
    password = '123456789'
    
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, authmode=2, password=password)
    
    while ap.active() == False:
        pass
    
    print("Connection successful")
    print(ap.ifconfig())
    
    
