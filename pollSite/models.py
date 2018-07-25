#pollSite


from __future__ import unicode_literals
from django.db import models

# Create your models here.

class PageUrl(models.Model):
    question_text = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(PageUrl, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
