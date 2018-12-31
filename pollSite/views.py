#pollSite
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Entries, Person, siteUrl

import random
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
def detail(request,pk):
	siteObj		=	get_object_or_404(siteUrl, pk=pk)
	args		=	{'object':siteObj}
	return render(request,'pollSite/detail.html',args)
def results(request,pk):
	siteObj		=	get_object_or_404(siteUrl, pk=pk)
	args		=	{'object':siteObj}
	return render(request,'pollSite/results.html',args)
def thanks(request):
	args		=	{}
	return render(request,'pollSite/thanks.html',args)
def vote(request, siteId):
	global num
	siteObj = get_object_or_404(siteUrl, pk=siteId)
	try:
	 	userRating = request.POST['choice']
	except (KeyError, siteUrl.DoesNotExist):
		return render(request, 'pollSite/detail.html', {
		'object': siteObj,
			'error_message': "You didn't select a choice.",
			})
	else:
		if userRating=="7":
			siteObj.rate7+=1
		elif userRating=="6":
			siteObj.rate6+=1
		elif userRating=="5":
			siteObj.rate5+=1
		elif userRating=="4":
			siteObj.rate4+=1
		elif userRating=="3":
			siteObj.rate3+=1
		elif userRating=="2":
			siteObj.rate2+=1
		elif userRating=="1":
			siteObj.rate1+=1
		siteObj.save()
		nextSite	=	random.choice(list(siteUrl.objects.order_by('id')))
		if num==5:
			num=0
			args={}
			return HttpResponseRedirect(reverse('pollSite:thanks'))
		num+=1
		return HttpResponseRedirect(reverse('pollSite:detail', args=(nextSite.id,)))

def newPerson(request):
	nextSite	=	random.choice(list(siteUrl.objects.order_by('id')))
	return HttpResponseRedirect(reverse('pollSite:detail', args=(nextSite.id,)))
