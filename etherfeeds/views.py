from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
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
def addQuestion(request):
	args={}
	question = request.POST['question']

	return HttpResponseRedirect(reverse('etherfeeds:dashboard'))
def thanks(request):
	args={}
	return render(request,'etherfeeds/thanks.html',args)
