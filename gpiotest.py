from gpiozero import LED
from time import sleep as delay


ardu_pin = LED(21)

while 1:
	ardu_pin.on()
	print('On')
	delay(1)
	ardu_pin.off()
	print('off')
	delay(1)

