from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
def index(request):
	args={}
	return render(request, 'etherfeeds/index.html', args)
def action(request):
	args={}
	return render(request,'etherfeeds/action.html',args)
def thanks(request):
	args={}
	return render(request,'etherfeeds/thanks.html',args)
