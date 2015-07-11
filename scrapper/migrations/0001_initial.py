# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('internal_id', models.CharField(max_length=255, null=True, verbose_name='ID na Vivo', blank=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Nome', blank=True)),
                ('avaliabilty', models.CharField(max_length=255, null=True, verbose_name='Disponibilidade', blank=True)),
                ('date', models.DateTimeField(null=True, verbose_name='Data e hora', blank=True)),
                ('link', models.CharField(max_length=255, null=True, verbose_name='Link', blank=True)),
                ('location', models.CharField(max_length=255, null=True, verbose_name='Localiza\xe7\xe3o', blank=True)),
                ('address', models.CharField(max_length=255, null=True, verbose_name='Endere\xe7o', blank=True)),
                ('description', models.CharField(max_length=255, null=True, verbose_name='Descri\xe7\xe3o', blank=True)),
            ],
        ),
    ]
