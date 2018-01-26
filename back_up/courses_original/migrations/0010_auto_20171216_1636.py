# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-16 15:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_round_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='round',
            name='holes',
        ),
        migrations.AddField(
            model_name='hole',
            name='round',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.Round'),
        ),
    ]
