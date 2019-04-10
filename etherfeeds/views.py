from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
def index(request):
	args={}
	return render(request, 'etherfeeds/index.html', args)
def dashboard(request):
	args={}
	return render(request,'etherfeeds/dashboard.html',args)
def createpoll(request):
	args={}
	return render(request,'etherfeeds/createpoll.html',args)
def addmember(request):
	args={}
	return render(request,'etherfeeds/addmember.html',args)

def thanks(request):
	args={}
	return render(request,'etherfeeds/thanks.html',args)
