# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-16 18:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_auto_20171216_1857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hole',
            name='round',
        ),
        migrations.AddField(
            model_name='round',
            name='holes',
            field=models.ManyToManyField(to='courses.Hole'),
        ),
    ]
