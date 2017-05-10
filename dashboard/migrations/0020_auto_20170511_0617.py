# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='dev_interface',
            field=models.CharField(max_length=255, verbose_name=b'\xe5\xbc\x80\xe5\x8f\x91\xe8\xb4\x9f\xe8\xb4\xa3\xe4\xba\xba\xef\xbc\x9ausername1,username2'),
        ),
        migrations.AlterField(
            model_name='product',
            name='module_letter',
            field=models.CharField(max_length=10, verbose_name=b'\xe4\xb8\x9a\xe5\x8a\xa1\xe7\xba\xbf\xe5\xad\x97\xe6\xaf\x8d\xe7\xae\x80\xe7\xa7\xb0'),
        ),
    ]
