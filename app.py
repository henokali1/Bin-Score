from flask import Flask, render_template, redirect, url_for, session, request, logging, json, jsonify
from pynput.keyboard import Key, Controller
from flask_socketio import SocketIO, emit
from werkzeug import secure_filename
from threading import Thread, Event
from pynput import keyboard
from random import randint
from gpiozero import LED
from time import sleep
import webbrowser
import threading
import operator
import json
import time
import os


cntr = 0
drop_delay = 10
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
socketio = SocketIO(app)

ardu_pin = LED(21)
ardu_pin.on()

barcode = ''
last_scan = 0.0

prev_bin_data = {"1":'', "2":'', "3":''}
start_cntr = False
msg = ''
def read_bin_db():
    with open('bin_data.txt') as json_file:  
        data = json.load(json_file)
    return data

def get_th(rank):
    if rank == '1':
        return rank+'st'
    elif rank == '2':
        return rank+'nd'
    elif rank == '3':
        return rank+'rd'
    else:
        return rank+'th'

def dict_srt(dict_val, srt_by):
    r = []
    for i in sorted(dict_val, key=operator.itemgetter(srt_by)):
        r.append(i)
    return r[::-1]

def del_db_data():
	with open('student_db.txt', 'w') as outfile:
		json.dump({}, outfile)

def read_db():
    with open('student_db.txt') as json_file:  
        data = json.load(json_file)
    return data


def save_db(barcode, full_name, gender, score=0):
    existing_data = read_db()
    existing_data[barcode] = {'full_name':full_name, 'gender':gender, 'score':score}
    with open('student_db.txt', 'w') as outfile:  
        json.dump(existing_data, outfile)


@app.route('/')
def index():
    msgg = msg
    global msg
    msg = ''
    all_data = read_db()
    std_lst = [all_data[i] for i in all_data]
    srtd_lst = dict_srt(std_lst, 'score')
    return render_template('scoreboard.html', all_students=srtd_lst, msg=msgg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        gender = request.form.get('gender')
        barcode = request.form.get('barcode')

        save_db(barcode=barcode, full_name=full_name.title(), gender=gender)

        print('New Student Registered\nFull Name: {}    Gender: {}  Barcode: {}'.format(full_name, gender, barcode))
        # Refresh the Leadboard Page
        socketio.emit('newnumber', {'number': 1}, namespace='/test')
        return redirect(url_for('index'))
    else:
        return render_template('register.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    all_students = read_db()
    return render_template('admin.html', all_students=read_db())


@app.route('/counter', methods=['GET'])
def counter():
    return render_template('counter.html')


@app.route('/del/<string:barcode>', methods=['GET', 'POST'])
def del_student(barcode):
    try:
        all_students=read_db()
        del all_students[str(barcode)]
        with open('student_db.txt', 'w') as outfile:  
            json.dump(all_students, outfile)
        # Refresh Leadboard Page
        socketio.emit('newnumber', {'number': 1}, namespace='/test')
        return redirect(url_for('admin'))
    except KeyError:
        return redirect(url_for('admin'))
    return redirect(url_for('admin'))

@app.route('/edit/<string:barcode>', methods=['GET', 'POST'])
def edit_student(barcode):
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        gender = request.form.get('gender')
        new_barcode = request.form.get('new_barcode')
 
        old_score = read_db()[str(barcode)]['score']
        del_student(barcode)
        save_db(
            barcode=new_barcode, full_name=full_name.title(),
            gender=gender, score=old_score
        )
        
        print('New Barcode: {}  Old barcode:    {} \nFull Name: {}\nGender:{}'.format(new_barcode, barcode, full_name, gender))
        print('-----------------------------------------------')
        # Refresh Leadboard Page
        socketio.emit('newnumber', {'number': 1}, namespace='/test')
        return redirect(url_for('admin'))
    else:
        return render_template('edit.html', stud_info=read_db()[str(barcode)], barcode=str(barcode))

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    return jsonify(result=start_cntr)


def update_score(barcode, val):
    existing_data = read_db()
    old_score = existing_data[str(barcode)]['score']
    existing_data[str(barcode)]['score'] = old_score + int(val)
    with open('student_db.txt', 'w') as outfile:  
        json.dump(existing_data, outfile)
    socketio.emit('newnumber', {'number': 1}, namespace='/test')

# Socket Thread
class SocketThread(Thread):
    def __init__(self):
        self.delay = 1
        super(SocketThread, self).__init__()

    def socket_thread(self):
        while 1:
            print('start_cntr',start_cntr)
            #update_score(barcode='5342344', val=1)
            sleep(self.delay)
            #socketio.emit('newnumber', {'number': cntr}, namespace='/test')

            bin_data = read_bin_db()
            print('bin_data: {}'.format(bin_data))
            for i in bin_data:
                if i != 'score':
                    try:
                        socketio.emit('bin_stat', {'bin_stat': bin_data[i]['val'], 'bin_id': i}, namespace='/test')
                        time.sleep(2)
                    except:
                        print('Error x001')

    def run(self):
        self.socket_thread()

        

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
            
            ex_data = read_db()
            if barcode in ex_data:
                print('Data Exists')
                global cntr
                cntr = time.time()
                global start_cntr
                start_cntr = True
                while(time.time()-cntr <= drop_delay):
                    ardu_pin.off()
                    print(time.time()-cntr)
                    time.sleep(1)
                ardu_pin.on()
                global start_cntr
                start_cntr = False

                new_score = read_bin_db()['last_score']['score']
                print('new_score: {}    barcode: {}'.format(new_score, barcode))
                
                global msg
                msg = 'You Got {} Points'.format(new_score)
                update_score(barcode=barcode, val=new_score)
                socketio.emit('newnumber', {'number': 1}, namespace='/test')

            else:
            	print('unknown barcode')
            # TO-DO Verify that barcode exists in database
            
            #update_score(barcode=barcode, val=1)
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



# Start Socket Thread
print('Starting Socket Thread')
sock_thread = SocketThread()
sock_thread.start()

# Start Keyboard Listner Thread
print('Starting Keyboard Listner Thread')            
key_list_thread = threading.Thread(name='key_list', target=key_list)
key_list_thread.start()




if __name__ == '__main__':
    #webbrowser.open('http://127.0.0.1:5000/')
    socketio.run(app)
