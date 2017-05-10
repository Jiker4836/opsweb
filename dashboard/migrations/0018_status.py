# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0017_auto_20170423_1828'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32, verbose_name=b'\xe7\x8a\xb6\xe6\x80\x81')),
            ],
            options={
                'db_table': 'status',
            },
        ),
    ]
