# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-07 08:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tupa', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sarja',
            old_name='tasapiste_teht1',
            new_name='teht1',
        ),
        migrations.RenameField(
            model_name='sarja',
            old_name='tasapiste_teht2',
            new_name='teht2',
        ),
        migrations.RenameField(
            model_name='sarja',
            old_name='tasapiste_teht3',
            new_name='teht3',
        ),
        migrations.RemoveField(
            model_name='sarja',
            name='vartion_maksimikoko',
        ),
        migrations.RemoveField(
            model_name='sarja',
            name='vartion_minimikoko',
        ),
    ]
