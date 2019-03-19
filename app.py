from flask import Flask, render_template, redirect, url_for, session, request, logging, json
from flask_socketio import SocketIO, emit
from werkzeug import secure_filename
from threading import Thread, Event
from random import randint
from time import sleep
import webbrowser
import operator
import json
import time
import os


UPLOAD_FOLDER = 'C:/Users/Henok/Documents/MEGA/MEGAsync/Projects/Garbage Bin Score/static/img'
cntr = 0

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#turn the flask app into a socketio app
socketio = SocketIO(app)



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
def index(msg=''):
    all_data = read_db()
    std_lst = [all_data[i] for i in all_data]
    srtd_lst = dict_srt(std_lst, 'score')
    return render_template('scoreboard.html', all_students=srtd_lst, msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        gender = request.form.get('gender')
        barcode = request.form.get('barcode')

        # try:
        #     f = request.files['file']
        #     u_file_name = str(time.time()) + f.filename
        #     f.save(os.path.join(app.config['UPLOAD_FOLDER'], u_file_name))
        # except:
        #     if gender == 'female':
        #         u_file_name = 'female_profile_default.png'
        #     else:
        #         u_file_name = 'male_profile_default.png'
        
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
 
        # try:
        #     f = request.files['file']
        #     u_file_name = str(time.time()) + f.filename   
        #     print(u_file_name)         
        #     f.save(os.path.join(app.config['UPLOAD_FOLDER'], u_file_name))
        #     print('Phot changed')
        # except:
        #     u_file_name = read_db()[str(barcode)]['prof_img']
        #     print('No photo uploaded: {}'.format(u_file_name))
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

def update_score(barcode, val):
    existing_data = read_db()
    old_score = existing_data[str(barcode)]['score']
    existing_data[str(barcode)]['score'] = old_score + int(val)
    with open('student_db.txt', 'w') as outfile:  
        json.dump(existing_data, outfile)

# Socket Thread
class SocketThread(Thread):
    def __init__(self):
        self.delay = 1
        super(SocketThread, self).__init__()

    def socket_thread(self):
        while 1:
            global cntr
            cntr += 5
            #print(cntr)
            #update_score(barcode='5342344', val=1)
            sleep(self.delay)
            #socketio.emit('newnumber', {'number': cntr}, namespace='/test')

            stat_val = randint(0, 100)
            bin_id = randint(1,3)
            # print('stat_val: {} Bin ID: {}'.format(stat_val, bin_id))
            # socketio.emit('bin_stat', {'bin_stat': stat_val, 'bin_id': str(bin_id)}, namespace='/test')
    
    def run(self):
        self.socket_thread()
        

# Start Socket Thread
print('Starting Socket Thread')
sock_thread = SocketThread()
sock_thread.start()


if __name__ == '__main__':
    #webbrowser.open('http://127.0.0.1:5000/')
    socketio.run(app)
