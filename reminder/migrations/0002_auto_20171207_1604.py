# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-12-07 18:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reminder', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reminder',
            name='hour',
        ),
        migrations.AddField(
            model_name='reminder',
            name='email_to_alt',
            field=models.EmailField(blank=True, max_length=254, verbose_name='E-mail para (alternativo)'),
        ),
    ]