# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_profile_cn_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='cn_name',
            new_name='name',
        ),
    ]
