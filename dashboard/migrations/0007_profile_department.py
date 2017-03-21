# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_delete_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='department',
            field=models.CharField(max_length=32, null=True),
        ),
    ]
