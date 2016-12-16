# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-06 11:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0006_remove_tournament_stage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mode', models.CharField(choices=[('REG', 'Regular'), ('PO', 'Playoff')], default='REG', max_length=3)),
            ],
        ),
        migrations.RemoveField(
            model_name='round',
            name='status',
        ),
        migrations.RemoveField(
            model_name='round',
            name='tournament',
        ),
        migrations.RemoveField(
            model_name='team',
            name='matches',
        ),
        migrations.RemoveField(
            model_name='tournament',
            name='mode',
        ),
        migrations.AddField(
            model_name='match',
            name='teams',
            field=models.ManyToManyField(to='tournament.Team'),
        ),
        migrations.AddField(
            model_name='stage',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.Tournament'),
        ),
        migrations.AddField(
            model_name='round',
            name='stage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.Stage'),
        ),
    ]