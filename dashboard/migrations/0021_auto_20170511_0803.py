# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0020_auto_20170511_0617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='module_letter',
            field=models.CharField(max_length=32, verbose_name=b'\xe4\xb8\x9a\xe5\x8a\xa1\xe7\xba\xbf\xe5\xad\x97\xe6\xaf\x8d\xe7\xae\x80\xe7\xa7\xb0'),
        ),
    ]
