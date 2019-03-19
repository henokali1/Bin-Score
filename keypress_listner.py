from pynput import keyboard

barcode = ''
def on_press(key):
    try:
        if (len(str(key)) == 3):
            k = str(key)
            global barcode
            barcode += key.char
        (key.char)
    except AttributeError:
        if(str(key) == 'Key.enter'):
            print(barcode)
            global barcode
            barcode = ''
        else:
            pass

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()