from pynput.keyboard import Key, Controller
from threading import Thread, Event
from selenium import webdriver
from pynput import keyboard
from gpiozero import LED
from time import sleep
import urllib.request
import threading
import time
import ast



ardu_pin = LED(21)
ardu_pin.on()

barcode = ''


scoreboard_url = 'http://46.101.144.34:9000/bin/scoreboard/'
counter_url = 'http://46.101.144.34:9000/bin/counter/'
# open chrome (/scoreboard)
PATH_TO_DRIVER = '/home/pi/Downloads/chromedriver'
browser = webdriver.ChromeOptions()
browser.add_argument("--kiosk")
driver = webdriver.Chrome(chrome_options=browser)
browser = webdriver.Chrome(PATH_TO_DRIVER)
browser.get(scoreboard_url)

# Returns all regestered ID numbers from DB
def get_all_ids():
    f = urllib.request.urlopen("http://46.101.144.34:9000/bin/get_all_ids/")
    all_ids = f.read()
    all_ids = all_ids.decode("utf-8")

    all_ids = ast.literal_eval(all_ids)
    return all_ids

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
            all_ids = get_all_ids()
            print('DB all_ids', all_ids)
            if barcode in all_ids:
                f = urllib.request.urlopen("http://46.101.144.34:9000/bin/start_cntr/{}/".format(barcode))
                print(f.read())
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

