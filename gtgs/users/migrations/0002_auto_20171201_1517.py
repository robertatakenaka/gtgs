# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-12-01 17:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='anniversary',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Data de admissão (DD/MM/AAAA)'),
        ),
        migrations.AddField(
            model_name='user',
            name='anniversary_alert',
            field=models.BooleanField(default=True, verbose_name='Alertar tempo de SciELO'),
        ),
        migrations.AddField(
            model_name='user',
            name='birthdate',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Data de nascimento (DD/MM/AAAA)'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_checked',
            field=models.BooleanField(default=False, verbose_name='Confirmo que estes dados estão atualizados'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_checked_by_admin',
            field=models.BooleanField(default=False, verbose_name='Validado'),
        ),
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.ImageField(default='/app/gtgs/media/perfil.png', upload_to='', verbose_name='Foto'),
        ),
    ]
