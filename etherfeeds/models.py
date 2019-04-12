from __future__ import unicode_literals

from django.db import models
import datetime
# Create your models here.

class Users(models.Model):
	usrAddr = models.CharField(max_length=200)
	usrSig	= models.CharField(max_length=200,default="0x0")
class HashList(models.Model):
	hash=models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	time_exp_days = models.IntegerField(default=0)
	time_exp_hours = models.IntegerField(default=0)
	time_exp_minutes = models.IntegerField(default=0)
	exp_time = models.DateTimeField('date expiring',default=datetime.datetime.now()+datetime.timedelta(days=10))
	etherSpent	= models.IntegerField(default=0)
	status	= models.IntegerField(default=1)
	user = models.ForeignKey(Users, on_delete=models.CASCADE,default=None)

class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	answer_text = models.CharField(max_length=200,default="")
	upvotes = models.IntegerField(default=0)
	downvotes = models.IntegerField(default=0)
