# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-12-04 16:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('email_from', models.EmailField(max_length=254, verbose_name='E-mail from')),
                ('email_to', models.EmailField(max_length=254, verbose_name='E-mail para')),
                ('is_active', models.BooleanField(default=False, verbose_name='Ativo')),
                ('hour', models.IntegerField(default=6, verbose_name='Hora')),
                ('default_date', models.CharField(blank=True, max_length=5, verbose_name='Date (MM-DD)')),
            ],
        ),
    ]
