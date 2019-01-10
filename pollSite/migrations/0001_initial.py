# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-24 14:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('age', models.IntegerField(default=0)),
				('sex', models.IntegerField(default=0)),
				('education', models.IntegerField(default=0)),

            ],
        ),
        migrations.CreateModel(
            name='siteUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urlText', models.CharField(max_length=500)),
				('rate7',models.IntegerField(default=0)),
				('rate6',models.IntegerField(default=0)),
				('rate5',models.IntegerField(default=0)),
				('rate4',models.IntegerField(default=0)),
				('rate3',models.IntegerField(default=0)),
				('rate2',models.IntegerField(default=0)),
				('rate1',models.IntegerField(default=0)),
            ],
        ),
		migrations.CreateModel(
            name='Entries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
				('rating',models.IntegerField(default=0)),
            ],
        ),
		migrations.AddField(
            model_name	=	'Entries',
            name		=	'personId',
            field		=	models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pollSite.Person'),
		),
		migrations.AddField(
            model_name	=	'Entries',
            name		=	'urlId',
            field		=	models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pollSite.siteUrl'),
		),
    ]
