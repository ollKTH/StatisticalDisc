# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-19 21:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20171219_2127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='score',
            name='hole',
        ),
        migrations.RemoveField(
            model_name='score',
            name='scorecard',
        ),
        migrations.RemoveField(
            model_name='scorecard',
            name='course',
        ),
        migrations.RemoveField(
            model_name='scorecard',
            name='round',
        ),
        migrations.DeleteModel(
            name='Score',
        ),
        migrations.DeleteModel(
            name='Scorecard',
        ),
    ]
