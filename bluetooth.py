from bluepy import btle
from time import sleep

SERVICE_UUID = "0000fee0-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_UUID = "0000fee1-0000-1000-8000-00805f9b34fb"

def send(addr, data):
		p = btle.Peripheral(addr)
		svc = p.getServiceByUUID(SERVICE_UUID)
		ch = svc.getCharacteristics(CHARACTERISTIC_UUID)[0]

		for i in range(0, len(data)):
				print(ch.write(data[i], withResponse=True))

