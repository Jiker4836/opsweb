# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0022_zabbixhost'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='server_purpose',
            field=models.ForeignKey(to='dashboard.Product', null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='service_id',
            field=models.IntegerField(null=True, db_index=True),
        ),
    ]
