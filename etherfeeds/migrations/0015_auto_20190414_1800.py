# Generated by Django 2.1.3 on 2019-04-14 18:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etherfeeds', '0014_auto_20190414_1303'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='ansHash',
            field=models.CharField(default='0x0', max_length=200),
        ),
        migrations.AddField(
            model_name='answerentries',
            name='ansEntHash',
            field=models.CharField(default='0x0', max_length=200),
        ),
        migrations.AddField(
            model_name='memberproposal',
            name='memPropHash',
            field=models.CharField(default='0x0', max_length=200),
        ),
        migrations.AddField(
            model_name='question',
            name='qnHash',
            field=models.CharField(default='0x0', max_length=200),
        ),
        migrations.AlterField(
            model_name='hashlist',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 14, 18, 0, 6, 130360), verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='memberproposal',
            name='exp_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 24, 18, 0, 6, 131874), verbose_name='date expiring'),
        ),
        migrations.AlterField(
            model_name='memberproposal',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 14, 18, 0, 6, 131826), verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='question',
            name='exp_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 24, 18, 0, 6, 130662), verbose_name='date expiring'),
        ),
    ]
