from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import time


# Returns a list of all registerd ID num's in the DB
def get_all_ids(request):
	ids=[]
	stdt_obj = Student.objects.all()
	for i in stdt_obj:
		ids.append(str(i.id_num))
	ids = str(ids)
	return HttpResponse(str(ids))

# Verifys ID Num posted time stamp
def verify_id_ts():
	scanned_id_ts_obj = CurrentId.objects.all().filter(pk=1)[0]
	scanned_id_ts = scanned_id_ts_obj.current_ts
	time_diff = int(time.time()) - scanned_id_ts
	print('c_ts - scanned_id_ts', time_diff)
	return time_diff < 15

def scoreboard(request):
	scanned_id = CurrentId.objects.all().filter(pk=1)[0]
	print('verify_id_ts', verify_id_ts())
	score = ArduScore.objects.all().filter(pk=1)[0]
	score = score.score
	scanned_id = scanned_id.id_num
	if verify_id_ts():
		if score != 0 and score > 1:
			msg = 'Congratulations, you have scored ' + str(score) + ' points!'
		elif score == 1:
			msg = msg = 'Congratulations, you have scored 1 point!'
		else:
			msg = 'You have scored 0 points!'
	else:
		msg = ''

	# Update Score on the DB
	stdt = Student.objects.filter(id_num=scanned_id)[0]
	priv_score = stdt.score
	print('Priv Score', priv_score)
	if verify_id_ts():
		Student.objects.filter(id_num=scanned_id).update(score=score+priv_score)
	
	all_stds = Student.objects.all().order_by('-score')
	args={'all_stds': all_stds, 'msg': msg,}
	print(scanned_id, score)
	return render(request, 'bin/scoreboard.html', args)

def counter(request):
	args = {}
	return render(request, 'bin/counter.html', args)

def bin_stat(request):
	us_dist = UsDistance.objects.all()[0]
	args = {'us_dist': us_dist}
	return render(request, 'bin/bin_stat.html', args)

def post_bin_stat(request, bin1, bin2, bin3):
	UsDistance.objects.filter(pk=1).update(
		us_one = bin1,
		us_two = bin2,
		us_three = bin3,
		)
	return HttpResponse(str(bin1) + '-' + str(bin2) + '-' + str(bin3))

def start_cntr(request, std_id):
	CurrentId.objects.filter(pk=1).update(
		id_num = std_id,
		current_ts = str(int(time.time())),
		)
	return HttpResponse(std_id)

def post_score(request, score):
	ArduScore.objects.filter(pk=1).update(
		score = score,
		current_ts = str(int(time.time())),
		)
	return HttpResponse(score)

def reg(request):
	args = {}
	if request.method == 'POST':
		new_student = Student()
		full_name = request.POST['full_name']
		new_student.full_name = full_name
		new_student.id_num = request.POST['barcode']
		
		msg = 'Welcome, {}'.format(full_name) + '! You are registered successfully!!'
		args['msg']=msg
		args['all_stds'] = Student.objects.all().order_by('-score')

		# Save to DB
		new_student.save()
		return render(request, 'bin/scoreboard.html', args)

	return render(request, 'bin/reg.html', args)

def a(request):
	args = {}
	return render(request, 'bin/a.html', args)