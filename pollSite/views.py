#pollSite

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import Choice, PageUrl


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

def vote(request, question_id):
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
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('pollSite:results', args=(question.id,)))

