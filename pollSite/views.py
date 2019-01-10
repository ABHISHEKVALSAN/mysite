#pollSite
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Entries, Person, siteUrl

import random
import datetime
"""
class IndexView(generic.ListView):
    template_name = 'pollSite/index.html'
    context_object_name = 'question_list'
    def get_queryset(self):
        return siteUrl.objects.order_by('id')
class DetailView(generic.DetailView):
    model = siteUrl
    template_name = 'pollSite/detail.html'
class ResultsView(generic.DetailView):
    model = siteUrl
    template_name = 'pollSite/results.html'
"""
num=0
def index(request):
	args={}
	return render(request,'pollSite/index.html',args)
def register(request):
	args		=	{}
	return render(request,'pollSite/register.html',args)
def detail(request,pk1,pk2):
	siteObj		=	get_object_or_404(siteUrl, pk=pk1)
	PersonObj	=	get_object_or_404(Person, pk=pk2)
	args		=	{'site':siteObj,'person':PersonObj}
	return render(request,'pollSite/detail.html',args)
def results(request,pk):
	siteObj		=	get_object_or_404(siteUrl, pk=pk)
	args		=	{'object':siteObj}
	return render(request,'pollSite/results.html',args)
def thanks(request):
	args		=	{}
	return render(request,'pollSite/thanks.html',args)
def vote(request, siteId, PersonId):
	global num
	siteObj		=	get_object_or_404(siteUrl, pk=siteId)
	PersonObj	=	get_object_or_404(Person, pk=PersonId)
	userRating	= request.POST['choice']
	if userRating=="7":
		siteObj.rate7+=1
		newEntry	=	Entries.objects.create(personId=PersonObj,urlId=siteObj,rating=7)
	elif userRating=="6":
		siteObj.rate6+=1
		newEntry	=	Entries.objects.create(personId=PersonObj,urlId=siteObj,rating=6)
	elif userRating=="5":
		siteObj.rate5+=1
		newEntry	=	Entries.objects.create(personId=PersonObj,urlId=siteObj,rating=5)
	elif userRating=="4":
		siteObj.rate4+=1
		newEntry	=	Entries.objects.create(personId=PersonObj,urlId=siteObj,rating=4)
	elif userRating=="3":
		siteObj.rate3+=1
		newEntry	=	Entries.objects.create(personId=PersonObj,urlId=siteObj,rating=3)
	elif userRating=="2":
		siteObj.rate2+=1
		newEntry	=	Entries.objects.create(personId=PersonObj,urlId=siteObj,rating=2)
	elif userRating=="1":
		siteObj.rate1+=1
		newEntry	=	Entries.objects.create(personId=PersonObj,urlId=siteObj,rating=1)
	siteObj.save()
	nextSite	=	random.choice(list(siteUrl.objects.order_by('id')))
	if num==19:
		num=0
		args={}
		return HttpResponseRedirect(reverse('pollSite:thanks'))
	num+=1
	return HttpResponseRedirect(reverse('pollSite:detail', args=(nextSite.id,PersonObj.id)))
def newPerson(request):
	Name		=	request.POST['Name']
	age			=	24
	sex			=	1
	education	=	4
	PersonObj	=	Person.objects.create(name=Name,age=age,sex=sex,education=education)
	nextSite	=	random.choice(list(siteUrl.objects.order_by('id')))
	return HttpResponseRedirect(reverse('pollSite:detail', args=(nextSite.id,PersonObj.id)))
