# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2019-04-10 17:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_courseorg_course_nums'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default='', upload_to='teacher/%Y/%m', verbose_name='头像'),
        ),
    ]
