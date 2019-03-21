import time
import serial
from gpiozero import LED
from ser_com_list import serial_ports as sp

ardu_pin = LED(21)


print("Avalable port", sp()[0])

ser = serial.Serial(
 port=sp()[0],
 baudrate = 9600,
 parity=serial.PARITY_NONE,
 stopbits=serial.STOPBITS_ONE,
 bytesize=serial.EIGHTBITS,
 timeout=1
)

while 1:
	try:
		x=str(ser.readline(), 'utf-8').split(',')
		print(x)
		key_ = x[-1].replace('\r\n', '')
		if(x[2] == 'u'):
			print(x[0], x[1])
	except:
		print('err')