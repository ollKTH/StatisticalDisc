# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-10 21:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_scorecard_noofholes'),
    ]

    operations = [
        migrations.AddField(
            model_name='scorecard',
            name='total_score',
            field=models.PositiveIntegerField(null=True),
        ),
    ]