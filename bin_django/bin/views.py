from django.shortcuts import render
from django.http import HttpResponse

def post_data(request, d):
    # MsoCns.objects.filter(pk=pk).delete()
    r = 'Incoming: ' + d
    return HttpResponse(r)

def t(request):
	return HttpResponse("return this string")

def score_bord(request):
	args={}
	return render(request, 'bin/score_bord.html', args)

def counter(request):
	args = {}
	return render(request, 'bin/counter.html', args)