from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Users,Question,HashList,Answer
# Create your views here.
import datetime


def index(request):
	args={}
	return render(request, 'etherfeeds/index.html', args)
def dashboard(request):
	if request.user:
		args={'user':request.user}
	else:
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
	question_text 	= request.POST['question']
	pub_date		= datetime.datetime.now()
	etherSpent		= request.POST['ether']
	time_exp_days	= request.POST['time_exp_days']
	time_exp_hours	= request.POST['time_exp_hours']
	time_exp_minutes= request.POST['time_exp_minutes']
	usrAddr			= request.user
	try:
		user	=	Users.objects.get(usrAddr=usrAddr)
	except:
		user	=	Users.objects.create(usrAddr=usrAddr,usrSig="null")
	Question.objects.create(question_text=question_text,pub_date=pub_date,etherSpent=etherSpent,\
	time_exp_days=time_exp_days,time_exp_hours=time_exp_hours,time_exp_minutes=time_exp_minutes,\
	user=user)
	return HttpResponseRedirect(reverse('etherfeeds:dashboard'))
def thanks(request):
	args={}
	return render(request,'etherfeeds/thanks.html',args)
def feeds(request):
	questions=Question.objects.all()
	args={'questions':questions}
	return render(request,'etherfeeds/feeds.html',args)
def question_view(request,questionid):
	questionObj	= get_object_or_404(siteUrl, pk=pk1)
	answerList	= Answer.object.get(question=questionObj)
	args={'question':questionObj,'answers':answerList}
	return render(request,'etherfeeds/question_view.html',args)
