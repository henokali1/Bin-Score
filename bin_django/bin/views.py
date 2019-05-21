from django.shortcuts import render
from django.http import HttpResponse
from .models import *
import time


def post_data(request, d):
    # MsoCns.objects.filter(pk=pk).delete()
    r = 'Incoming: ' + d
    return HttpResponse(r)

def t(request):
	return HttpResponse("return this string")

def scoreboard(request):
	scanned_id = CurrentId.objects.all().filter(pk=1)[0]
	score = ArduScore.objects.all().filter(pk=1)[0]
	score = score.score
	scanned_id = scanned_id.id_num
	if score != 0 and score > 1:
		msg = 'Congratulations, you have scored ' + str(score) + ' points!'
	elif score == 1:
		msg = msg = 'Congratulations, you have scored 1 point!'
	else:
		msg = 'You have scored 0 points!'

	# Update Score on the DB
	stdt = Student.objects.filter(id_num=scanned_id)[0]
	priv_score = stdt.score
	print('Priv Score', priv_score)

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
