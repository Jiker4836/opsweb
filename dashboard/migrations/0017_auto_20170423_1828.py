# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_server'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='check_update_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
