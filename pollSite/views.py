#pollSite
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Choice, PageUrl

import random
"""
class IndexView(generic.ListView):
    template_name = 'pollSite/index.html'
    context_object_name = 'question_list'
    def get_queryset(self):
        return PageUrl.objects.order_by('id')
class DetailView(generic.DetailView):
    model = PageUrl
    template_name = 'pollSite/detail.html'
class ResultsView(generic.DetailView):
    model = PageUrl
    template_name = 'pollSite/results.html'
"""
num=0
def index(request):
	global	num
	num			=	0
	question_id	=	random.randint(1,6)
	question	=	get_object_or_404(PageUrl, pk=question_id)
	args		=	{'question':question}
	return render(request,'pollSite/index.html',args)
def detail(request,pk):
	question	=	get_object_or_404(PageUrl, pk=pk)
	args		=	{'object':question}
	return render(request,'pollSite/detail.html',args)
def results(request,pk):
	question	=	get_object_or_404(PageUrl, pk=pk)
	args		=	{'object':question}
	return render(request,'pollSite/results.html',args)
def thanks(request):
	args		=	{}
	return render(request,'pollSite/thanks.html',args)
def vote(request, question_id):
	global num
	question = get_object_or_404(PageUrl, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Redisplay the question voting form.
		return render(request, 'pollSite/detail.html', {
		'question': question,
			'error_message': "You didn't select a choice.",
			})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		nextQuestion	=	random.choice(list(PageUrl.objects.order_by('id')))
		if num==5:
			num=0
			args={}
			return HttpResponseRedirect(reverse('pollSite:thanks'))
		num+=1
		return HttpResponseRedirect(reverse('pollSite:detail', args=(nextQuestion.id,)))
