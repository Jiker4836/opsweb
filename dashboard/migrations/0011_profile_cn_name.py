# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_profile_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='cn_name',
            field=models.CharField(max_length=32, null=True, verbose_name=b'\xe4\xb8\xad\xe6\x96\x87\xe5\x90\x8d'),
        ),
    ]
