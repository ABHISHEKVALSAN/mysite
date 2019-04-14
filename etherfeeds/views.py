from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Users,Question,HashList,Answer,AnswerEntries,memberProposal
import datetime
from .EtherFeeds import authUser,addUser
def index(request):
	args={}
	return render(request, 'etherfeeds/index.html', args)
def dashboard(request):
	if authUser(str(request.user)):
		addUser('0x715f6885102c954077956EF4Eb36d6BfD1C3DE73')
		args={'user':request.user}
		return render(request,'etherfeeds/dashboard.html',args)
	else:
		args={'error_message':"You are still not a member of the compnay"}
		request.session.clear()
		return HttpResponseRedirect(reverse('etherfeeds:index'))
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
	exp_time		= pub_date+datetime.timedelta(days=int(time_exp_days))+datetime.timedelta(hours=int(time_exp_hours))+datetime.timedelta(minutes=int(time_exp_minutes))
	usrAddr			= request.user
	try:
		user	=	Users.objects.get(usrAddr=usrAddr)
	except:
		user	=	Users.objects.create(usrAddr=usrAddr,usrSig="null")
	Question.objects.create(question_text=question_text,pub_date=pub_date,etherSpent=etherSpent,\
	time_exp_days=time_exp_days,time_exp_hours=time_exp_hours,time_exp_minutes=time_exp_minutes,\
	user=user,exp_time=exp_time)
	return HttpResponseRedirect(reverse('etherfeeds:dashboard'))
def addAnswer(request,questionId):
	answer=request.POST["newAnswer"]
	questionObj=get_object_or_404(Question,pk=questionId)
	Answer.objects.create(question=questionObj,answer_text=answer)
	return HttpResponseRedirect(reverse('etherfeeds:question_view', args=(questionObj.id,)))
def thanks(request):
	args={}
	return render(request,'etherfeeds/thanks.html',args)
def feeds(request):
	questions=Question.objects.all()
	exp_time=Question.objects.values('exp_time')
	time_left=[]
	for exp in exp_time:
		time_left.append(exp['exp_time'])
	quest_time=zip(questions,time_left)
	args={'questions':quest_time}
	return render(request,'etherfeeds/feeds.html',args)
def question_view(request,pk):
	questionObj	 	= get_object_or_404(Question, pk=pk)
	answers 		= Answer.objects.filter(question=questionObj)
	status 			= []
	upvotes		 	= []
	downvotes	 	= []
	for answer in answers:
		user=get_object_or_404(Users,usrAddr=request.user)
		try:
			Obj=get_object_or_404(AnswerEntries,user=user,answer=answer)
			status.append(0)
		except:
			status.append(1)
		upvotes.append(answer.upvotes)
		downvotes.append(answer.downvotes)
	answerList=zip(answers,status,upvotes,downvotes)
	args={'question':questionObj,'answerList':answerList}
	return render(request,'etherfeeds/question_view.html',args)
def answerUpDown(request,answerId,questionId):
	answerObj	= get_object_or_404(Answer, pk=answerId)
	questionObj = get_object_or_404(Question, pk=questionId)
	user		= get_object_or_404(Users, usrAddr=request.user)
	if request.POST['answer'+answerId]=='1':
		answerObj.upvotes+=1
	else:
		answerObj.downvotes+=1
	answerObj.save()
	newVote=AnswerEntries.objects.create(answer=answerObj,user=user)
	return HttpResponseRedirect(reverse('etherfeeds:question_view', args=(questionObj.id,)))
def memberProposal(request):
	proposer	= request.user
	proposalFor	= request.POST['publicAddr']
