from django.shortcuts import render
from django.http import HttpResponse
from .models import *

def post_data(request, d):
    # MsoCns.objects.filter(pk=pk).delete()
    r = 'Incoming: ' + d
    return HttpResponse(r)

def t(request):
	return HttpResponse("return this string")

def scoreboard(request):
	all_stds = Student.objects.all().order_by('-score')
	args={'all_stds': all_stds}
	return render(request, 'bin/scoreboard.html', args)

def counter(request):
	args = {}
	return render(request, 'bin/counter.html', args)

def bin_stat(request):
	args = {}
	return render(request, 'bin/bin_stat.html', args)