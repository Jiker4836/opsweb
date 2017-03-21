# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(unique=True, max_length=32)),
                ('ip', models.CharField(unique=True, max_length=15)),
                ('cpu', models.CharField(max_length=50)),
                ('mem', models.CharField(max_length=50)),
                ('disk', models.CharField(max_length=50)),
                ('sn', models.CharField(max_length=32)),
                ('idc', models.CharField(max_length=60)),
                ('ipinfo', models.CharField(max_length=255, verbose_name=b"[{'eth0':'192.168.1.1','mac':''},{'eth1':'192.168.1.1','mac':''}]")),
                ('product', models.CharField(max_length=50)),
                ('remark', models.TextField(default=b'')),
            ],
            options={
                'db_table': 'server',
            },
        ),
    ]
