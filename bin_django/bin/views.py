from django.shortcuts import render
from django.http import HttpResponse

def post_data(request, d):
    # MsoCns.objects.filter(pk=pk).delete()
    r = 'Incoming: ' + d
    return HttpResponse(r)

def t(request):
	return HttpResponse("return this string")

def scoreboard(request):
	args={}
	return render(request, 'bin/scoreboard.html', args)

def counter(request):
	args = {}
	return render(request, 'bin/counter.html', args)

def a(request):
	args = {}
	return render(request, 'bin/a.html', args)