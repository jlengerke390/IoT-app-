# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
#from networkConnection import connectNetwork
from stationMode import connectNetwork
import gc
import esp

gc.collect()
esp.osdebug(None)

connectNetwork()

