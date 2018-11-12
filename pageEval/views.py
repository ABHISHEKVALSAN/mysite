import subprocess
import sys

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

def index(request):
	return render(request, 'pageEval/index.html')

def detail(request):
	return render(request, 'pageEval/detail.html')

def results(request):
	return render(request, 'pageEval/results.html',{
            'error_message': "You didn't select a choice.",
        })

def metrics(request):
	url			= request.POST['urlText']
	command 	= [sys.executable,"/home/abhiavk/git/mysite/pageEval/all.py",url]
	output		= subprocess.Popen(command, stdout=subprocess.PIPE, stderr = subprocess.STDOUT )
	webMetrics	= output.communicate()[0].decode("utf-8").split("\n")+[str(sys.executable)]
	return render(request, 'pageEval/results.html',{
	'webMetrics' 	: webMetrics,
	})
