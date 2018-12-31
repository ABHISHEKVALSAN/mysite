#pollSite


from __future__ import unicode_literals
from django.db import models

# Create your models here.

class siteUrl(models.Model):
	urlText			=	models.CharField(max_length=500)
	pub_date		=	models.DateTimeField('date published')
	rate7			=	models.IntegerField(default=0)
	rate6			=	models.IntegerField(default=0)
	rate5			=	models.IntegerField(default=0)
	rate4			=	models.IntegerField(default=0)
	rate3			=	models.IntegerField(default=0)
	rate2			=	models.IntegerField(default=0)
	rate1			=	models.IntegerField(default=0)

class Person(models.Model):
	name			=	models.CharField(max_length=200)
	age				=	models.IntegerField(default=0)
	sex				=	models.IntegerField(default=0)
	education		=	models.IntegerField(default=0)

class Entries(models.Model):
	personId		=	models.ForeignKey(Person, on_delete=models.CASCADE)
	urlId			=	models.ForeignKey(siteUrl, on_delete=models.CASCADE)
	rating			=	models.IntegerField(default=0)
	
