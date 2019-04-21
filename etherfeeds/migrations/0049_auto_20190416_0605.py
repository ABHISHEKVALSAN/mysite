# Generated by Django 2.1.3 on 2019-04-16 06:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('etherfeeds', '0048_auto_20190416_0552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hashlist',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 16, 6, 5, 46, 563349), verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='memberproposal',
            name='exp_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 26, 6, 5, 46, 564874), verbose_name='date expiring'),
        ),
        migrations.AlterField(
            model_name='memberproposal',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 16, 6, 5, 46, 564825), verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='question',
            name='exp_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 26, 6, 5, 46, 563650), verbose_name='date expiring'),
        ),
    ]
