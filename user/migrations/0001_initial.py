# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-23 11:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=255, verbose_name='密码')),
                ('email', models.CharField(max_length=255, unique=True, verbose_name='邮箱')),
            ],
            options={
                'db_table': 'ttsx_user',
            },
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tel', models.CharField(max_length=50, unique=True, verbose_name='电话')),
                ('address', models.CharField(max_length=255, verbose_name='地址')),
                ('zcpde', models.CharField(max_length=20, verbose_name='邮编')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
            options={
                'db_table': 'ttsx_address',
            },
        ),
        migrations.CreateModel(
            name='UserTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket', models.CharField(max_length=256)),
                ('out_time', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
            options={
                'db_table': 'ttsx_ticket',
            },
        ),
    ]
