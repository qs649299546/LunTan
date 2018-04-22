# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-26 01:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20180326_0130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField()),
                ('name', models.CharField(max_length=64)),
                ('content', models.TextField()),
                ('create', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]