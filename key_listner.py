from pynput.keyboard import Key, Controller
from threading import Thread, Event
from selenium import webdriver
from pynput import keyboard
from gpiozero import LED
from time import sleep
import threading
import time


ardu_pin = LED(21)
ardu_pin.on()

barcode = ''


scoreboard_url = 'http://46.101.144.34:9000/bin/scoreboard/'
counter_url = 'http://46.101.144.34:9000/bin/counter/'
# open chrome (/scoreboard)
PATH_TO_DRIVER = '/home/pi/Downloads/chromedriver'
browser = webdriver.Chrome(PATH_TO_DRIVER)
browser.get(scoreboard_url)


def on_press(key):
    try:
        if (len(str(key)) == 3):
            k = str(key)
            global barcode
            barcode += key.char
        (key.char)
    except AttributeError:
        if(str(key) == 'Key.enter'):
            print('Scanned Barcode: {}'.format(barcode))
            # verify if scanned id existes in DB
            if barcode == '1234':
            	ardu_pin.off()
            	browser.get(counter_url)
            	sleep(10)
            	ardu_pin.on()
            else:
            	print('Unknown Barcode(ID)')

            # start counter(/counter)

            global barcode
            barcode = ''
        else:
            pass

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def key_list():
    while 1:
        # Collect events until released
        with keyboard.Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()


# Start Keyboard Listner Thread
print('Starting Keyboard Listner Thread')            
key_list_thread = threading.Thread(name='key_list', target=key_list)
key_list_thread.start()

