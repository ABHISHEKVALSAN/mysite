from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Users(models.Model):
	usrAddr = models.CharField(max_length=200)
	usrSig	= models.CharField(max_length=200)
class HashList(models.Model):
	hash=models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	exp_date = models.DateTimeField('date expiring')

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
