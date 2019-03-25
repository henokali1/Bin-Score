import time
import serial
from gpiozero import LED
from ser_com_list import serial_ports as sp
from random import randint
import json



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


def read_db():
    with open('bin_data.txt') as json_file:  
        data = json.load(json_file)
    return data


def save_bin_data(bin_num, val):
    existing_data = read_db()
    existing_data[bin_num] = {'bin_num':bin_num, 'val':val}
    with open('bin_data.txt', 'w') as outfile:  
        json.dump(existing_data, outfile)

def save_score_data(val):
	existing_data = read_db()
	existing_data['last_score'] = {'score':val}
	with open('bin_data.txt', 'w') as outfile:
		json.dump(existing_data, outfile)
	print('im called .................')




while 1:
	try:
		x=str(ser.readline(), 'utf-8').split(',')
		print(x)
		if x[2] == 'u':
			val = x[0]
			bin_num = x[1]
			#val = str(randint(0,100))
			save_bin_data(bin_num, val)
			print('Bin #{}	Val:{}'.format(bin_num, val))
		
		
		if x[1] == 's':
			print('Score: {}'.format(x[0]))
			save_score_data(x[0])
	except:
		print('err')